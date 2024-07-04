# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class EvidentSchema(Schema):
    class Meta:
        unknown = RAISE

    amount = fields.Str(required=True)
    tx_hash = fields.Str(required=True)
    contract_address = fields.Str(required=True)
    user_address = fields.Str(required=True)
    from_chain_id = fields.Int(required=True)
    to_chain_id = fields.Int(required=True)

