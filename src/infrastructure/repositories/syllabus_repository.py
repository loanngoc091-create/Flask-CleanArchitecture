from infrastructure.models.syllabus_model import SyllabusModel
from domain.models.syllabus import Syllabus
from infrastructure.models.course_model import Course
from sqlalchemy import or_, func


class SyllabusRepository:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, syllabus_id: int) -> Syllabus | None:
        model = (
            self.session
            .query(SyllabusModel)
            .filter_by(syllabus_id=syllabus_id)
            .first()
        )

        if not model:
            return None

        # ✅ mapping ORM → domain
        return Syllabus(
            syllabus_id=model.syllabus_id,
            version_number=model.version_number,
            status=model.status,
         )
    def add(self, syllabus: Syllabus):

        model = SyllabusModel(
            version_number=syllabus.version_number,
            status=syllabus.status,
            course_id=syllabus.course_id,
             file_path=syllabus.file_path,
             lecturer_id=syllabus.lecturer_id 
        )

        self.session.add(model)
        self.session.flush()

        syllabus.syllabus_id = model.syllabus_id
        
    def update_file(self, syllabus_id: int, file_path: str, status: str):
        model = (
            self.session
            .query(SyllabusModel)
            .filter_by(syllabus_id=syllabus_id)
            .first()
        )

        if not model:
            raise Exception("Syllabus not found")

        model.file_path = file_path
        model.status = status

    def update_status(self, syllabus_id: int, status: str):
        model = (
            self.session
            .query(SyllabusModel)
            .filter(SyllabusModel.syllabus_id == syllabus_id)
            .first()
        )

        if not model:
            raise Exception("Syllabus not found")

        model.status = status

    def find_by_keyword(self, keyword: str):
        return (
            self.session.execute(
                """
                SELECT * FROM syllabi
                WHERE subject_name LIKE :kw
                """
                ,
                {"kw": f"%{keyword}%"}
            ).fetchall()
        )
    
    def save_subscription(self, student_id, syllabus_id):
        self.session.execute(
            """
            INSERT INTO subscriptions(student_id, syllabus_id)
            VALUES (:sid, :syllabus)
            """,
            {"sid": student_id, "syllabus": syllabus_id}
        )
    
    def save_feedback(self, student_id, syllabus_id, content):
        self.session.execute(
            """
            INSERT INTO feedback(student_id, syllabus_id, content)
            VALUES (:sid, :syllabus, :content)
            """,
            {
                "sid": student_id,
                "syllabus": syllabus_id,
                "content": content
            }
        )

    def get_published(self):
        rows = (
            self.session
            .query(
                SyllabusModel.syllabus_id,
                SyllabusModel.status,
                Course.course_name.label("course_name"),
                Course.course_code.label("course_code")
            )
            .join(Course, Course.course_id == SyllabusModel.course_id)
            .filter(SyllabusModel.status == "Published")
            .all()
        )

        return [
            {
                "syllabus_id": r.syllabus_id,
                "status": r.status,
                "course_name": r.course_name,
                "course_code": r.course_code
            }
            for r in rows
        ]

    def get_published_detail(self, syllabus_id):
      result = (
            self.session
            .query(SyllabusModel)
            .join(Course)
            .filter(
                SyllabusModel.syllabus_id == syllabus_id,
                SyllabusModel.status == "Published"
            )
            .first()
        )

      if not result:
            return None


      file_path = result.file_path

      return {
            "syllabus_id": result.syllabus_id,
            "status": result.status,
            "file_path": file_path,
            "file_type": (
                file_path.split(".")[-1].lower()
                if file_path
                else None
            )
        }

    def search_published(self, keyword=None, major=None, semester=None):
        query = (
            self.session.query(SyllabusModel, Course)
            .join(Course, SyllabusModel.course_id == Course.course_id)
            .filter(SyllabusModel.status == "Published")
        )

        # 🔍 search theo keyword (tên + mã học phần)
        if keyword:
            keyword = f"%{keyword.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Course.course_name).like(keyword),
                    func.lower(Course.course_code).like(keyword)
                )
            )

        # 🎓 lọc theo ngành (nếu có)
        if major:
            query = query.filter(Course.major == major)

        # 📅 lọc theo học kỳ (nếu có)
        if semester:
            query = query.filter(Course.semester == semester)

        results = query.all()

        return [
            {
                "syllabus_id": s.syllabus_id,
                "course_name": c.course_name,
                "course_code": c.course_code,
                "status": s.status
            }
            for s, c in results
        ]
