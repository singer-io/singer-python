"""
The exceptions module contains Exception subclasses whose instances might be
raised by the singer library or taps that use the singer library.
"""

class SingerError(Exception):
    """The base Exeception class for singer"""
    def __init__(self, message):
        """Create an exeception with a multiline error message

        The first line is the error's class name. The subsequent lines are
        the message that class was created with.
        """
        super().__init__(f"{self.__class__.__name__}\n{message}")


class SingerConfigurationError(SingerError):
    """The base class of errors encountered before discovery and before sync mode"""


class SingerDiscoveryError(SingerError):
    """The base class of errors encountered in discovery mode"""


class SingerSyncError(SingerError):
    """The base class of errors encountered in sync mode"""


class SingerRetryableRequestError(SingerError):
    """This error is meant to be thrown when a tap encounters a retryable request"""
