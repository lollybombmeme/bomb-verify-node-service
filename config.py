# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    PROJECT = "guard"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')

    # Authentication
    TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Config celery worker
    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    BROKER_USE_SSL = True
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.send_task_check_evident_node1': 'guard-evident-1-queue',
        'worker.send_task_check_evident_node2': 'guard-evident-2-queue',
        'worker.send_task_check_evident_node3': 'guard-evident-3-queue',
        'worker.send_task_check_evident_node4': 'guard-evident-4-queue',
        'worker.send_task_check_evident_node5': 'guard-evident-5-queue'
    }   

    SERVICE_URL = os.getenv('SERVICE_URL')
    # Redis
    REDIS_URL = os.getenv('REDIS_URL')
    # Blockchain
    BNB_RPC_URI = json.loads(os.getenv('BNB_RPC_URI', default='[]'))
    ETH_RPC_URI = json.loads(os.getenv('ETH_RPC_URI', default='[]'))
    BASE_RPC_URI = json.loads(os.getenv('BASE_RPC_URI', default='[]'))

    NODES_GUARD = json.loads(os.getenv('NODES_GUARD', default='[]'))
    BNB_CONTRACT_ADDRESS = os.getenv('BNB_CONTRACT_ADDRESS')
    ETH_CONTRACT_ADDRESS= os.getenv('ETH_CONTRACT_ADDRESS')
    BASE_CONTRACT_ADDRESS= os.getenv('BASE_CONTRACT_ADDRESS')

    BNB_CHAIN_ID = os.getenv('BNB_CHAIN_ID')
    ETH_CHAIN_ID = os.getenv('ETH_CHAIN_ID')
    BASE_CHAIN_ID = os.getenv('BASE_CHAIN_ID')


    SUPPORT_CHAINS = json.loads(os.getenv('SUPPORT_CHAINS', default='[]'))




    