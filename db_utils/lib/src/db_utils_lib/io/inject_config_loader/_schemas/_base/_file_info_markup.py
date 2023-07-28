from typing import Collection

from marshmallow import validates, validates_schema, ValidationError, post_load
from marshmallow.fields import Str

from db_utils_lib.io.filetools import MarkupsSimplets, markups

from ._file_info import FileInfoSchema


class MarkupFileInfoSchema(FileInfoSchema):
    """
    Base schema to validate basic markup file input credentials and used markup.
    """

    # ------ Service protected fields & getters

    _markups_valid: Collection[str]     # Collection of accepted markups names
    _markups_tool: MarkupsSimplets      # Tool (`MarkupsSimplets` instance) to handle markups

    def _get_valid_markups(self) -> Collection[str]:
        """Returns stored collection of valid markups."""

        if type(self._markups_valid) is str:
            self._markups_valid = self.context[self._markups_valid]

        return self._markups_valid

    # ------ Instantiation method overload

    def __init__(self, *args, markups_valid: str | Collection[str], markups_tool: MarkupsSimplets = None, **kwargs):
        """
        Initializes `MarkupFileInfoSchema` `marshmallow` `Schema`.

        :param args: `marshmallow` `Schema` instantiation `args`
        :param kwargs: `marshmallow` `Schema` instantiation `kwargs`

        :param markups_valid: collection of accepted markups names itself or corresponding key in `context`
        :param markups_tool: tool (`MarkupsSimplets` instance) to handle markups (global `markups` by default)
        """

        super().__init__(*args, **kwargs)

        self._markups_valid = markups_valid
        self._markups_tool = markups_tool if markups_tool is not None else markups

    # ------ Schema fields

    markup = Str(required=False)
    """File markup (will be obtained from file path if not provided)"""

    # ------ Schema handlers

    @validates('markup')
    def _validate_passed_markup(self, markup):
        """Validates is passed markup belongs to specified valid markups."""

        if markup not in self._get_valid_markups():
            raise ValidationError(
                f"'{markup}' is not a valid markup. AcceptedMarkups are: {self._markups_valid}."
                f"If you are currently using valid markup, try to specify markup implicitly using 'markup' field "
                f"if not specified or change file extension to match correct markup standard extensions."
            )

    @validates_schema
    def _validate_path_markup(self, data, **__):
        """Validates file markup extracted from file path if `markup` field value missed."""

        # Check if `markup` is already specified
        if 'markup' in data:
            return

        # Get markup from file extension
        markup, _ = self._markups_tool.markup_from_path(data['path'])

        # Check extension existing
        if markup is None:
            raise ValidationError(
                "File markup was not specified implicitly and can not be extracted from file extension.",
                field_name='markup'
            )

        # Validate possible markup
        self._validate_passed_markup(markup)

    @post_load
    def _extract_markup(self, data, **__):
        """Extracts correct markup if not defined and puts to `markup` field."""

        data['markup'] = data.get('markup') or markups.markup_from_path(data['path'])[0]

        return data
