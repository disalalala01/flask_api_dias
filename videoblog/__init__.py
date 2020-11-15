import os, sys
sys.path.append(os.getcwd())
from flask import Flask
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from videoblog.config import Config
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
import logging


app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()
engine = create_engine(f'postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}')
session_db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session_db.query_property()
jwt = JWTManager()
docs = FlaskApiSpec()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/'
})

from videoblog.models import *
Base.metadata.create_all(bind=engine)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session_db.remove()


from videoblog.main.views import videos
from videoblog.users.views_users import users


app.register_blueprint(videos)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)