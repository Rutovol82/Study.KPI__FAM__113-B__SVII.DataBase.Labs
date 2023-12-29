import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import NumberRange

from data_lib.model import Sex


class ExamineesQueryForm(FlaskForm):

    sex = SelectField(
        'Examinee Sex',
        choices=[
            (_e, _e.value) for _e in Sex
        ]
    )

    birth_year = IntegerField(
        "Examinee Birth Year",
        validators=[
            NumberRange(min=datetime.date.today().year - 100, max=datetime.date.today().year - 15)
        ]
    )
