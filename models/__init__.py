# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['EvidentModel']

from config import Config
from connect import connect_db, redis_standalone
from lib import DaoModel
from models.evident import EvidentDao

# SampleModel = SampleModel(col=connect_db.db.SampleModel, redis=redis_standalone)
EvidentModel = EvidentDao(col=connect_db.db.evident, redis=redis_standalone)
RequestEvidentModel = EvidentDao(col=connect_db.db.evident_request, redis=redis_standalone)
