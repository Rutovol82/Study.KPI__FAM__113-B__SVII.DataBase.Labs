from enum import Enum


class TerrType(str, Enum):
    """Enumeration represents examinee **residence territory type**."""

    UTS = 'СМТ'
    CITY = 'місто'
    VILLAGE = 'село'
