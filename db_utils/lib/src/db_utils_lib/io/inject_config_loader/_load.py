from collections.abc import Mapping, MutableMapping
from os import PathLike
from typing import Any, Literal

from copy import copy as do_copy

import marshmallow

from db_utils_lib.io.filetools import markups

from db_utils_lib.db.csv_inject import Config, Source, SourceFile, SourceTyping, SourceTreatment

import yaml
import json

from ._schemas import RootConfigSchema, SourceSpecificsSchema


# noinspection PyPep8Naming
class loadconfig:
    """
    Utility methods, allows to easily assemble `csv_inject.Config`
    instance with all nested instances from configuration file in the easiest way.
    """

    # ------ Pre-assembled `marshmallow` schemas

    # `marshmallow` `Schema` for standalone source specifics file
    _STANDALONE_SOURCE_SPECIFICS_SCHEMA = SourceSpecificsSchema()

    # `marshmallow` `Schema` for root injection config file
    _CONFIG_ROOT_SCHEMA = RootConfigSchema(context={'supported_markups': ['yaml', 'json']})

    # ------ Loading public methods

    @staticmethod
    def from_file(file: str | bytes | PathLike[str] | PathLike[bytes] | int,
                  markup: Literal['yaml', 'json'] = None,
                  encoding: str | None = None) -> Config:
        """
        Loads injection configuration from file (files).

        :param file: path to file
        :param markup: file markup (`'json'` or `'yaml'`) - if not specified - will be extracted form file extension
        :param encoding: file encoding literal (optional)

        :raise ValueError: if `markup` not specified by argument & it is unable to extract it from file extension /
                           specified implicitly or extracted markup literal is not supported  or unknown /
                           root file or any of related files markup parsing failed /
                           root file or any of related files content validation failed
        :raise OSError: if file root or any of related files loading failed

        :return: `csv_inject.Config` instance
        """

        # Handle markup literal
        if markup is None:

            # Get markup from file extension
            markup, _ = markups.markup_from_path(file)

            # Check extension existing
            if markup is None:
                raise ValueError(
                    "File 'markup' was not specified implicitly and can not be extracted from file extension."
                )

        # Validate possible markup
        if markup not in ('yaml', 'json'):
            raise ValueError(
                f"Unknown file markup {markup}. If markup was not specified by 'markup' parameter, "
                f"there are probability of incorrect markup recognition. Try to specify 'markup' implicitly."
            )

        # Open file & read data using markup-specific load function
        with open(file, mode='r', encoding=encoding) as config_file:
            try:
                if markup == 'yaml':
                    data = yaml.safe_load(config_file)
                else:
                    data = json.load(config_file)

            # Reraise unified ValueError instead of markup-specific if caught
            except (yaml.YAMLError, json.JSONDecodeError) as e:
                raise ValueError(*e.args) from e

        # Call dict loader
        return loadconfig.from_dict(data)

    @staticmethod
    def from_yaml(stream) -> Config:
        """
        Loads injection configuration from stream in `yaml` markup.

        :param stream: stream or string to read from

        :raise ValueError: if current stream or any of related files markup parsing failed /
                           root or any of related files content validation failed
        :raise OSError: if any of related files loading failed

        :return: `csv_inject.Config` instance
        """

        # Load data from stream to dict using `yaml.safe_load()` function
        try:
            data = yaml.safe_load(stream)

        # Reraise unified ValueError instead of markup-specific if caught
        except yaml.YAMLError as e:
            raise ValueError(*e.args) from e

        # Call dict loader :)
        return loadconfig.from_dict(data)

    @staticmethod
    def from_json(stream) -> Config:
        """
        Loads injection configuration from stream in `json` markup.

        :param stream: stream or string to read from

        :raise ValueError: if current stream or any of related files markup parsing failed /
                           root or any of related files content validation failed
        :raise OSError: if any of related files loading failed

        :return: `csv_inject.Config` instance
        """

        # Load data from stream to dict using `json.load()` function
        try:
            data = json.loads(stream) if type(stream) is str or type(stream) is bytes else json.load(stream)

        # Reraise unified ValueError instead of markup-specific if caught
        except json.JSONDecodeError as e:
            raise ValueError(*e.args) from e

        # Call dict loader :)
        return loadconfig.from_dict(data)

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> Config:
        """
        Loads injection configuration from data mapping.

        :param data: data mapping to load from

        :raise ValueError: if any of related files markup parsing failed /
                           root or any of related files content validation failed
        :raise OSError: if any of related files loading failed

        :return: `csv_inject.Config` instance
        """

        # Validate input `data` dict content, extract config & sources data
        try:
            config_data, sources_data = loadconfig._CONFIG_ROOT_SCHEMA.load(data)

        # Reraise unified ValueError instead of `marshmallow` `ValidationError` if caught
        except marshmallow.ValidationError as e:
            raise ValueError(*e.args) from e

        # Load all sources to list using `_load_source()` method and previously extracted data
        sources = {
            source_id: loadconfig._load_source(local_data=local_data, file_info=file_info, copy=False)
            for source_id, (local_data, file_info) in sources_data.items()
        }

        # Initialize `csv_inject.Config` instance & return
        return Config(**config_data, sources=sources)

    # ------ Protected auxiliary methods

    @staticmethod
    def _append_missing_keys(target_: Mapping | MutableMapping = None, source_: Mapping = None, *,
                             copy_target: bool = False, dict_target: bool = False,
                             copy_source: bool = False, dict_source: bool = False):
        """
        Updates `target_` mapping with key-values from `source_` mapping
        which keys are not presented in `target_`.

          If `target_` is None will return `source_` ot its copy.

        :param target_: target mapping to update
        :param source_: source mapping to take data from
        :param copy_target: whether to copy `target_` mapping as it is if provided (`False` by default)
        :param copy_source: whether to copy `source_` mapping as it is if it will be returned (`False` by default)
        :param dict_target: whether to copy `target_` mapping to dict if provided (`False` by default)
        :param dict_source: whether to copy `source_` mapping to dict it will be returned (`False` by default)

        :return: updated `target_` or its copy / `source_` or its copy
        """

        # Return `source_` or its copy if `target_` missing
        if target_ is None:
            return do_copy(source_) if copy_source else dict(source_) if dict_source else source_

        # Copy `target_` if needed
        target_ = do_copy(target_) if copy_target else dict(target_) if dict_target else target_

        # Update `target_` if possible
        if source_ is not None:
            target_.update([(key, value) for key, value in source_.items() if key not in target_])

        return target_

    @staticmethod
    def _load_source(local_data: Mapping[str, Any], file_info: Mapping[str, Any] = None,
                     *, copy: bool = True) -> Source:
        """
        Loads `csv_inject.Source` instance by data extracted from `RootSourceSchema`.

        :param local_data: local data mapping to load from
        :param file_info: standalone specifics file info
        :param copy: whether to copy input `local_data` or mutate existing

        :raise ValueError: if standalone source specifics file markup parsing / content validation failed
        :raise OSError: if standalone source specifics file loading failed

        :return: `csv_inject.Source` instance
        """

        # Extract data sections from `local_data`
        file_kwargs = local_data.get('file')
        typing_kwargs = local_data.get('typing')
        treatment_kwargs = local_data.get('treatment')

        # Handle case if standalone source specifics file defined
        if file_info is not None:

            # Load & validate specifics data from file
            with open(file_info['path'], encoding=file_info.get('encoding')) as specifics_file:
                try:
                    file_data = loadconfig._STANDALONE_SOURCE_SPECIFICS_SCHEMA.load(
                        yaml.safe_load(specifics_file)
                        if file_info['markup'] == 'yaml'
                        else json.load(specifics_file)
                    )

                # Reraise unified ValueError instead of markup-specific parsing error
                # or `marshmallow` `ValidationError` if caught
                except (yaml.YAMLError, json.JSONDecodeError, marshmallow.ValidationError) as e:
                    raise ValueError(f"Exception occurred during '{file_info['path']}' file handling", *e.args) from e

            # Update `file_kwargs` if needed
            file_kwargs = \
                loadconfig._append_missing_keys(file_kwargs, file_data.get('file'), dict_target=copy)

            # Update `typing_kwargs` if needed
            typing_kwargs = \
                loadconfig._append_missing_keys(typing_kwargs, file_data.get('typing'), dict_target=copy)

            # Update `typing_kwargs` if needed
            treatment_kwargs = \
                loadconfig._append_missing_keys(treatment_kwargs, file_data.get('treatment'), dict_target=copy)

        # Assemble & return `csv_inject.Source` instance
        return Source(
            file=SourceFile(**file_kwargs),
            typing=SourceTyping(**typing_kwargs),
            treatment=SourceTreatment(**treatment_kwargs),
            **(dict() if 'properties' not in local_data
               else dict(properties=(do_copy(local_data['properties'])
                                     if copy else local_data['properties'])))
        )
