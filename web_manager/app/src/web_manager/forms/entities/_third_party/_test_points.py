from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional

from data_lib.model import Territory
from web_manager.forms._validators import IdentityValidator


# Define public visible members
__all__ = ['TestPointForm']


class TestPointForm(FlaskForm):
    """`FlaskForm` serves **testing point** entity data input."""

    id = IntegerField('Test point ID', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('Test point name', validators=[InputRequired()])
    location_terr_id = IntegerField('Location / Territory ID', validators=[Optional(), IdentityValidator(Territory)])
