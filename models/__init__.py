from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

db = SQLAlchemy()

# Import models here
from models.user import User  # Ensure this line is added
from models.history import History  # Ensure this line is added
from models.profile_note import ProfileNote

def init_db(app):
    db.init_app(app)


def ensure_schema():
    inspector = inspect(db.engine)

    if "user" in inspector.get_table_names():
        user_columns = {column["name"] for column in inspector.get_columns("user")}
        if "role" not in user_columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(30) DEFAULT 'patient'"))
        if "specialization" not in user_columns:
            db.session.execute(text("ALTER TABLE user ADD COLUMN specialization VARCHAR(120)"))

    db.session.commit()
