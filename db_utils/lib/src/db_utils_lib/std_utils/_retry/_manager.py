from time import sleep

from . import RetryOpts


class RetryManager:
    """
    Simple class, helps to unify retry managing
    to avoid need of changing code in many places in case if general retry protocol
    and/or `RetryOpts` class will change.
    """

    # ------ Protected fields

    _allow_sleeps: bool     # Indicates is it allowed to call `time.sleep()` method if delay is necessary
    _options: RetryOpts     # Retry options

    _counter: int   # Attempts counter

    # ------ Properties

    @property
    def counter(self) -> int:
        """Stores current numer of made attempts."""

        return self._counter

    @property
    def options(self) -> RetryOpts:
        """Retry options."""

        return self._options

    @property
    def allow_sleeps(self) -> bool:
        """Indicates is it allowed to call `time.sleep()` method if delay is necessary."""

        return self._allow_sleeps

    @allow_sleeps.setter
    def allow_sleeps(self, value: bool):
        self._allow_sleeps = value

    # ------ Instantiation methods

    def __init__(self, options: RetryOpts, allow_sleeps: bool = True):
        """
        Initializes new instance of RetryManager.

        :param options: retry options.
        :param allow_sleeps: sets is it allowed to call `time.sleep()` method if delay is necessary.
        """

        self._allow_sleeps = allow_sleeps
        self._options = options
        self._counter = 0

    # ------ Main functional attempt() method

    def hasnext(self) -> bool:
        """Checks attempts counter, returns `False` if attempts limit reached on current attempt, otherwise `True`"""

        return self._options.attempts is None or self._counter < self._options.attempts

    def attempt(self, allow_sleep: bool = True) -> bool:
        """
        If attempts limit is not reached, increases attempts counter & executes actions due to interval protocol,
        then returns `True`, otherwise returns `False`.

          **WARNING**: Calls `time.sleep()` method for interval delays.
          Can be disabled by `allow_sleep` parameter (for current call) or by the `allow_sleeps` property.

            **NOTE**: If attempts limit not reached yet and sleeps allowed - this will take delay according to settings,
            so it is not recommended to use this method to check attempts limit reach - use `hasnext()` instead.

        :param allow_sleep: sets is it allowed to call `time.sleep()` method if delay is necessary
                            (applied only to current call - to set for the whole session use `allow_sleeps` property)
        :return: `False` if attempts limit reached - else `True`
        """

        self._counter += 1

        if self._options.attempts is None or self._counter < self._options.attempts:
            if self._options.interval is not None and self._allow_sleeps and allow_sleep:
                sleep(self._options.interval)
            return False

        return True

    # ------ Iterator protocol

    def __iter__(self):
        return self

    def __next__(self):
        if not self.attempt():
            raise StopIteration()


def retry_session(attempts: int | None = None, interval: float | None = 1) -> RetryManager:
    """
    Initialize new instance of `RetryManager` class.

      Unlike to `RetryManager.__init__()` takes retry options as args & kwargs
      and packs them by `RetryOpts` automatically. Then initializes `RetryManager` instance in a normal way.

    :param attempts: maximum number of attempts (`None` - for unlimited - default option)
    :param interval: delay between attempts (seconds) - 1 by default (`None` to avoid delay)
    :return: `RetryManager` instance
    """

    return RetryManager(RetryOpts(attempts=attempts, interval=interval))
