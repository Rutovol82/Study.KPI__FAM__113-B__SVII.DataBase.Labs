from collections.abc import Collection, Mapping
from typing import Any

import psycopg2.extensions
import psycopg2.sql as pgsql

from db_utils_lib.db.wrapper import Dumper
from db_utils_lib.db import csv_inject

from importlib import resources

from db_utils_lib.io.argparse import CompileFlag

import re

from .. import queries
from . import db_utils_command

# from loguru import logger
from db_utils_lib.runtimer import runtimer


# Public members definition
__all__ = ['__command__', 'db_injector']


# ------ Command script body

# noinspection PyPep8Naming
class db_injector:
    """'zno-odata' database injector to be used with `db.csv_inject.inject` api."""

    # ------ SQL queries class variables

    # AT entities injection/referencing query pattern (from resources)
    _QUERY_PATTERN_GET_LOCATION                                                                             \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_location.query'))

    # Educational language entity injection/referencing query pattern (from resources)
    _QUERY_PATTERN_GET_EDU_LANG                                                                             \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_edu_lang.query'))
    # Educational profile entity injection/referencing query pattern (from resources)
    _QUERY_PATTERN_GET_EDU_PROFILE                                                                          \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_edu_profile.query'))
    # Educational organization & related entities injection/referencing query pattern (from resources)
    _QUERY_PATTERN_GET_EDU_ORG                                                                              \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_edu_org.query'))

    # Record & examinee entities injection (& related entities injection/referencing) query pattern (from resources)
    _QUERY_PATTERN_INJECT_RECORD_EXAMINEE                                                                   \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__inject_record_examinee.query'))

    # Test point & related entities injection/referencing query pattern (from resources)
    _QUERY_PATTERN_GET_TEST_POINT                                                                           \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_test_point.query'))

    # Test pass entity injection (& related entities injection/referencing) query pattern (from resources)
    _QUERY_PATTERN_INJECT_TEST_DATA                                                                         \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__inject_test_data.query'))

    # Subject ID selection query (from resources)
    _QUERY_GET_SUBJECT                                                                                      \
        = pgsql.SQL(resources.read_text(queries, 'V2_1__get_subject.query'))

    # ------ Regex patterns class variables

    # Property regex fullmatch pattern: matches any property, related to the test pass, extracts test subject code
    _PROP_PATTERN_MATCH_TEST_SUBJECT                                                                        \
        = re.compile(r"^test\$(?P<subject_code>[^\s$]*)\$\S*$")
    # Property regex fullmatch pattern: matches local-level test pass properties, extracts property name without prefix
    _PROP_PATTERN_MATCH_TEST_PROP_NAME                                                                      \
        = re.compile(r"^test\$[^\s$]*\$(?P<property_name>[^\s$]*)(?<!status)(?<!lang)$")
    # Property regex fullmatch pattern: matches subtest properties, extracts current & super pass subject codes
    _PROP_PATTERN_MATCH_TEST_SUB_TEST                                                                       \
        = re.compile(r"^test\$(?P<subject_code>[^\s$]*)\$sub_test\$(?P<super_subject_code>[^\s$]*)$")

    # ------ Query building protected class methods

    @classmethod
    def _query_build_get_location(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds AT entities injection/referencing query
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Define dict for query insertions
        insertions_ = dict()

        # Iterate over necessary args & create corresponding injections
        for arg_ in ['region', 'area', 'territory']:

            # Try to find the corresponding property & build a placeholder
            placeholders_ = tuple(pgsql.Placeholder(prop_) for prop_ in properties_ if prop_.endswith(arg_))

            # Check property exists
            if len(placeholders_) == 0:
                return pgsql.NULL

            # Add placeholder to the insertions
            insertions_[arg_] = placeholders_[0]

        # Build & return the whole query
        return cls._QUERY_PATTERN_GET_LOCATION.format(**insertions_)

    @classmethod
    def _query_build_get_edu_lang(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds educational language entity injection/referencing query
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Try to build placeholder for the only name argument
        name_placeholders_ = tuple(
            pgsql.Placeholder(prop_) for prop_ in properties_ if prop_.endswith("lang")
        )

        # Check if necessary property exists, build & return the query
        return cls._QUERY_PATTERN_GET_EDU_LANG.format(name=name_placeholders_[0])        \
            if len(name_placeholders_) > 0 else pgsql.NULL

    @classmethod
    def _query_build_get_edu_profile(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds educational profile entity injection/referencing query
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Try to build placeholder for the only name argument
        name_placeholders_ = tuple(
            pgsql.Placeholder(prop_) for prop_ in properties_ if prop_.endswith("profile")
        )

        # Check if necessary property exists, build & return the query
        return cls._QUERY_PATTERN_GET_EDU_PROFILE.format(name=name_placeholders_[0])     \
            if len(name_placeholders_) > 0 else pgsql.NULL

    @classmethod
    def _query_build_get_edu_ord(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds educational organization & related entities injection/referencing query
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Check if edu_org can be obtained
        if not any(prop_.endswith('edu$org$name') for prop_ in properties_):
            return pgsql.NULL

        # Build all necessary insertions, build & return the whole query
        return cls._QUERY_PATTERN_GET_EDU_ORG.format(
            **{
                arg_: placeholders_[0] if len(placeholders_) > 0 else pgsql.Literal(None)
                for placeholders_, arg_ in (
                    (
                        tuple(pgsql.Placeholder(prop_) for prop_ in properties_ if prop_.endswith(f"org${suffix_}")),
                        suffix_
                    )
                    for suffix_ in ['name', 'type', 'supervisor']
                )
            },
            location=cls._query_build_get_location([prop_ for prop_ in properties_ if "org$loc$" in prop_])
        )

    @classmethod
    def _query_build_inject_record_examinee(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds record & examinee entities injection (& related entities injection/referencing) query
        using passed property keys for cases dispatch & named placeholders.

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Filter examinee-related properties from the whole collection
        examinee_properties_ = [prop_ for prop_ in properties_ if prop_.startswith("examinee$")]

        # Filter properties for sub-query builders
        examinee_residence_properties_ = [
            prop_ for prop_ in examinee_properties_ if prop_.startswith("examinee$residence$")
        ]
        examinee_edu_org_properties_ = [
            prop_ for prop_ in examinee_properties_ if prop_.startswith("examinee$edu$org$")
        ]
        examinee_edu_class_properties_ = [
            prop_ for prop_ in examinee_properties_ if prop_.startswith("examinee$edu$class$")
        ]

        # Build all necessary insertions, build & return the whole query
        return cls._QUERY_PATTERN_INJECT_RECORD_EXAMINEE.format(
            **{
                arg_: placeholders_[0] if len(placeholders_) > 0 else pgsql.Literal(None)
                for placeholders_, arg_ in (
                    (
                        tuple(pgsql.Placeholder(prop_) for prop_ in examinee_properties_ if prop_.endswith(suffix_)),
                        f"examinee_{suffix_.replace('$', '_')}"
                    )
                    for suffix_ in ['sex', 'birth_year', 'residence_terrtype', 'edu$status']
                )
            },
            examinee_residence=cls._query_build_get_location(examinee_residence_properties_),
            examinee_edu_lang=cls._query_build_get_edu_lang(examinee_edu_class_properties_),
            examinee_edu_profile=cls._query_build_get_edu_profile(examinee_edu_class_properties_),
            examinee_edu_org=cls._query_build_get_edu_ord(examinee_edu_org_properties_)
        )

    @classmethod
    def _query_build_get_test_point(cls, properties_: Collection[str]) -> pgsql.Composable:
        """
        Builds test point & related entities injection/referencing query pattern (from resources)
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: built query as :class:`pgsql.Composable`
        """

        # Try to build placeholder for the only name argument
        name_placeholders_ = tuple(pgsql.Placeholder(prop_) for prop_ in properties_ if prop_.endswith("point$name"))

        # Check if the name property exists
        if len(name_placeholders_) == 0:
            return pgsql.NULL

        # Build & return the whole query
        return cls._QUERY_PATTERN_GET_TEST_POINT.format(
            name=name_placeholders_[0],
            location=cls._query_build_get_location([prop_ for prop_ in properties_ if "point$loc$" in prop_])
        )

    @classmethod
    def _query_build_get_test_super_pass(cls, properties_: Collection[str]):
        """
        Builds super pass property placeholder (or returns :class:`pgsql.NULL`) using passed property keys.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :return: super pass subject ID :class:`pgsql.Placeholder` or :class:`pgsql.NULL`
        """

        # Get all properties, matches the subtest property pattern
        super_pass_prop_matches_ = tuple(
            filter(None, map(cls._PROP_PATTERN_MATCH_TEST_SUB_TEST.fullmatch, properties_))
        )

        # Check if necessary property, build & return the query
        return pgsql.Placeholder(
            cls._subject_code_to_test_pass_id_prop(super_pass_prop_matches_[0].groupdict()['super_subject_code'])
        ) if len(super_pass_prop_matches_) > 0 else pgsql.NULL

    @classmethod
    def _query_build_inject_test_data(cls, properties_: Collection[str], subject_code: str) -> pgsql.Composable:
        """
        Builds test pass entity injection (& related entities injection/referencing) query
        using passed property keys for cases dispatch & named placeholders.

          ----

        Note: `properties_` :class:`Collection` should not contain more than one set of suitable properties

        :param properties_: property keys :class:`Collection`
        :param subject_code: current test pass subject code
        :return: built query as :class:`pgsql.Composable`
        """

        # Get all properties, matches the local-level test property pattern
        local_prop_matches_ = list(filter(None, map(cls._PROP_PATTERN_MATCH_TEST_PROP_NAME.fullmatch, properties_)))

        # Build all necessary insertions, build & return the whole query
        return cls._QUERY_PATTERN_INJECT_TEST_DATA.format(
            subject_id=pgsql.Placeholder(cls._subject_code_to_subject_id_prop(subject_code)),
            test_status=pgsql.Placeholder(f'test${subject_code}$status'),
            super_pass_id=cls._query_build_get_test_super_pass(properties_),
            test_point_id=cls._query_build_get_test_point([prop_ for prop_ in properties_ if "point$" in prop_]),
            test_lang_id=cls._query_build_get_edu_lang(properties_),
            other_columns=pgsql.SQL(',').join(
                pgsql.Identifier(match_.groupdict()['property_name']) for match_ in local_prop_matches_
            ),
            other_values_placeholders=pgsql.SQL(',').join(
                pgsql.Placeholder(match_.string) for match_ in local_prop_matches_
            )
        )

    # ------ Auxiliary properties handling class methods

    @classmethod
    def _subject_code_to_subject_id_prop(cls, subject_code: str) -> str:
        """
        For the given subject code returns the corresponding subject id property key,
        as will be presented in `Subjects_` mapping
        """

        return f'subjects${subject_code}$id'

    @classmethod
    def _subject_code_to_test_pass_id_prop(cls, subject_code: str) -> str:
        """
        For the given subject code returns the corresponding pass id property key,
        as will be presented in the insertion properties mapping
        """

        return f'test${subject_code}$pass$id'

    @classmethod
    def _build_inject_test_data_queries(cls, properties_: Collection[str]) -> Mapping[str, pgsql.Composable]:
        """
        Builds test pass entity injection (& related entities injection/referencing) queries for all tests
        referenced in the `properties_` as the subject code to :class:`pgsql.Composable` query :class:`Mapping`.

        The keys will be ordered to satisfy all cross-test references.

        :param properties_: property keys :class:`Collection`
        :return: subject code to :class:`pgsql.Composable` query :class:`Mapping`

        :raises RuntimeError: if circular dependency between tests detected
        """

        # Init list for codes of all subjects mentioned in properties_
        subjects_ = list()

        # Iterate over properties, matches the subtest property pattern
        # & add related subject codes to the subjects_ list in the correct order
        for sub_test_prop_match_ in filter(None, map(cls._PROP_PATTERN_MATCH_TEST_SUB_TEST.fullmatch, properties_)):

            # Get subject and super-subject codes from the match
            subject_code = sub_test_prop_match_.groupdict()['subject_code']
            super_subject_code = sub_test_prop_match_.groupdict()['super_subject_code']

            # Check existence & get indexes for both subject codes in the subjects_ list
            subject_index = subjects_.index(subject_code) if subject_code in subjects_ else None
            super_subject_index = subjects_.index(super_subject_code) if super_subject_code in subjects_ else None

            # Insert both subject codes into the subjects_ list in the correct order
            if subject_index is None:
                if super_subject_index is None:
                    subjects_.append(super_subject_code)

                subjects_.append(subject_code)

            else:
                if super_subject_index is None:
                    subjects_.insert(subject_index, subject_code)

                elif super_subject_index > subject_index:
                    raise RuntimeError(f'Circular dependency detected between tests for subjects'
                                       f'"{subject_code}" and "{super_subject_code}"')

        # Init dict for split by subject properties
        split_properties_ = {subject_code: list() for subject_code in subjects_}

        # Iterate over all properties, matches the test property pattern and add to the split dict
        for test_prop_match_ in filter(None, map(cls._PROP_PATTERN_MATCH_TEST_SUBJECT.fullmatch, properties_)):

            # Get subject code from the match
            subject_code = test_prop_match_.groupdict()['subject_code']

            # Try to get the list for matched subject if exists
            subject_test_properties_ = split_properties_.get(subject_code, None)

            # Add matched subject to the dict if not in dict yet
            if subject_test_properties_ is None:
                subject_test_properties_ = list()
                split_properties_[subject_code] = subject_test_properties_

            # Append property to the subject list
            subject_test_properties_.append(test_prop_match_.string)

        # Return split properties dict
        return {
            subject_code: cls._query_build_inject_test_data(test_properties_, subject_code)
            for subject_code, test_properties_ in split_properties_.items()
        }

    @classmethod
    def _test_data_exist(cls, data_: Mapping[str, Any], subject_code: str) -> bool:
        """
        Checks if test pass data for subject with passed `subject_code`
        really exists in passed `data_` :class:`Mapping`

        :param data_: property key-to-value :class:`Mapping`
        :param subject_code: target test pass subject code
        :return: `True` if test pass data exists, otherwise `False`
        """

        return data_[f'test${subject_code}$subject$name'] is not None

    # ------ Protected fields

    # Last passed block source id
    _last_source_id: str = None

    # Code-based property names to IDs mapping for subjects defined in the last passed block source
    _last_source_subjects: Mapping[str, int] = None

    # Queries formatted for the currently passing source data blocks
    _fmt_query_inject_record_examinee: pgsql.Composable = None
    _fmt_queries_inject_testing_data: Mapping[str, pgsql.Composable] = None

    # ------ `__call__()` method

    def __call__(self, __conn: psycopg2.extensions.connection, block_: tuple[Collection[Mapping[str, Any]], str]):
        """
        Injects data block into 'zno-odata' database.

        :param __conn: `psycopg2.connection` instance, represents active database connection
        :param block_: data block tuple emitted by injection emitter
        """

        data_, source_id_ = block_  # Unpack block tuple

        # Check if source id changed - if yes - rebuild queries, update subjects and store new id
        if source_id_ != self._last_source_id:

            # Store the new source id
            self._last_source_id = source_id_

            # Extract property keys from the data
            properties_ = next(iter(data_)).keys()

            # Rebuild injection queries
            self._fmt_query_inject_record_examinee = self._query_build_inject_record_examinee(properties_)
            self._fmt_queries_inject_testing_data = self._build_inject_test_data_queries(properties_)

            # Update subjects mapping for the current source subjects
            with __conn.cursor() as cursor_:

                # Define function, provides subject id querying
                def subject_id(code_: str) -> int:
                    cursor_.execute(self._QUERY_GET_SUBJECT, dict(code=code_))
                    return cursor_.fetchone()[0]

                # Re-build subjects mapping
                self._last_source_subjects = {
                    self._subject_code_to_subject_id_prop(subject_code): subject_id(subject_code)
                    for subject_code in self._fmt_queries_inject_testing_data.keys()
                }

        # Inject data to database record-by-record
        with __conn.cursor() as cursor_:
            for rec_ in data_:

                # Inject records, examinees data and related instances
                cursor_.execute(self._fmt_query_inject_record_examinee, rec_)

                # Create the modifiable copy of the record & update it with extra properties
                rec_ext_ = dict(rec_)
                rec_ext_.update(self._last_source_subjects)

                # Inject testing data subject-by-subject
                for subject_code, inject_query_ in self._fmt_queries_inject_testing_data.items():

                    # Check if the record contain test data for the current subject
                    if not self._test_data_exist(rec_, subject_code):
                        continue

                    # Execute insertion & obtain back pass id
                    cursor_.execute(inject_query_, rec_ext_)
                    rec_ext_[self._subject_code_to_test_pass_id_prop(subject_code)] = cursor_.fetchone()[0]

    # ------ `inject()` class method

    @classmethod
    def inject(cls, config: csv_inject.Config, dumper: Dumper, repo: csv_inject.RepositoryInfo,
               cache: csv_inject.CacheInfo = None, mode: int | csv_inject.Mode = 0):
        """
        Run database injection procedure using a `db_injector` as `injector`.

          Just a wrapper for the `db.csv_inject.inject()` ;)

        :param config: current injection configuration as `Config` instance
        :param dumper: `wrapper.Dumper` instance manages database operations
        :param repo: db-side injections info repository specification
        :param cache: local injection data cache specification (optional)
        :param mode: injection `Mode` flags (optional)
        """

        return csv_inject.inject(config=config, dumper=dumper, injector=cls(), repo=repo, cache=cache, mode=mode)


# ------ Command script setup & entry point

@db_utils_command.entry_point(
    command='V2.1__inject',
    description="Injects data into ZNO Open Data database. "
                "Injections configures mainly through the special "
                "injection config files in .yaml format",
    args=[
        ('cfg_path',
         dict(type=str,
              help='Path of injection config .yaml file.')),
        ('--cfg-encoding',
         dict(required=False, type=str, default='utf-8', dest='cfg_encoding',
              help='Injection config .yaml file encoding (UTF-8 by default).')),
        ('--inject-table',
         dict(required=False, type=str, default='injections', dest='inject_table',
              help='Name of table stores information about injections on database side.')),
        (('--mode', '-M'),
         dict(required=False, type=csv_inject.Mode, default=0, action=CompileFlag, dest='mode',
              help='Injection mode flags.'))
    ]
)
def __command__(dumper: Dumper, cfg_path: str, cfg_encoding: str = None,
                inject_table: str = 'injections',
                mode: int | csv_inject.Mode = 0, **__):
    """
    `V2.1__inject` command script entry point.

      Runs database injection procedure.

    :param dumper: `db.wrapper.Dumper` instance manages db operations
    :param cfg_path: path of injection config `.yaml` file
    :param cfg_encoding: injection config .yaml file encoding
    :param inject_table: name of table stores information about injections on the database side
    :param do_init: whether to initialize the database if not exists
    :param mode: injection mode flags
    """

    # Read config file
    from db_utils_lib.io import inject_config_loader
    config = inject_config_loader.loadconfig.from_file(cfg_path, encoding=cfg_encoding)

    # Construct `RepositoryInfo`
    repo = csv_inject.RepositoryInfo(table_name=inject_table)

    # Establish database connection
    with dumper:

        # Run data injection
        with runtimer(__name__ + ' [inject]'):
            db_injector.inject(dumper=dumper, config=config, repo=repo, mode=mode | csv_inject.CACHE_DISABLE)
