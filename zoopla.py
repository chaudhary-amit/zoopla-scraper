# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 21:25:23 2017

@author: AC
"""
from datetime import timedelta
import logging
import argparse
import sys
import time
import requests
from lxml import html
from datetime import datetime
import webbrowser
from zoopla_config import ABConfig
from zoopla_survey import ZSurvey
from HomeListing import HomeListing
import zoopla_rq

logging.basicConfig(level=logging.WARNING)

start_time = time.time()

ab_config = ABConfig()
survey = ZSurvey(ab_config, '1145280717', 'NW6')

# write to csv
survey.search(2)

# print the web
#survey.search(5)

#this is start from specifoc micro post code in case of code run error previously 
#survey.search(2,"N5 1XL")



end_time = time.time()

print("Elapsed time was :" , str(timedelta(seconds=(end_time - start_time))))

