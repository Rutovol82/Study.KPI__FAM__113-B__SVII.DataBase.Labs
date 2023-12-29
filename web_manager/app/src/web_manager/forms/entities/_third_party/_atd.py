from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional
from data_lib.model import Area, Region
from web_manager.forms._validators import IdentityValidator


# Define public visible members
__all__ = ['RegionForm', 'AreaForm', 'TerritoryForm']


class RegionForm(FlaskForm):
    """`FlaskForm` serves **ATD region** entity data input."""
    
    id = IntegerField('Region id', render_kw={'readonly': True}, validators=[Optional()])
    
    name = StringField('Region name', validators=[InputRequired()])


class AreaForm(FlaskForm):
    """`FlaskForm` serves **ATD region area** entity data input."""
    
    id = IntegerField('Area id', render_kw={'readonly': True}, validators=[Optional()])
    
    name = StringField('Area name', validators=[InputRequired()])
    region_id = IntegerField('Region id', validators=[IdentityValidator(Region)])


class TerritoryForm(FlaskForm):
    """`FlaskForm` serves **ATD area territory** entity data input."""
    
    id = IntegerField('territory id', render_kw={'readonly': True}, validators=[Optional()])
    
    name = StringField('territory name', validators=[InputRequired()])
    area_id = IntegerField('area id', validators=[IdentityValidator(Area)])
