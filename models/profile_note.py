from models import db


class ProfileNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    remarks = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    patient = db.relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="profile_notes_received",
    )
    doctor = db.relationship(
        "User",
        foreign_keys=[doctor_id],
        back_populates="profile_notes_authored",
    )
