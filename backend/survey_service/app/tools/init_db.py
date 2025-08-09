# tools/init_db.py  (temporary script; you can delete later)
from app.db import engine
from app.models.survey import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print(" Tables created.")
