import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, request
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


def get_locale():
    # This function can be customized to determine the locale based on user preferences
    return request.accept_languages.best_match(app.config["LANGUAGES"])
    # return "es"


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"  # Redirect to login page if not authenticated
# login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")
mail = Mail(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Microblog Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler("logs/microblog.log", maxBytes=10240, backupCount=10)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info("Microblog startup")

from app import errors, models, routes  # noqa: F401 #avoid circular import
