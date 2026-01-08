from infrastructure.databases.mssql import session
from infrastructure.models.course_model import Course
from infrastructure.models.syllabus_model import Syllabus

course = session.query(Course).first()

print(course)
print(course.syllabus)
