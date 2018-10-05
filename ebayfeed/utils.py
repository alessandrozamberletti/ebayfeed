# -*- coding: utf-8 -*-
from gzip import GzipFile
from io import BytesIO
from base64 import b64encode

from ebayfeed.constants import _ENVIRONMENT_TO_API_DICT


def gunzip(byte_str_gz):
    """
    Decompress a gzipped byte string.
    See: https://gist.github.com/Garrett-R/dc6f08fc1eab63f94d2cbb89cb61c33d

    Args:
        byte_str_gz (str): Gzipped byte string.

    Returns:
        str: decompressed string.

    Raises:
        IOError: when input is not a gzipped str.
    """
    bstream = BytesIO()
    bstream.write(byte_str_gz)
    bstream.seek(0)
    with GzipFile(fileobj=bstream, mode="rb") as bs:
        compressed_bytes = bs.read()
    return compressed_bytes.decode()


def get_base64_oauth(client_id, client_secret):
    """
    Retrieve Base64-encoded OAuth credentials (<client_id>:<client_secret>).

    Args:
        client_id (str): App-ID (Client-ID) from application keyset.
        client_secret (str): Cert-ID (Client-Secret) from application keyset.

    Returns:
        str: Base64-encoded OAuth credentials (<client_id>:<client_secret>).
    """
    credentials = "{}:{}".format(client_id, client_secret).encode(
        "utf-8"
    )  # python 3.x compatibility
    return b64encode(credentials).decode("utf-8")


def get_api_uri(env):
    """
    Retrieve eBay FeedAPI endpoints based on chosen environment.

    Args:
        env (str): eBay environment. Must be one of [ENVIRONMENT_PRODUCTION, ENVIRONMENT_SANDBOX].
                   Default: EBAY_PRODUCTION.

    Returns:
        str: _PRODUCTION_API_URI or _SANDBOX_API_URI.
    """
    return _ENVIRONMENT_TO_API_DICT[env]
