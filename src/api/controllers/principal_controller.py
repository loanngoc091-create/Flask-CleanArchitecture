from flask import Blueprint, request, jsonify, g
from flasgger import swag_from

from services.approval_service import ApprovalService
from infrastructure.unit_of_work import UnitOfWork
from api.middleware import jwt_required
from api.role_required import require_role

bp = Blueprint("principal_approval", __name__)

@bp.route("/final-approval", methods=["POST"])
@jwt_required()
@require_role("PRINCIPAL")
@swag_from({
    "tags": ["Principal Approval"],
    "summary": "Final approval by Principal",
    "description": "Principal approves or rejects syllabus (final step)",
    "security": [{"BearerAuth": []}],
    "consumes": ["application/json"],
    "parameters": [
        
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "syllabus_id": {
                        "type": "integer",
                        "example": 12
                    },
                    "decision": {
                        "type": "string",
                        "enum": ["APPROVED", "REJECTED"],
                        "example": "APPROVED"
                    },
                    "comment": {
                        "type": "string",
                        "example": "Final approval by Principal"
                    }
                },
                "required": ["syllabus_id", "decision"]
            }
        }
    ],
    "responses": {
        200: {"description": "Final approval success"},
        400: {"description": "Approval failed"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})
def final_approval():
    data = request.json

    # ✅ lấy user_id từ token giống HOD
    user_id = g.user["user_id"]

    service = ApprovalService(UnitOfWork())

    try:
        service.final_approval(
            syllabus_id=data["syllabus_id"],
            decision=data["decision"],
            user_id=user_id
        )

        return jsonify({"message": "Final approval successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
