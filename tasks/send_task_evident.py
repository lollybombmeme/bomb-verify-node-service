import traceback
import sentry_sdk
from bson import json_util
from pydash import get
from config import Config
from lib.logger import debug
from worker import worker
from helper.bridge import BridgeHelper
from blockchain import Blockchain
from web3 import Web3

def check_evident(self, data):
    
    _nodes= Config.NODES_GUARD
    _node_index = data['node_index'] 
    data['delay'] = _nodes[_node_index].get("delay_block")
    data['node_id'] = _nodes[_node_index].get("id")
    data['signature_sign_pk'] = _nodes[_node_index].get("signature_sign_pk")
    
    try:
        
        # Check transaction on Source Chain is correct amount (wei), txn_hash with confidence confirm block number
        _status_evident = BridgeHelper.check_txn(data)
        if not _status_evident:
            return
        
        data["status"] = _status_evident
        del data['node_index']
        del data['delay']
        del data['signature_sign_pk'] 
        # Update status flag for bridge service
        BridgeHelper.callback_status_evident(data)
        
    except Exception as e:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        debug(f"retry")
        self.retry(exc=e, countdown=20) # NOTE: retry task if has error after 5 seconds


@worker.task(name='worker.send_task_check_evident_node1', rate_limit='1000/s', bind=True, max_retries=3)
def send_task_check_evident_node1(self, data):
    debug(f"Worker: Send task node 1: {data}")
    check_evident(self, data)


@worker.task(name='worker.send_task_check_evident_node2',rate_limit='1000/s', bind=True, max_retries=3)
def send_task_check_evident_node2(self, data):
    check_evident(self, data)


@worker.task(name='worker.send_task_check_evident_node3',rate_limit='1000/s', bind=True, max_retries=3)
def send_task_check_evident_node3(self, data):
    check_evident(self, data)       
        
@worker.task(name='worker.send_task_check_evident_node4',rate_limit='1000/s', bind=True, max_retries=3)
def send_task_check_evident_node4(self, data):
    check_evident(self, data)     
        
        
@worker.task(name='worker.send_task_check_evident_node5',rate_limit='1000/s', bind=True, max_retries=3)
def send_task_check_evident_node5(self, data):
    check_evident(self, data)      