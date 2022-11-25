import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-ghmo5g35rrbody4g.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'identity access app'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code






## Auth Header
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'Invalid claims',
            'description': 'No header Found'
        }, 401)

        req_auth_header = request.headers['Authorization']
        req_auth_path = req_auth_header.split(' ')

        if len(req_auth_path) !=2:
            raise AuthError({
                'code': 'invalid claims',
                'description': 'Wrong claims'
            }, 401)
        
        if req_auth_path[0].lower() != 'bearer':
            raise AuthError({
                'code': 'Invalid_claims',
                'description': 'Incorrect JWT'
            }, 401)
        
        return (req_auth_path[1])



## check permissions

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid claim',
            'description': 'Permission not included in jwt'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorise',
            'description': 'Permision not found'
        }, 403)
    
    return True


## verify

def verify_decode_jwt(token):
    # get data in Header
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    # chose key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization Malformed'
        }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e'],
                }
        
        # final verification
        if rsa_key:
            try:
                # using the jwt to validate
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://'+AUTH0_DOMAIN+'/'       
                )
                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token  expired',
                    'description': 'Token Expired'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Unable to parse auth token'
                }, 400)
        
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Unable to locate appropriate key'
        }, 400)

            



# code below is for require auth Decorator method
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator