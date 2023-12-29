from dataclasses import dataclass

from .. import Sex, TerrType, EduStatus


@dataclass
class ExamineeData:
    """Dataclass represents **examinee information**."""

    # ------ Identity

    id: int
    """Examinee data id."""

    # ------ General information

    sex: Sex = None
    """Examinee sex."""

    birth_year: int = None
    """Examinee birth year."""

    # ------ Registration/residence data

    residence_terr_id: int = None
    """Examinee registration/residence territory id."""

    residence_terrtype: TerrType = None
    """Examinee registration/residence territory type."""

    # ------ Educational class info

    edu_profile_id: int = None
    """Examinee class educational profile id."""

    edu_lang_id: int = None
    """Examinee class educational language id."""

    # ------ Educational organization & status

    edu_org_id: int = None
    """Examinee educational organization id."""

    edu_status: EduStatus = None
    """Examinee educational status"""
