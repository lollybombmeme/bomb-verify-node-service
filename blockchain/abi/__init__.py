# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json

bridge_abi = None
with open("blockchain/abi/data/BridgeARB.json") as file:
    bridge_abi = json.load(file)  # load contract info as JSON

