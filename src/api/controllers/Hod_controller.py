from flask import Blueprint, request, jsonify,g
from flasgger import swag_from

from services.approval_service import ApprovalService
from infrastructure.unit_of_work import UnitOfWork
from infrastructure.databases.db import db
from infrastructure.models.clo_model import CLO
from api.middleware import jwt_required
from api.role_required import require_role

bp = Blueprint("hod", __name__, url_prefix="/hod")


@bp.route("/approve", methods=["POST"])
@jwt_required()
@require_role("HOD")
@swag_from({
    "tags": ["HOD Approval"],
    "summary": "HOD approve or reject syllabus",
    "description": "Head of Department reviews syllabus",
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "syllabus_id": {"type": "integer"},
                    "decision": {
                        "type": "string",
                        "enum": ["APPROVED", "REJECTED"]
                    },
                    "comment": {"type": "string"}
                },
                "required": ["syllabus_id", "decision"]
            }
        }
    ],

    "responses": {
        200: {"description": "HOD reviewed successfully"},
        401: {"description": "Missing token"},
        403: {"description": "Forbidden"}
    }
})
def hod_approve():
    data = request.json

    service = ApprovalService(UnitOfWork())
    service.hod_approve(
        syllabus_id=data["syllabus_id"],
        decision=data["decision"],
        user_id=g.user["user_id"]
    )

    return jsonify({"message": "HOD approved successfully"})

@bp.route("/api/clo", methods=["GET"])
@jwt_required()
@require_role("HOD")
def get_clos():
    """
    Lấy danh sách CLO (tất cả hoặc theo đề cương)
    ---
    tags:
      - CLO
    security:
      - BearerAuth: []
    parameters:
      - name: syllabus_id
        in: query
        type: integer
        required: false
        description: ID đề cương (nếu không truyền → lấy tất cả CLO)
    responses:
      200:
        description: Danh sách CLO
    """

    syllabus_id = request.args.get("syllabus_id", type=int)

    query = db.session.query(CLO)

    if syllabus_id:
        query = query.filter(CLO.syllabus_id == syllabus_id)

    clos = query.order_by(CLO.clo_code).all()

    return jsonify([
        {
            "clo_id": c.clo_id,
            "clo_code": c.clo_code,
            "description": c.description,
            "syllabus_id": c.syllabus_id
        }
        for c in clos
    ])