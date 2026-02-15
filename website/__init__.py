from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app
