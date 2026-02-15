import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Config (Console Backend for Dev)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # For actual dev without creds, we can print to console:
    # MAIL_BACKEND = 'flask_mail.backends.console.Mail' 
    # But let's keep standard config and just wrap send in try-except for demo robustness
