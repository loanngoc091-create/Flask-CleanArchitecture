from flask import Blueprint, jsonify, request, g
from flasgger import swag_from
from infrastructure.unit_of_work import UnitOfWork
from services.student_syllabus_service import StudentSyllabusService
from api.middleware import jwt_required
from api.role_required import require_role
from services.search_service import SearchService
from services.subscription_service import SubscriptionService
from services.feedback_service import FeedbackService
from services.syllabus_service import SyllabusService
from infrastructure.models.syllabus_model import SyllabusModel
from infrastructure.databases.db import db

bp = Blueprint("student_syllabus", __name__, url_prefix="/student/syllabus")

@bp.route("/list", methods=["GET"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student"],
    "summary": "View published syllabi",
    "security": [{"BearerAuth": []}],
    "responses": {
        200: {
            "description": "List of published syllabi",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "course_code": {"type": "string"},
                        "course_name": {"type": "string"},
                        "semester": {"type": "string"},
                        "status": {"type": "string"}
                    }
                }
            }
        }
    }
})

def view_published_syllabus():
    service = StudentSyllabusService(UnitOfWork())
    syllabi = service.get_published_syllabi()
    return jsonify(syllabi)

@bp.route("<int:syllabus_id>", methods=["GET"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student"],
    "summary": "View syllabus detail",
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "syllabus_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "example": 1444
        }
    ],
    "responses": {
        200: {
            "description": "Syllabus detail",
            "schema": {
                "type": "object",
                "properties": {
                    "syllabus_id": {
                        "type": "integer",
                        "example": 1444
                    },
                    "course_name": {
                        "type": "string",
                        "example": "Lập trình Python"
                    },
                    "course_code": {
                        "type": "string",
                        "example": "IT001"
                    },
                    "ai_summary": {
                        "type": "string",
                        "example": "Môn học giúp sinh viên nắm vững Python..."
                    },
                    "roadmap": {
                        "type": "string",
                        "example": "Tuần 1: Cơ bản, Tuần 2: OOP..."
                    },
                    "outcomes": {
                        "type": "string",
                        "example": "Có thể xây dựng ứng dụng Python"
                    }
                }
            }
        },
        404: {
            "description": "Syllabus not found"
        }
    }
})
def detail(syllabus_id):
    service = StudentSyllabusService(UnitOfWork())
    syllabus = service.get_published_detail(syllabus_id)

    return jsonify(syllabus)

@bp.route("/syllabus/search", methods=["GET"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student"],
    "summary": "Search published syllabi",
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "keyword",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Tên hoặc mã học phần"
        },
        {
            "name": "major",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Ngành học"
        },
        {
            "name": "semester",
            "in": "query",
            "type": "integer",
            "required": False,
            "description": "Học kỳ"
        }
    ],
    "responses": {
        200: {
            "description": "Danh sách đề cương đã công bố",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "syllabus_id": {"type": "integer"},
                        "course_code": {"type": "string"},
                        "course_name": {"type": "string"},
                        "major": {"type": "string"},
                        "semester": {"type": "integer"},
                        "status": {"type": "string"}
                    }
                }
            }
        }
    }
})
def search():
    keyword = request.args.get("keyword")
    major = request.args.get("major")
    semester = request.args.get("semester", type=int)

    with UnitOfWork() as uow:
        service = SearchService(uow)
        result = service.search_published(
            keyword=keyword,
            major=major,
            semester=semester
        )

    return jsonify(result), 200

@bp.route("/student/syllabus/subscribe", methods=["POST"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student"],
    "summary": "Subscribe syllabus",
    "description": "Sinh viên theo dõi (subscribe) một đề cương đã được publish",
    "security": [{"BearerAuth": []}],
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
                        "example": 1458
                    }
                },
                "required": ["syllabus_id"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Subscribe thành công",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Subscribe success"
                    }
                }
            }
        },
        400: {
            "description": "Thiếu syllabus_id hoặc dữ liệu không hợp lệ"
        },
        401: {
            "description": "Chưa đăng nhập / token không hợp lệ"
        },
        403: {
            "description": "Không có quyền (chỉ STUDENT)"
        }
    }
})
def subscribe():
    data = request.json

    service = SubscriptionService(UnitOfWork())
    service.subscribe(
        student_id=g.user["user_id"],
        syllabus_id=data["syllabus_id"]
    )

    return jsonify({"message": "Subscribe success"}), 200


@bp.route("/syllabus/feedback", methods=["POST"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student"],
    "security": [{"BearerAuth": []}],
    "summary": "Send feedback",
    "parameters": [{
        "in": "body",
        "schema": {
            "type": "object",
            "properties": {
                "syllabus_id": {"type": "integer"},
                "content": {"type": "string"}
            },
            "required": ["syllabus_id", "content"]
        }
    }]
})
def feedback():
    data = request.json

    service = FeedbackService(UnitOfWork())
    service.send_feedback(
        student_id=g.user["user_id"],
        syllabus_id=data["syllabus_id"],
        content=data["content"]
    )

    return jsonify({"message": "Feedback sent"})

@bp.route("/student/syllabus/<int:syllabus_id>")
@jwt_required()
def syllabus_detail(syllabus_id):

    syllabus = (
        db.session.query(SyllabusModel)
        .filter_by(syllabus_id=syllabus_id)
        .first()
    )

    if not syllabus:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "file_path": syllabus.file_path,
        "ai_summary": syllabus.ai_summary or "",
        "learning_path": syllabus.learning_path or [],
        "outcomes": syllabus.outcomes or []
    })
