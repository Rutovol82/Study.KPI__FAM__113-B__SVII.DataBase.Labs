from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Optional

# Define public visible members
__all__ = ['EduLangForm', 'EduProfileForm']


class EduLangForm(FlaskForm):
    """`FlaskForm` serves **language accepted to be used in education/testing** entity data input."""

    id = IntegerField('language id', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('language name', validators=[InputRequired()])


class EduProfileForm(FlaskForm):
    """`FlaskForm` serves **educational profile** entity data input."""

    id = IntegerField('profile id', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('profile name', validators=[InputRequired()])
