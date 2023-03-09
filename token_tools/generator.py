from datetime import datetime

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36, urlsafe_base64_decode

from token_tools.settings import TOKEN_TIMEOUT


class TokenGenerator:
    """
    Generic token generation based on django.contrib.auth.tokens
    """

    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    secret = settings.SECRET_KEY

    @property
    def timestamp(self):
        return int((datetime.now() - datetime(2001, 1, 1)).total_seconds())

    def make_hash_string(self, *args, **kwargs):
        return salted_hmac(
            self.key_salt, self._make_hash_value(*args, **kwargs), secret=self.secret
        ).hexdigest()[::2]

    def make_token_with_timestamp(self, timestamp, *args, **kwargs):
        ts_b36 = int_to_base36(timestamp)
        hash_string = self.make_hash_string(*args, **kwargs)
        return "%s-%s" % (ts_b36, hash_string)

    def make_token(self, *args, **kwargs):
        # timestamp is number of seconds since 2001-1-1. Converted to base 36,
        # this gives us a 6 digit string until about 2069.
        ts_b36 = int_to_base36(self.timestamp)
        hash_string = self.make_hash_string(*args, **kwargs)
        return "%s-%s" % (ts_b36, hash_string)

    def decode_idb64(self, idb64):
        try:
            return urlsafe_base64_decode(idb64).decode()
        except (UnicodeDecodeError, ValueError):
            return None

    def token_idb64(self, *args, **kwargs):
        raise NotImplementedError

    def _make_hash_value(self, *args, **kwargs):
        raise NotImplementedError

    def check_token(self, token, *args, **kwargs):
        """
        Check that the token is valid
        """

        if not token:
            return False

        try:
            ts_b36, _ = token.split("-")
            ts = base36_to_int(ts_b36)
        except (ValueError, AssertionError):
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(
            self.make_token_with_timestamp(ts, *args, **kwargs), token
        ):
            return False

        # Check the timestamp is within limit.
        if (self.timestamp - ts) > TOKEN_TIMEOUT:
            return False

        return True
