# Import Flask, Flask extensions and core components, needs to be initialized

from flask import Flask, request, g

from flask_bootstrap import Bootstrap5

from web_manager_core.apprepo_sqlalchemy import SQLAlchemyAppRepoBase


# Initialize Flask application & load configuration

app = Flask(__name__)

app.config.from_prefixed_env("WEB_MANAGER")


# Initialize imported extensions and core components

bootstrap = Bootstrap5(app)

repo = SQLAlchemyAppRepoBase(app, config_handler=lambda __cfg: __cfg['REPO'], g_manager_key='repman')


# Import local app-definition modules

from . import endpoints
