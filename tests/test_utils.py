# -*- coding: utf-8 -*-
from unittest import TestCase, main
from gzip import GzipFile
from io import BytesIO


from ebayfeed.constants import (
    ENVIRONMENT_PRODUCTION,
    ENVIRONMENT_SANDBOX,
    PRODUCTION_API_URI,
    SANDBOX_API_URI,
)
from ebayfeed.utils import gunzip, get_base64_oauth, get_api_uri


def _compress(msg):
    out = BytesIO()
    with GzipFile(fileobj=out, mode="w") as f:
        f.write(msg)
    return out.getvalue()


class TestBase(TestCase):
    def test_gunzip_empty_byte_empty_rsp(self):
        self.assertEqual("", gunzip(b""))

    def test_gunzip_raise_for_wrong_str(self):
        with self.assertRaises(IOError):
            gunzip(b"im not a gzip file")

    def test_gunzip_works(self):
        self.assertEqual("ciao", gunzip(_compress(b"ciao")))

    def test_get_base64_oauth(self):
        self.assertEqual("dXNlcjprZXk=", get_base64_oauth("user", "key"))

    def test_api_uri_is_correct_for_env(self):
        self.assertEqual(PRODUCTION_API_URI, get_api_uri(ENVIRONMENT_PRODUCTION))
        self.assertEqual(SANDBOX_API_URI, get_api_uri(ENVIRONMENT_SANDBOX))


if __name__ == "__main__":
    main()
