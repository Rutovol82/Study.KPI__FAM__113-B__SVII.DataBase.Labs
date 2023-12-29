from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length, Optional

from data_lib.model import Subject
from web_manager.forms._validators import IdentityValidator


class SubjectForm(FlaskForm):
    """`FlaskForm` serves **test subject** entity data input"""

    id = IntegerField('Subject id', render_kw={'readonly': True}, validators=[Optional()])

    code = StringField('Subject code', validators=[Length(max=64), IdentityValidator(Subject, 'code', invert=True)])
    name = StringField('Subject name')
