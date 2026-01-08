from infrastructure.databases.mssql import init_mssql
from infrastructure.models import course_model, program_model, syllabus_model, user_model, approval_model, userrole_model, department_model, plo_model, clo_model, role_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base