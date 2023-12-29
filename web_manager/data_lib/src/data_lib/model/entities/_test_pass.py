from dataclasses import dataclass

import decimal

from .. import TestStatus, DPALevel


@dataclass
class TestPass:
    """Dataclass represents **test pass information**."""

    # ------ Identity

    id: int
    """Test pass id."""

    # ------ Record & subject

    record_id: int
    """Test pass record id."""

    subject_id: int
    """Test pass subject id."""

    # ------ Status & additional info

    test_status: TestStatus
    """Test pass test status."""

    super_pass_id: int = None
    """Id of super test pass (not None only when the current test is a subtest)."""

    # ------ Test organization details

    test_point_id: int = None
    """Id of the current test pass testing point."""

    # ------ Individual details

    test_lang_id: int = None
    """Id of educational language of the individual copy of the test task."""

    adapt_scale: int = None
    """Test individual adapt scale."""

    dpa_level: DPALevel = None
    """DPA level."""

    # ------ Test scoring

    score: int = None
    """Raw test score (0-100 points)."""

    score_12: int = None
    """Converted 12-point scale score (0-12 points)."""

    score_100: decimal = None
    """Final ZNO test score (100-200 points)."""
