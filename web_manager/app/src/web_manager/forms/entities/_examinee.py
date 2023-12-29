import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

from data_lib.model import Sex, TerrType, EduStatus, Territory, EduProfile, EduLang, EduOrganization
from web_manager.forms._validators import IdentityValidator


class ExamineeDataForm(FlaskForm):
    """`FlaskForm` serves **examinee information** entity data input."""

    # ------ Identity

    id = IntegerField('Examinee (data) id', render_kw={'readonly': True}, validators=[Optional()])

    # ------ General information

    sex = SelectField('Sex', choices=[(_e, _e.value) for _e in Sex])
    birth_year = IntegerField("Birth year", validators=[
        NumberRange(min=datetime.date.today().year - 100, max=datetime.date.today().year-15)
    ])

    # ------ Registration/residence data

    residence_terr_id = IntegerField("residence territory id", validators=[Optional(), IdentityValidator(Territory)])

    residence_terrtype = SelectField('residence territory type', choices=[(_e, _e.value) for _e in TerrType])

    # ------ Educational class info

    edu_profile_id = IntegerField("educational profile id", validators=[Optional(), IdentityValidator(EduProfile)])

    edu_lang_id = IntegerField("educational language id", validators=[Optional(), IdentityValidator(EduLang)])

    # ------ Educational organization & status

    edu_org_id = IntegerField("eduOrg id", validators=[Optional(), IdentityValidator(EduOrganization)])

    edu_status = SelectField('educational status', choices=[(_e, _e.value) for _e in EduStatus])
