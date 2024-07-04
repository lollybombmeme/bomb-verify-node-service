# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import string
from datetime import datetime, timezone
from random import choice

from bson import ObjectId
from web3 import Web3

util_web3 = Web3()


def dt_utcnow():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def is_oid(oid: str) -> bool:
    return ObjectId.is_valid(oid)


def random_str(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for x in range(size))


def get_default(default):
    if callable(default):
        return default()
    return default


def allowed_file(filename, regex):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in regex


def get_crypto_currency_address(redis_cluster, chain: str, symbol: str):
    _key = f'crypto_currencies:{chain}:{symbol}'
    _address = redis_cluster.get(_key)

    return _address


# redis key

# create domain status
# f'smc:user_template_id:{_user_template_id}:create_domain:{_website_domain}:status'

# create smc status
# f'smc:_id:{_contract_id}:create_smc:status'
