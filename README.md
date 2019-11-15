# django-token-tools

Suite of Django tools around token authentication

### Settings

#### TOKEN_TIMEOUT

Validity time of a token in seconds.

### token_tools.generator.TokenGenerator

This module is a generic version of the token generator used by django for
reset password URLs.
You should implement `token_idb64` and `_make_hash_value` to make it work.

#### token_idb64

This method must return a base64 encoded data, it's used to validate the token, and can embed data.
It must not embed critical data, it can be simply decoded.

#### _make_hash_value

This is the hash value, it must be unique by user. It will be used to generate the token, and to validate a token
with idb64 content.
