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

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)
    init_mssql(app)
    setup_middleware(app)
    register_routes(app)
    init_db(app)

    return app
