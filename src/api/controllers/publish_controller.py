from flasgger import swag_from
from flask import Blueprint, request, jsonify, g

from api.middleware import jwt_required
from api.role_required import require_role
from infrastructure.unit_of_work import UnitOfWork
from services.publish_service import PublishService
from infrastructure.models.course_model import Course
from infrastructure.models.syllabus_model import SyllabusModel
from infrastructure.databases.db import db

bp = Blueprint("publish", __name__)

@bp.route("/publish", methods=["POST"])
@jwt_required()
@require_role("ACADEMIC_AFFAIRS")
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Publish syllabus",
    "description": "Publish syllabus after Principal approval so students can view and download",
    "security": [
        {
            "BearerAuth": []
        }
    ],
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
                    }
                },
                "required": ["syllabus_id"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Syllabus published successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Syllabus published"
                    }
                }
            }
        },
        400: {"description": "Invalid request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})
def publish_syllabus():
    data = request.json

    PublishService(UnitOfWork()).publish(
        syllabus_id=data["syllabus_id"],
        user_id=g.user["user_id"]
    )

    return jsonify({"message": "Syllabus published"})

@bp.route("/publish/list", methods=["GET"])
@jwt_required()
@require_role("ACADEMIC_AFFAIRS")
@swag_from({
    "tags": ["Syllabus - Publish"],
    "summary": "Danh sách đề cương chờ publish",
    "description": "Lấy danh sách đề cương đã được Principal duyệt (status = Approved) để Academic Affairs publish",
    "security": [{"BearerAuth": []}],
    "responses": {
        200: {
            "description": "Danh sách đề cương",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 12
                        },
                        "course_name": {
                            "type": "string",
                            "example": "Công nghệ phần mềm"
                        },
                        "status": {
                            "type": "string",
                            "example": "Approved"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Không đủ quyền (chỉ AA)"
        }
    }
})
def list_syllabus_to_publish():
    syllabi = (
        db.session.query(SyllabusModel, Course)
        .join(Course, SyllabusModel.course_id == Course.course_id)
        .filter(SyllabusModel.status == "Approved")
        .order_by(SyllabusModel.create_date.desc())
        .all()
    )

    return jsonify([
        {
            "id": s.syllabus_id,
            "course_name": c.course_name,
            "status": s.status
        }
        for s, c in syllabi
    ])

@bp.route("/publish/<int:syllabus_id>", methods=["GET"])
@jwt_required()
@require_role("STUDENT")
@swag_from({
    "tags": ["Student - Syllabus"],
    "summary": "Student xem đề cương đã publish",
    "description": "Sinh viên xem chi tiết đề cương đã được publish, bao gồm file gốc và nội dung AI",
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "syllabus_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "example": 1458
        }
    ],
    "responses": {
        200: {
            "description": "Lấy chi tiết đề cương thành công",
            "schema": {
                "type": "object",
                "properties": {
                    "syllabus_id": {
                        "type": "integer",
                        "example": 1458
                    },
                    "course_name": {
                        "type": "string",
                        "example": "Kinh tế vi mô"
                    },
                    "file_path": {
                        "type": "string",
                        "example": "uploads/syllabus/414023_-_Kinh_te_vi_mo.docx"
                    },
                    "file_type": {
                        "type": "string",
                        "example": "docx"
                    },
                    "ai_summary": {
                        "type": "string",
                        "example": "Học phần cung cấp kiến thức nền tảng về kinh tế vi mô..."
                    },
                    "learning_path": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "Chương 1: Tổng quan kinh tế vi mô"
                        }
                    },
                    "outcomes": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "Hiểu được quy luật cung cầu"
                        }
                    },
                    "status": {
                        "type": "string",
                        "example": "Published"
                    }
                }
            }
        },
        404: {
            "description": "Không tìm thấy đề cương hoặc đề cương chưa được publish",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Syllabus not found"
                    }
                }
            }
        },
        401: {
            "description": "Chưa đăng nhập hoặc token không hợp lệ"
        }
    }
})
def get_published_syllabus(syllabus_id):

    syllabus = (
        db.session.query(SyllabusModel, Course)
        .join(Course, SyllabusModel.course_id == Course.course_id)
        .filter(
            SyllabusModel.syllabus_id == syllabus_id,
            SyllabusModel.status == "Published"
        )
        .first()
    )

    if not syllabus:
        return jsonify({"error": "Syllabus not found"}), 404

    s, c = syllabus

    return jsonify({
        "syllabus_id": s.syllabus_id,
        "course_name": c.course_name,
        "file_path": s.file_path,
        "file_type": s.file_path.split(".")[-1],
        "status": s.status
    })
