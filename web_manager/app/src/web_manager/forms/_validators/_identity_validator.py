from flask_wtf import FlaskForm
from wtforms import ValidationError, Field

from data_lib.repo_abc import RepoDataError, RepoArgumentError
from web_manager import repo


class IdentityValidator:

    __cls: type
    __key: str

    _invert: bool

    def __init__(self, __cls: type, __key: str = 'id', /, invert: bool = False):
        self.__cls = __cls
        self.__key = __key
        self._invert = invert

    def __call__(self, form: FlaskForm, field: Field):

        valid = False

        try:
            valid = repo.manager.exists(self.__cls, {self.__key: field.data})

        except (RepoDataError, RepoArgumentError):
            pass

        if self._invert:
            if valid:
                raise ValidationError("Identity has an invalid format or already taken.")

        else:
            if not valid:
                raise ValidationError("Identity has an invalid format or corresponding instance does not exist.")
