from enum import Enum


class TestStatus(str, Enum):
    """Enumeration represents **test pass status**."""

    INVALIDATED = 'Анульовано'
    NOT_APPEARED = 'Не з’явився'
    SCORE_12_ONLY = 'Не обрано 100-200'
    NOT_PASSED = 'Не подолав поріг'
    PASSED = 'Зараховано'
