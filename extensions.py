from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

db = SQLAlchemy()