# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.iapi import iapi_resources

api_resources = {
    '/api-guard/common/health_check': HealthCheck,
    **{f'/api-guard/iapi{k}': val for k, val in iapi_resources.items()},
}
