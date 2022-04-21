from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Autopsy1@localhost/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# THiS coDe is Used only when we dont use ORMS for connecting to database
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='postgres', user='postgres', password="Autopsy1", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection successful")
#         break

#     except Exception as error:
#         print("Connecting to db failed")
#         print("error:", error)
#         sleep(2)
