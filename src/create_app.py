from flask import Flask
from src.config import Config
from src.api.routes import register_routes
from src.infrastructure.databases.mssql import init_mssql
from src.app_logging import setup_logging
from src.api.middleware import setup_middleware
from infrastructure.models.program_model import Program
from infrastructure.models.course_model import Course
from infrastructure.models.user_model import User
from infrastructure.models.syllabus_model import Syllabus
from infrastructure.models.approval_model import Approval
from infrastructure.databases.db import init_db
from src.api.controllers.auth_controller import bp as auth_bp
from src.api.controllers.syllabus_controller import bp as syllabus_bp
from api.controllers.Hod_controller import bp as review_bp
from api.controllers.academic_verification_controller import bp as academic_verify_bp
from api.controllers.principal_controller import bp as principal_bp
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ register ALL module
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(syllabus_bp, url_prefix="/syllabus")
    app.register_blueprint(review_bp, url_prefix="/syllabus")
    app.register_blueprint( academic_verify_bp, url_prefix="/syllabus")
    app.register_blueprint(principal_bp, url_prefix="/principal")

    init_db(app)

    swagger_config = {
        "swagger": "2.0",
        "title": "Syllabus Approval API",
        "version": "1.0.0",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Nhập: Bearer <access_token>"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }

    Swagger(app, config=swagger_config)

    return app
    

