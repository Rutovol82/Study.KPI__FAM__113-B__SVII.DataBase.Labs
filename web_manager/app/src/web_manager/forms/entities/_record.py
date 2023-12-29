import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import NumberRange, InputRequired, Optional

from data_lib.model import ExamineeData
from web_manager.forms._validators import IdentityValidator


class RecordForm(FlaskForm):
    """`FlaskForm` serves ** OpenData record ** entity data input."""

    id = StringField('Record OutID', render_kw={'readonly': True}, validators=[Optional()])

    year = IntegerField('Record year', validators=[
        NumberRange(min=2005, max=datetime.date.today().year + 1), InputRequired()
    ])
    examinee_id = IntegerField('Examinee (data) id', validators=[Optional(), IdentityValidator(ExamineeData)])
