import traceback

import jwt
import sentry_sdk
from flask import (request, jsonify)

from functools import wraps
from marshmallow import Schema, ValidationError, fields, EXCLUDE
from pydash import get
from sentry_sdk import capture_exception

# from .redis import redis_cluster
from ..enums.http import StatusInt, ErrorCode
from ..schema import BaseReq, ObjectIdField


def auth_token_key(user: str, subdomain: str) -> str:
    if not subdomain:
        subdomain = ''
    return f'dapp:tokens:{subdomain}:{user}'


def make_response(data: dict = {},
                  msg: str = '',
                  error_code: str = '', error=None) -> dict:
    if error:
        if not isinstance(error, dict):
            error = {
                'error': error
            }
        return {
            'data': data,
            'msg': msg,
            'error_code': error_code,
            'error': error
        }
    return {
        'data': data,
        'msg': msg,
        'error_code': error_code
    }


def _get_token_info(token):
    try:
        return jwt.decode(token, algorithm="RS256", options={"verify_signature": False})
    except:
        traceback.print_exc()
        capture_exception()
        return False


def _get_token():
    _rq_token = request.headers.get('Authorization')

    if not _rq_token or 'Bearer ' not in _rq_token:
        _rq_token = request.args.get('access_token', type=str)
        if not _rq_token:
            return None, None
    else:
        _rq_tokens = _rq_token.split(' ')
        if len(_rq_tokens) < 1:
            return None, None
        _rq_token = _rq_tokens[1]

    # Get pos token on Redis pos info
    _data = _get_token_info(_rq_token)
    if not isinstance(_data, dict):
        return None, None
    if not _data.get('payload'):
        return None, None

    return _data.get('payload'), _rq_token


def _verify_token_req(subdomain):
    """
        - The function that verifies token
    """

    _token_info, _rq_token = _get_token()

    if not _token_info:
        return False

    _token_existed = redis_cluster.get(auth_token_key(user=_token_info.get('user'), subdomain=subdomain))

    if _token_existed and _token_existed == _rq_token:
        return _token_info

    return False


class _AuthSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    public_address = fields.String()
    disable_funcs = fields.List(fields.String(), missing=[])
    device_id = fields.String(missing='')
    xrip = fields.String(missing='')
    user = ObjectIdField()
    provider = fields.String()


class Object(object):
    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])


from flask import request


def get_subdomain():
    try:
        _rq_host = get(request.headers, 'Origin') or get(request.headers, 'origin')
        # print("** Header debug subdomain : ", dict(request.headers))
        if _rq_host:
            _rq_host = _rq_host.replace('https://', '')
            _lt = _rq_host.split('.')
            if len(_lt) == 3 and _lt[1] == '':
                return _lt[0].replace('-stag', '')
    except:
        traceback.print_exc()
        pass
    return ""


def handle_res(res_schema=None, req_schema=None, param_schema=None, login: bool = True):
    """
        - return:
            + params: object if param_schema not None
            + body: object if req_schema not None
            + wallet: object if login = True
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate res:
            _subdomain = get_subdomain()

            try:
                _params = request.args.to_dict() or {}
                if 'debug' in _params:

                    if 'subdomain' in _params:
                        _subdomain = _params['subdomain']

                kwargs['subdomain'] = _subdomain

                if request.method == 'GET' and param_schema:
                    _param_schema = param_schema()
                    _validate_params = _param_schema.validate(_params)
                    if _validate_params:
                        raise ValidationError(_validate_params)

                    _params = Object(param_schema().dump(_params))
                else:
                    _params = Object(BaseReq().dump(_params))

                if request.method in ['POST', 'PUT', 'DELETE'] and req_schema:
                    _json_body = request.json
                    _req_schema = req_schema()
                    _validate = _req_schema.validate(_json_body)
                    if _validate:
                        raise ValidationError(_validate)
                    _body = Object(req_schema().dump(_json_body))

                    kwargs['body'] = _body

                kwargs['params'] = _params
            except ValidationError as err:
                error = err.messages
                return make_response(msg='Missing data for required field', error=error,
                                     error_code=ErrorCode.BAD_REQUEST), StatusInt.Bad

            if login:
                _wallet = _verify_token_req(_subdomain)

                if not isinstance(_wallet, dict):
                    return make_response(msg='Please login to continue',
                                         error_code=ErrorCode.REQUIRED_AUTH), StatusInt.Forbidden

                kwargs['wallet'] = Object(_AuthSchema().load(_wallet))

            try:
                resp = func(*args, **kwargs)
            except Exception as e:
                if hasattr(e, 'response'):
                    return e.response
                else:
                    traceback.print_exc()
                    sentry_sdk.capture_exception()
                    return make_response(msg='Unknown error', error_code=ErrorCode.UNKNOWN_ERROR), StatusInt.Unknown
            # Response
            if res_schema:
                try:
                    resp = res_schema().load(resp)
                except ValidationError as err:
                    msg = err.messages
                    sentry_sdk.capture_message(msg)
                    traceback.print_exc()
            if not isinstance(resp, dict):
                raise Exception('Response must be a dict')
            resp = make_response(data=resp)

            return resp, 200

        return wrapper

    return decorator
