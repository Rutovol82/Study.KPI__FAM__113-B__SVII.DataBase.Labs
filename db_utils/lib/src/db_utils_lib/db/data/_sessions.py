from contextlib import contextmanager
from dataclasses import dataclass
from typing import Literal

import psycopg2.extensions


@dataclass(frozen=True)
class SessionOpts:
    """`psycopg2` session parameters, supported by `connection.set_session()` method."""

    isolation_level: str | bytes | int | None = None
    readonly: Literal["default", b"default"] | bool | None = None
    deferrable: Literal["default", b"default"] | bool | None = None
    autocommit: bool = None

    @classmethod
    def of(cls, __conn: psycopg2.extensions.connection) -> 'SessionOpts':
        """Initializes new instance of `SessionOpts` class with existing `psycopg2` `connection` object options."""

        return cls(isolation_level=__conn.isolation_level,
                   readonly=__conn.readonly,
                   deferrable=__conn.deferrable,
                   autocommit=__conn.autocommit)

    def apply(self, __conn: psycopg2.extensions.connection):
        """Applies stored options to existing `psycopg2` `connection` object via `set_session()` method."""

        __conn.set_session(isolation_level=self.isolation_level,
                           readonly=self.readonly,
                           deferrable=self.deferrable,
                           autocommit=self.autocommit)

    @contextmanager
    def inject(self, __conn: psycopg2.extensions.connection):
        """
        Contextmanager.
        Applies stored options to existing `psycopg2` `connection` object via `set_session()` method
        within the `with` context (restores previous options on exit).
        """

        backup = SessionOpts.of(__conn)
        self.apply(__conn)

        try:
            yield

        finally:
            backup.apply(__conn)
