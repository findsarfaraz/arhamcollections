from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_principal import Principal
principal = Principal()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_mail import Mail
mail = Mail()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

