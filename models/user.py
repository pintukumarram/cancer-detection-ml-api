from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from models import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="patient")
    specialization = db.Column(db.String(120), nullable=True)
    history_entries = db.relationship(
        "History",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )
    profile_notes_received = db.relationship(
        "ProfileNote",
        foreign_keys="ProfileNote.patient_id",
        back_populates="patient",
        lazy=True,
        cascade="all, delete-orphan",
    )
    profile_notes_authored = db.relationship(
        "ProfileNote",
        foreign_keys="ProfileNote.doctor_id",
        back_populates="doctor",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_patient(self):
        return self.role == "patient"

    @property
    def is_doctor(self):
        return self.role in {"doctor", "lab_expert"}

    def __repr__(self):
        return f"<User {self.username}>"
