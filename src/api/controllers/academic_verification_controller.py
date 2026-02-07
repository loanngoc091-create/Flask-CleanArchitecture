from flask import Blueprint, request, jsonify, g
from flasgger import swag_from

from services.academic_verification_service import AcademicVerificationService
from domain.commands.verify_syllabus_command import VerifySyllabusCommand
from infrastructure.unit_of_work import UnitOfWork
from api.middleware import jwt_required
from infrastructure.databases.db import db
from infrastructure.models.plo_model import PLO
from api.role_required import require_role

bp = Blueprint("academic_verify", __name__)

@bp.route("/verify", methods=["POST"])
@jwt_required()
@require_role("ACADEMIC_AFFAIRS")
@swag_from({
    "tags": ["Academic Verification"],
    "summary": "Verify syllabus",
    "description": "Academic Affairs verifies syllabus after department review",
    "security": [{"BearerAuth": []}],
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "syllabus_id": {
                        "type": "integer",
                        "example": 1
                    },
                    "decision": {
                        "type": "string",
                        "enum": ["APPROVED", "REJECTED"],
                        "example": "APPROVED"
                    },
                    "comment": {
                        "type": "string",
                        "example": "CLO–PLO mapping is valid"
                    }
                },
                "required": ["syllabus_id", "decision"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Verify successfully"
        },
        400: {
            "description": "Verification failed"
        }
    }
})
def verify_syllabus():
    data = request.json

    # 🔥 LẤY USER TỪ JWT PAYLOAD
    user_id = g.user.get("user_id")
    role_code = g.user.get("role_code")

    command = VerifySyllabusCommand(
        syllabus_id=data["syllabus_id"],
        decision=data["decision"],
        comment=data.get("comment")
    )

    service = AcademicVerificationService(UnitOfWork())

    try:
        service.verify_syllabus(
            command=command,
            user_id=user_id
        )

        return jsonify({
            "message": "Verify successfully",
            "verified_by": role_code
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/api/plo", methods=["GET"])
@jwt_required()
@require_role("ACADEMIC_AFFAIRS")
def get_plos():
    """
    Lấy danh sách PLO (tất cả hoặc theo CTĐT)
    ---
    tags:
      - PLO
    security:
      - BearerAuth: []
    parameters:
      - name: program_id
        in: query
        type: integer
        required: false
        description: ID chương trình đào tạo (nếu không truyền → lấy tất cả)
    responses:
      200:
        description: Danh sách PLO
    """

    program_id = request.args.get("program_id", type=int)

    query = db.session.query(PLO)

    if program_id:
        query = query.filter(PLO.program_id == program_id)

    plos = query.order_by(PLO.plo_code).all()

    return jsonify([
        {
            "plo_id": p.plo_id,
            "plo_code": p.plo_code,
            "description": p.description,
            "program_id": p.program_id
        }
        for p in plos
    ])