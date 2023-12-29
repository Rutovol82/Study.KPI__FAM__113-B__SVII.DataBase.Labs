from enum import Enum


class Sex(str, Enum):
    """Enumeration represents examinee **sex**."""

    FEMALE = 'жіноча'
    MALE = 'чоловіча'
