# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from schemas.evident import EvidentSchema
from connect import security
from config import Config
from models import RequestEvidentModel
from lib.logger import debug
from worker import worker
from tasks.send_task_evident import send_task_check_evident_node1, send_task_check_evident_node2, send_task_check_evident_node3, send_task_check_evident_node4, send_task_check_evident_node5


class EvidentResource(Resource):
    @security.http(
        form_data=EvidentSchema(),  # form_data
    )
    def post(self, form_data):

        # check chain support
        _chains = Config.SUPPORT_CHAINS
        if len(_chains) == 0 or form_data['from_chain_id'] not in _chains or form_data['to_chain_id'] not in _chains:
            debug(f"Chain not support {form_data} ")
            return
        # add tracked request for txn hash, from_chain_id
        _is_check = RequestEvidentModel.find_one(
            {
                "from_chain_id": form_data['from_chain_id'],
                "tx_hash": form_data['tx_hash']
            }
        )
        if _is_check:
            debug(
                f"Duplicate request check evident hash {form_data['tx_hash']}")
            return
        else:
            RequestEvidentModel.insert_one({
                "from_chain_id": form_data['from_chain_id'],
                "tx_hash": form_data['tx_hash'],
                "amount": form_data['amount'],
                "request": form_data,
                "created_by": "api-guard"
            })

        debug(f"Get request check evident {form_data}")

        form_data['node_index'] = 0
        _log = worker.send_task(
            'worker.send_task_check_evident_node1', (form_data,))
        debug(f"Worker: Send task node 1 : {_log}")

        form_data['node_index'] = 1
        _log = worker.send_task(
            'worker.send_task_check_evident_node2', (form_data,))
        debug(f"Worker: Send task node 2 : {_log}")

        form_data['node_index'] = 2
        _log = worker.send_task(
            'worker.send_task_check_evident_node3', (form_data,))
        debug(f"Worker: Send task node 3 : {_log}")

        form_data['node_index'] = 3
        _log = worker.send_task(
            'worker.send_task_check_evident_node4', (form_data,))
        debug(f"Worker: Send task node 4 : {_log}")

        form_data['node_index'] = 4
        _log = worker.send_task(
            'worker.send_task_check_evident_node5', (form_data,))
        debug(f"Worker: Send task node 5 : {_log}")

        return {}
