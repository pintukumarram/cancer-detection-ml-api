from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from models import db, History, User, ProfileNote
from utils.rbac import roles_required


common_routes = Blueprint('common_routes', __name__)


@common_routes.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('common_routes.profile'))


@common_routes.route('/profile')
@login_required
def profile():
    if current_user.is_doctor:
        recent_notes = (
            ProfileNote.query.filter_by(doctor_id=current_user.id)
            .order_by(ProfileNote.created_at.desc())
            .limit(10)
            .all()
        )
        patient_count = User.query.filter_by(role="patient").count()
        return render_template(
            'profile.html',
            user=current_user,
            patient_count=patient_count,
            recent_notes=recent_notes,
        )

    user_history = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).all()
    profile_notes = (
        ProfileNote.query.filter_by(patient_id=current_user.id)
        .order_by(ProfileNote.created_at.desc())
        .all()
    )
    return render_template(
        'profile.html',
        user=current_user,
        history=user_history,
        profile_notes=profile_notes,
    )


@common_routes.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        specialization = request.form.get('specialization', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email:
            flash('Username and email are required.')
            return render_template('settings.html', user=current_user)

        existing_username = User.query.filter(User.username == username, User.id != current_user.id).first()
        existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()

        if existing_username or existing_email:
            flash('That username or email is already in use by another account.')
            return render_template('settings.html', user=current_user)

        if password:
            if password != confirm_password:
                flash('Passwords do not match.')
                return render_template('settings.html', user=current_user)
            current_user.set_password(password)

        current_user.username = username
        current_user.email = email
        current_user.specialization = specialization or None
        db.session.commit()
        flash('Profile settings updated successfully.')
        return redirect(url_for('common_routes.settings'))

    return render_template('settings.html', user=current_user)


@common_routes.route('/history')
@login_required
def history():
    if current_user.is_doctor:
        return redirect(url_for('common_routes.patient_list'))

    user_history = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).all()
    profile_notes = (
        ProfileNote.query.filter_by(patient_id=current_user.id)
        .order_by(ProfileNote.created_at.desc())
        .all()
    )
    return render_template(
        'history.html',
        history=user_history,
        profile_notes=profile_notes,
        user=current_user,
    )


@common_routes.route('/patients')
@login_required
@roles_required('doctor', 'lab_expert')
def patient_list():
    patients = (
        User.query.filter_by(role='patient')
        .order_by(User.username.asc())
        .all()
    )
    return render_template('doctor_patients.html', patients=patients, user=current_user)


@common_routes.route('/patients/<int:patient_id>')
@login_required
@roles_required('doctor', 'lab_expert')
def patient_profile(patient_id):
    patient = User.query.filter_by(id=patient_id, role='patient').first_or_404()
    patient_history = History.query.filter_by(user_id=patient.id).order_by(History.timestamp.desc()).all()
    profile_notes = (
        ProfileNote.query.filter_by(patient_id=patient.id)
        .order_by(ProfileNote.created_at.desc())
        .all()
    )
    return render_template(
        'patient_profile.html',
        patient=patient,
        history=patient_history,
        profile_notes=profile_notes,
        user=current_user,
    )


@common_routes.route('/patients/<int:patient_id>/notes', methods=['POST'])
@login_required
@roles_required('doctor', 'lab_expert')
def add_patient_note(patient_id):
    patient = User.query.filter_by(id=patient_id, role='patient').first_or_404()
    remarks = request.form.get('remarks', '').strip()
    suggestions = request.form.get('suggestions', '').strip()
    prescription = request.form.get('prescription', '').strip()

    if not remarks:
        flash('Remarks are required before submitting a note.')
        return redirect(url_for('common_routes.patient_profile', patient_id=patient.id))

    note = ProfileNote(
        patient_id=patient.id,
        doctor_id=current_user.id,
        remarks=remarks,
        suggestions=suggestions,
        prescription=prescription,
    )
    db.session.add(note)
    db.session.commit()
    flash('Doctor note saved to the patient profile.')
    return redirect(url_for('common_routes.patient_profile', patient_id=patient.id))
