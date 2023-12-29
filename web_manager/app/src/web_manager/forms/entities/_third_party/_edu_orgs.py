from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional

from data_lib.model import Territory, EduOrgType, EduSupervisor
from web_manager.forms._validators import IdentityValidator


# Define public visible members
__all__ = ['EduOrgTypeForm', 'EduSupervisorForm', 'EduOrganizationForm']


class EduOrgTypeForm(FlaskForm):
    """`FlaskForm` serves **educational organizations type** entity data input."""

    id = IntegerField('Type id', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('Type name', validators=[InputRequired()])


class EduSupervisorForm(FlaskForm):
    """`FlaskForm` serves **educational organization supervisor** entity data input."""

    id = IntegerField('Supervisor organization id', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('Supervisor organization name', validators=[InputRequired()])


class EduOrganizationForm(FlaskForm):
    """`FlaskForm` serves **educational organization** entity data input."""

    id = IntegerField('Organization id', render_kw={'readonly': True}, validators=[Optional()])

    name = StringField('Organization name', validators=[InputRequired()])
    location_terr_id = IntegerField('Location territory id', validators=[Optional(), IdentityValidator(Territory)])
    type_id = IntegerField('Organization type id', validators=[Optional(), IdentityValidator(EduOrgType)])
    supervisor_id = IntegerField('Supervisor organization id', validators=[Optional(), IdentityValidator(EduSupervisor)])
