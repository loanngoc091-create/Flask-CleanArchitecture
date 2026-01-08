from infrastructure.databases.mssql import SessionLocal
from infrastructure.models.syllabus_model import Syllabus
import infrastructure.models

db = SessionLocal()

syllabus = db.query(Syllabus).first()

if syllabus:
    print("Syllabus:", syllabus.syllabus_id)
    print("CLOs:", syllabus.clos)
else:
    print("No syllabus found")
