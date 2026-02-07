from flask import Blueprint, jsonify, request, g
from flasgger import swag_from
from werkzeug.utils import secure_filename
from services.syllabus_service import SyllabusService
from infrastructure.unit_of_work import UnitOfWork
from services.revise_syllabus_service import ReviseSyllabusService
from flask_jwt_extended import get_jwt_identity
from api.middleware import jwt_required
from api.role_required import require_role
from infrastructure.models.course_model import Course
from infrastructure.models.syllabus_model import SyllabusModel
from infrastructure.databases.db import db
import os


bp = Blueprint("syllabus", __name__)

UPLOAD_FOLDER = "uploads/syllabus"
@bp.route("/upload", methods=["POST"])
@jwt_required()
@require_role("LECTURER")
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Upload syllabus file",
    "description": "Lecturer uploads syllabus file (PDF, DOCX)",
    "security": [{"BearerAuth": []}],
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "name": "file",
            "in": "formData",
            "type": "file",
            "required": True,
            "description": "Syllabus file (PDF or DOCX)"
        },
        {
            "name": "course_id",
            "in": "formData",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {
            "description": "Upload success"
        },
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})

def upload_syllabus():

    file = request.files.get("file")
    course_id = request.form.get("course_id")

    if not file or not course_id:
        return jsonify({"error": "Missing file or course_id"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)

    # 👉 ĐƯỜNG DẪN LƯU FILE (dùng nội bộ)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(save_path)

    # 👉 ĐƯỜNG DẪN TRẢ VỀ CHO FRONTEND (URL RELATIVE)
    file_path = f"uploads/syllabus/{filename}"

    service = SyllabusService(UnitOfWork())
    syllabus = service.create_syllabus(
        course_id=int(course_id),
        file_path=file_path,          # ✅ CHUẨN
        lecturer_id=g.user["user_id"]
    )

    return jsonify({
        "syllabus_id": syllabus.syllabus_id,
        "file_path": file_path,
        "message": "Upload syllabus successfully"
    }), 200
@bp.route("/submit", methods=["POST"])
@jwt_required()
@require_role("LECTURER")
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Submit syllabus for review",
    "description": "Lecturer submits syllabus for HOD review",
    "security": [
        {"BearerAuth": []}
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
                        "example": 721
                    }
                },
                "required": ["syllabus_id"]
            }
        }
    ],
    "responses": {
        200: {"description": "Submit successfully"},
        400: {"description": "Submit failed"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})
def submit_syllabus():

    data = request.get_json()
    syllabus_id = data.get("syllabus_id")

    if not syllabus_id:
        return jsonify({"error": "syllabus_id is required"}), 400

    service = SyllabusService(UnitOfWork())

    service.submit_syllabus(
        syllabus_id=int(syllabus_id),
        lecturer_id=g.user["user_id"]   # 🔥 cùng token
    )

    return jsonify({"message": "Submit syllabus successfully"})

    


@bp.route("/update", methods=["PUT"])
@jwt_required()
@require_role("LECTURER")
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Update syllabus file",
    "description": "Lecturer updates syllabus by uploading a new file",
    "consumes": ["multipart/form-data"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "file",
            "in": "formData",
            "type": "file",
            "required": True,
            "description": "Updated syllabus file (PDF/DOCX)"
        },
        {
            "name": "syllabus_id",
            "in": "formData",
            "type": "integer",
            "required": True,
            "example": 12
        }
    ],
    "responses": {
        200: {"description": "Update syllabus successfully"},
        400: {"description": "Update failed"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})
def update_syllabus():

    file = request.files.get("file")
    syllabus_id = request.form.get("syllabus_id")

    if not file or not syllabus_id:
        return jsonify({"error": "Missing file or syllabus_id"}), 400

    filename = secure_filename(file.filename)
    save_path = f"uploads/{filename}"
    file.save(save_path)

    service = ReviseSyllabusService(UnitOfWork())

    try:
        service.update_syllabus_file(
            syllabus_id=int(syllabus_id),
            file_path=save_path,
            lecturer_id=g.user["user_id"]
        )
        return jsonify({"message": "Syllabus updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/resubmit", methods=["POST"])
@jwt_required()
@require_role("LECTURER")
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Resubmit syllabus for review",
    "description": "Lecturer resubmits syllabus after revision",
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
                        "example": 12
                    }
                },
                "required": ["syllabus_id"]
            }
        }
    ],
    "responses": {
        200: {"description": "Resubmit successfully"},
        400: {"description": "Resubmit failed"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
})
def resubmit_syllabus():
    data = request.json

    service = ReviseSyllabusService(UnitOfWork())

    try:
        service.resubmit_syllabus(
            syllabus_id=data["syllabus_id"],
            lecturer_id=g.user["user_id"]
        )
        return jsonify({"message": "Resubmit successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/list", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Syllabus"],
    "summary": "Lấy danh sách đề cương của giảng viên",
    "description": "Giảng viên đăng nhập lấy danh sách đề cương của mình",
    "security": [{"BearerAuth": []}],
    "responses": {
        200: {
            "description": "Danh sách đề cương",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "course_code": {"type": "string", "example": "CS101"},
                        "course_name": {"type": "string", "example": "Lập trình Python"},
                        "version": {"type": "string", "example": "v2"},
                        "status": {"type": "string", "example": "PENDING"},
                        "created_at": {"type": "string", "example": "01/02/2026"}
                    }
                }
            }
        },
        401: {
            "description": "Chưa đăng nhập hoặc token không hợp lệ"
        }
    }
})
def list_syllabus():
    if not g.user:
        return jsonify({"error": "Unauthorized"}), 401

    role = g.user.get("role_code")
    user_id = g.user["user_id"]

    query = (
        db.session.query(SyllabusModel, Course)
        .outerjoin(Course, SyllabusModel.course_id == Course.course_id)
    )

    # 🔹 GIẢNG VIÊN → chỉ thấy đề cương của mình
    if role == "LECTURER":
        query = query.filter(
            SyllabusModel.lecturer_id == user_id
    )

    # 🔹 HOD → thấy TẤT CẢ đề cương cần duyệt
    elif role == "HOD":
        query = query.filter(
            SyllabusModel.status.in_([
                "PendingReview",
                "PENDING_REVIEW",
                "PENDING"
            ])
        )
    elif role == "ACADEMIC_AFFAIRS":
        query = query.filter(
            SyllabusModel.status.in_([
                "HodApproved",            
            ])
        )

    elif role == "PRINCIPAL":
        query = query.filter(
            SyllabusModel.status.in_([
                "AcademicApproved",
            
            ])
        )
    # 👉 sắp xếp để đề cương mới lên trên
    syllabi = query.order_by(
        SyllabusModel.create_date.desc()
    ).all()

    return jsonify([
        {
            "id": s.syllabus_id,
            "course_code": c.course_code if c else "",
            "course_name": c.course_name if c else "",
            "version": f"v{s.version_number}",
            "status": s.status,
            "created_at": s.create_date.strftime("%d/%m/%Y")
        }
        for s, c in syllabi
    ])

