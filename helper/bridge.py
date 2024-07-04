# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
from pydash import get
from web3 import Web3
from config import Config
import requests
from lib.logger import debug
from models import EvidentModel
from blockchain.abi import bridge_abi
import traceback
import sentry_sdk
import time
from helper.signature import SignatureHelper
import random
from exceptions.web3 import ProviderNotConnected


class BridgeHelper:

    @staticmethod
    def check_txn(_data):
        loop = False
        _current_block_number = 0
        _data['signature'] = ""
        _data['block_number'] = 0
        _tx_json = []

        if _data["from_chain_id"] == int(Config.BNB_CHAIN_ID):
            _rpc_urls = Config.BNB_RPC_URI
            _bridge_contract_address = Config.BNB_CONTRACT_ADDRESS

        if _data["from_chain_id"] == int(Config.ETH_CHAIN_ID):
            _rpc_urls = Config.ETH_RPC_URI
            _bridge_contract_address = Config.ETH_CONTRACT_ADDRESS

        if not _rpc_urls or len(_rpc_urls) == 0:
            debug(f"Get List From Chain RPC fail")
            return
        while not loop:

            _rpc_url = _rpc_urls[0]
            _web3 = Web3(Web3.HTTPProvider(
                _rpc_url, request_kwargs={'timeout': 30}))

            # check connection RPC providers
            if not _web3.is_connected():
                if len(_rpc_urls) > 1:

                    _rpc_urls.pop(0)
                    _rpc_urls.append(_rpc_url)

                sentry_sdk.capture_message(
                    f"Unable to connect RPC {_rpc_url} retry after 30s with RPC : {_rpc_urls[0]}")
                time.sleep(30)
                continue

            _contract = _web3.eth.contract(address=Web3.to_checksum_address(
                _bridge_contract_address), abi=bridge_abi)
            try:
                _receipt = _web3.eth.wait_for_transaction_receipt(
                    _data['tx_hash'])
            except Exception as e:
                debug(f"Check transaction fail {e}")
                return "fail"

            _tx = Web3.to_json(
                _contract.events.Bridge().process_receipt(_receipt))
            _tx_json = json.loads(_tx)
            _current_block_number = _web3.eth.block_number
            debug(f"_tx_json: {_tx_json}")

            _txn_block_number = _tx_json[0].get("blockNumber")
            _data["block_number"] = int(_current_block_number)
            debug(
                f"_current_block_number {_current_block_number} - delay block: {int(_data.get('delay'))} for txn block number: {_txn_block_number}")
            if int(_txn_block_number) + int(_data.get("delay")) < _current_block_number:
                loop = True
            else:
                time.sleep(30)

        # check amount
        if len(_tx_json) > 0 and str(_data['amount']).strip() != str(_tx_json[0]['args']['amount']).strip():
            debug(f"Check amount fail.")
            return "fail"

        # generate signature for node
        _signature = SignatureHelper.generate_bridge_signature(_data)
        _data['signature'] = _signature

        return "success"

    @staticmethod
    def callback_status_evident(_data):
        print("_data: ", _data)
        _res = requests.put(
            f'{Config.SERVICE_URL}/iapi/transaction',
            json=_data,
        )
        _json = _res.json()
        EvidentModel.insert_one({
            "from_chain_id": _data['from_chain_id'],
            "tx_hash": _data['tx_hash'],
            "evident": _data,
            "response": _json,
            "created_by": _data['node_id']

        })

        debug(f'callback_status_evident result: {_json}')
