from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DecimalField
from wtforms.validators import NumberRange, InputRequired, Optional, Length

from data_lib.model import TestStatus, DPALevel, Record, Subject, TestPass, TestPoint, EduLang
from web_manager.forms._validators import IdentityValidator


class TestPassForm(FlaskForm):
    """`FlaskForm` serves **test pass information** entity data input."""

    # ------ Identity

    id = IntegerField('Pass id', render_kw={'readonly': True}, validators=[Optional()])

    # ------ Record & subject

    record_id = StringField('Parent record id', validators=[InputRequired(), IdentityValidator(Record), Length(max=64)])
    """Test pass record id."""

    subject_id = IntegerField('Test subject id', validators=[InputRequired(), IdentityValidator(Subject)])

    # ------ Status & additional info

    test_status = SelectField('Test status', choices=[(_e, _e.value) for _e in TestStatus], validators=[InputRequired()])

    super_pass_id = IntegerField('Super-test pass id', validators=[Optional(), IdentityValidator(TestPass)])

    # ------ Test organization details

    test_point_id = IntegerField('Testing point id', validators=[Optional(), IdentityValidator(TestPoint)])

    # ------ Individual details

    test_lang_id = IntegerField('Educational language id', validators=[Optional(), IdentityValidator(EduLang)])

    adapt_scale = IntegerField('Adapt scale', validators=[Optional(), NumberRange(max=10)])

    dpa_level = SelectField('DPA level', choices=[(_e, _e.value) for _e in DPALevel])

    # ------ Test scoring

    score = IntegerField('Raw test score', validators=[Optional(), NumberRange(max=150)])

    score_12 = IntegerField('Converted 12-point score', validators=[Optional(), NumberRange(max=12)])

    score_100 = DecimalField('ZNO test score', validators=[Optional(), NumberRange(max=200)])
