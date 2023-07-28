from dataclasses import dataclass


@dataclass(frozen=True)
class RetryOpts:
    """Retry options dataclass."""

    attempts: int | None = None
    """Maximum number of attempts (`None` - for unlimited - default option)."""

    interval: float | None = 1
    """Delay between attempts (seconds) - 1 by default (`None` to avoid delay)."""
