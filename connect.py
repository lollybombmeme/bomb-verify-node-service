# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import asyncio

import motor
from flask_pymongo import PyMongo
import motor.motor_asyncio
from redis import Redis
from web3 import Web3

from blockchain import Blockchain
from config import Config
from redlock import Redlock
from lib import Chains


class InterfaceAsync:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
        self.client.get_io_loop = asyncio.get_event_loop
        self.db = self.client.core


connect_db = PyMongo()
redis_standalone = Redis.from_url(Config.REDIS_URL)

from lib import HTTPSecurity

security = HTTPSecurity(redis=redis_standalone)


