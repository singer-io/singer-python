import unittest

from singer.exceptions import SingerConfigurationError
from singer.exceptions import SingerDiscoveryError
from singer.exceptions import SingerError
from singer.exceptions import SingerRetryableRequestError
from singer.exceptions import SingerSyncError

class TestSingerErrors(unittest.TestCase):
    def test_SingerError_prints_correctly(self):
        error_text = "An error occured"

        with self.assertRaises(SingerError) as test_run:
            raise SingerError(error_text)

        expected_text = "SingerError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))

    def test_SingerConfigurationError_prints_correctly(self):
        error_text = "An error occured"

        with self.assertRaises(SingerConfigurationError) as test_run:
            raise SingerConfigurationError(error_text)

        expected_text = "SingerConfigurationError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))

    def test_SingerDiscoveryError_prints_correctly(self):
        error_text = "An error occured"

        with self.assertRaises(SingerDiscoveryError) as test_run:
            raise SingerDiscoveryError(error_text)

        expected_text = "SingerDiscoveryError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))

    def test_SingerSyncError_prints_correctly(self):
        error_text = "An error occured"

        with self.assertRaises(SingerSyncError) as test_run:
            raise SingerSyncError(error_text)

        expected_text = "SingerSyncError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))

    def test_SingerRetryableRequestError_prints_correctly(self):
        error_text = "An error occured"

        with self.assertRaises(SingerRetryableRequestError) as test_run:
            raise SingerRetryableRequestError(error_text)

        expected_text = "SingerRetryableRequestError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))

    def test_SingerError_prints_multiple_lines_correctly(self):
        error_text = "\n".join(["Line 1", "Line 2", "Line 3"])

        with self.assertRaises(SingerError) as test_run:
            raise SingerError(error_text)

        expected_text = "SingerError\n" + error_text
        self.assertEquals(expected_text,
                          str(test_run.exception))
