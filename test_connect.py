from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pymssql://sa:Aa%40123456@localhost:1433/FlaskApiDB"
)

try:
    with engine.connect() as conn:
        print("✅ CONNECT OK")
except Exception as e:
    print("❌ ERROR:", e)
