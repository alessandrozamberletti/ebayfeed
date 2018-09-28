# -*- coding: utf-8 -*-
import gzip
import io
import base64

from ebayfeed.constants import ENVIRONMENT_TO_API_DICT


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
    bstream = io.BytesIO()
    bstream.write(byte_str_gz)
    bstream.seek(0)
    with gzip.GzipFile(fileobj=bstream, mode='rb') as bs:
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
    return base64.b64encode('{}:{}'.format(client_id, client_secret))


def get_api_uri(env):
    """
    Retrieve eBay FeedAPI endpoints based on chosen environment.

    Args:
        env (str): eBay environment. Must be one of [ENVIRONMENT_PRODUCTION, ENVIRONMENT_SANDBOX].
                   Default: EBAY_PRODUCTION.

    Returns:
        str: PRODUCTION_API_URI or SANDBOX_API_URI.
    """
    return ENVIRONMENT_TO_API_DICT[env]
