from enum import Enum


class EduStatus(str, Enum):
    """Enumeration represents **educational status**."""

    SECONDARY = 'Випускник ЗСЗО'
    SECONDARY_PAST = 'Випускник ЗСЗО минуліх років'
    SECONDARY_FOREIGN = 'Випускник ЗСЗО іншої держави'

    PROFESSIONAL_STUDENT = 'Учень (слухач) ЗПО (ЗПТО)'
    HIGHER_STUDENT = 'Студент ВНЗ'
