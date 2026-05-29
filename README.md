# KancerCare
<img width="1884" height="971" alt="image" src="https://github.com/user-attachments/assets/63f6a442-0702-4bbd-b61b-5b05cab10e77" />
<img width="1897" height="862" alt="image" src="https://github.com/user-attachments/assets/c05558d5-efe8-43b2-8f26-5643ded8b955" />
<img width="1864" height="960" alt="image" src="https://github.com/user-attachments/assets/1ae23fdd-59ac-4d5d-b892-f7e0a65db54a" />
<img width="1910" height="895" alt="image" src="https://github.com/user-attachments/assets/9a0b5fca-5437-4171-be7e-ba2c90c18b26" />





KancerCare is a Flask-based cancer screening and clinical tracking prototype that combines machine learning prediction modules with patient history, doctor/lab review, and role-based access control.

The project has moved beyond a basic model demo and now behaves like an early-stage healthcare product prototype: patients can register, log in, use prediction modules, and review saved history, while doctors and lab experts can review patient records and add remarks, suggestions, and prescription-style notes.

## Current Project Status

This repository is best described as an `MVP / academic healthcare prototype`.

Implemented now:

- Public homepage with polished branding, navigation, footer, and responsive UI
- Role-based authentication for `patient`, `doctor`, and `lab_expert`
- Patient profile, settings, and prediction history
- Doctor/lab expert patient directory and patient review flow
- Doctor/lab expert notes with remarks, suggestions, and prescription fields
- Breast and lung prediction flows with history saving
- UI-ready prostate and colorectal modules
- Loading overlay for slow cold starts on hosts such as Render

Still in progress:

- Prostate backend prediction wiring
- Colorectal backend prediction wiring
- Production-grade audit logs, uploads, notifications, and hospital integrations

## Main Features

- Multi-role login and registration
- RBAC-based dashboards and protected routes
- Cancer prediction modules for:
  - Breast cancer
  - Lung cancer
  - Prostate cancer
  - Colorectal cancer
- Prediction history stored per patient account
- Doctor/lab review workflow
- Account profile and settings pages
- Contact form and polished landing page
- Responsive interface for desktop and mobile

## User Roles

### Patient

- Register and log in
- Access prediction modules
- Save and review prediction history
- View doctor/lab expert notes on their profile/history
- Update account settings

### Doctor / Lab Expert

- Register and log in with role-specific account
- Access patient directory
- Open individual patient profiles
- Read patient prediction history
- Add remarks, suggestions, and prescription-style notes

## Working Modules

### Breast Cancer

- Route: `/breast`
- Prediction route: `/breast/predict`
- Status: Working
- Saves prediction history for logged-in users

### Lung Cancer

- Route: `/lung`
- Prediction route: `/lung/predict`
- Status: Working
- Saves prediction history for logged-in users

### Prostate Cancer

- Route: `/prostate`
- Prediction route: `/prostate/predict`
- Status: UI complete, backend incomplete
- Current route file still has commented model loading and placeholder logic

### Colorectal Cancer

- Route: `/colorectal`
- Prediction route: `/colorectal/predict`
- Status: UI complete, backend incomplete
- Current route file still needs real colorectal model wiring

## Auth And Clinical Tracking Flow

- Unauthenticated users are redirected to login before opening prediction modules
- Patients can use supported prediction modules after login
- Prediction results are stored in the patient history table
- Doctors and lab experts can open `/patients` to review patient records
- Doctors and lab experts can add follow-up notes to patient profiles

## Tech Stack

- Python 3.12
- Flask
- Flask-Login
- Flask-SQLAlchemy
- scikit-learn
- NumPy
- joblib
- SQLite by default
- HTML, CSS, vanilla JavaScript
- Gunicorn for Linux deployment

## Project Structure

```text
KANCERCARE/
|-- app.py
|-- requirements.txt
|-- Procfile
|-- README.md
|-- models/
|   |-- __init__.py
|   |-- user.py
|   |-- history.py
|   |-- profile_note.py
|   |-- breast/
|   |-- lung/
|   |-- prostate/
|   |-- colorectal/
|-- routes/
|   |-- auth_routes.py
|   |-- common_routes.py
|   |-- breast_routes.py
|   |-- lung_routes.py
|   |-- prostate_routes.py
|   |-- colorectal_routes.py
|-- templates/
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- profile.html
|   |-- settings.html
|   |-- history.html
|   |-- doctor_patients.html
|   |-- patient_profile.html
|   |-- breast.html
|   |-- lung.html
|   |-- prostate.html
|   |-- colorectal.html
|   |-- result.html
|   |-- error.html
|   |-- contact.html
|-- static/
|   |-- css/
|   |-- js/
|   |-- images/
|   |-- sounds/
|-- utils/
|   |-- history.py
|   |-- rbac.py
```

## Important Routes

| Route | Purpose | Status |
| --- | --- | --- |
| `/` | Homepage | Working |
| `/login` | Login | Working |
| `/register` | Register | Working |
| `/logout` | Logout | Working |
| `/profile` | Role-aware profile/dashboard | Working |
| `/settings` | Update account details | Working |
| `/history` | Patient prediction history | Working |
| `/patients` | Doctor/lab patient list | Working |
| `/patients/<patient_id>` | Patient profile review page | Working |
| `/patients/<patient_id>/notes` | Add doctor/lab note | Working |
| `/breast` | Breast module | Working |
| `/breast/predict` | Breast prediction | Working |
| `/lung` | Lung module | Working |
| `/lung/predict` | Lung prediction | Working |
| `/prostate` | Prostate module page | Working |
| `/prostate/predict` | Prostate prediction | Incomplete |
| `/colorectal` | Colorectal module page | Working |
| `/colorectal/predict` | Colorectal prediction | Incomplete |
| `/contact` | Contact page | Working |

## Installation

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Development server:

```text
http://127.0.0.1:5000
```

## Deployment

This repository includes a `Procfile` for Gunicorn-based deployment:

```text
web: gunicorn app:app
```

Recommended deployment target:

- Render
- Railway
- Any Linux-based platform that supports Python + Gunicorn

Note:

- Free-tier Render deployments may take time to wake up after inactivity
- A loading overlay has already been added to improve the user experience during cold starts

## Database

The app currently uses SQLite by default:

```python
sqlite:///kancercare.db
```

You can switch to PostgreSQL later by setting `DATABASE_URL` in the environment.

## Known Limitations

- Prostate prediction backend is not fully connected
- Colorectal prediction backend is not fully connected
- `requirements.txt` may need cleanup/revalidation before final deployment, depending on your environment
- The current database setup is suitable for prototype/MVP use, not full hospital production use
- Model trust details such as sensitivity, specificity, and validation reporting are not yet surfaced in the UI
- Real hospital features like report upload, appointment tracking, audit logs, and notifications are not yet implemented

## Suggested Next Upgrades

- Complete prostate prediction wiring
- Complete colorectal prediction wiring
- Add report upload and patient timeline
- Add real assigned doctor mapping
- Add admin panel and audit logs
- Move from SQLite to PostgreSQL for deployment
- Add dedicated Privacy Policy, Terms, and Medical Disclaimer pages
- Document model metrics and training limitations

## Disclaimer

KancerCare is an educational and prototype healthcare project. It is intended for screening support, academic demonstration, and product prototyping only.

It must not be used as a substitute for licensed medical diagnosis, emergency care, or treatment decisions without qualified clinical review.
