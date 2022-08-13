from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CsrfProtect

csrf = CsrfProtect()

db = SQLAlchemy()