import json
import os
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = ['RS256']
CLIENT_ID = os.environ['CLIENT_ID']
API_AUDIENCE = os.environ['API_AUDIENCE']
REDIRECT_URI = os.environ['REDIRECT_URI']
REDIRECT_LOGIN = os.environ['REDIRECT_LOGIN']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    # get header from request
    auth_header = request.headers.get('authorization', None)

    token = None
    if auth_header is None:
        raise AuthError({
            'description': 'No Authorization header supplied',
            'code': 'UNAUTHORIZED'
        }, 401)
    # split bearer from authorization
    parts = auth_header.split()
    # 0 is the auth type(can be capitalized), 1 is the token
    if parts[0].lower() != 'bearer':
        # auth not supported
        raise AuthError({
            'description': 'Authorization method must be Bearer',
            'code': 'INVALID_AUTH_METHOD'
        }, 401)
    if len(parts) > 1 and parts[1] is not None:
        token = parts[1]

    return token


def check_permissions(permission, payload):
    # If payload does not include the claims/permissions, error

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'INVALID_CLAIMS',
            'description': 'Permissions are not included in the JWT token'
        }, 400)
    if permission not in payload['permissions']:
        # unathorized
        raise AuthError({
            'code': 'FORBIDDEN',
            'description': 'User does not have enough permissions to '
                           f'complete the operation. Required: ${permission}'
        }, 403)
    return True


def verify_decode_jwt(token):

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'INVALID_HEADER',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'TOKEN_EXPIRED',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'INVALID_CLAIMS',
                'description': 'Incorrect claims. Please, check the audience'
                               ' and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'INVALID_HEADER',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'INVALID_HEADER',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except Exception:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
