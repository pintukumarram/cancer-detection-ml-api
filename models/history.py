from models import db

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Linking to the User model
    cancer_type = db.Column(db.String(100), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    prediction_result = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship("User", back_populates="history_entries")

    def __repr__(self):
        return f"<History {self.id} - {self.cancer_type}: {self.prediction_result}>"
