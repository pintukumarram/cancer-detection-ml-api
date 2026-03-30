import json

from flask_login import current_user

from models import db, History


def save_prediction_history(cancer_type, input_data, cancer_prediction, stage_prediction):
    if not current_user.is_authenticated:
        return

    history_entry = History(
        user_id=current_user.id,
        cancer_type=cancer_type,
        input_data=json.dumps(input_data, indent=2),
        prediction_result=f"Cancer: {cancer_prediction}, Stage: {stage_prediction}",
    )
    db.session.add(history_entry)
    db.session.commit()
