import os

from flask import Flask, render_template
from flask_login import LoginManager

from models import init_db, db, User, ensure_schema
from routes.auth_routes import auth
from routes.common_routes import common_routes
from routes.breast_routes import breast_routes
from routes.lung_routes import lung_routes
from routes.prostate_routes import prostate_routes
from routes.colorectal_routes import colorectal_routes

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "kancercare-dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///kancercare.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(common_routes)
app.register_blueprint(breast_routes, url_prefix='/breast')
app.register_blueprint(lung_routes, url_prefix='/lung')
app.register_blueprint(prostate_routes, url_prefix='/prostate')
app.register_blueprint(colorectal_routes, url_prefix='/colorectal')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

with app.app_context():
    db.create_all()
    ensure_schema()

if __name__ == '__main__':
    app.run(debug=True)
