from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
bootstrap = Bootstrap(app)

from app.proftpd import bp as proftpd
app.register_blueprint(proftpd, url_prefix='/proftpd')

from app import views
