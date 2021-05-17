#!/usr/bin/python3
# ============================================================================
# Zoopla Configuration module, for use in web scraping
# ============================================================================
import logging
#import psycopg2
#import psycopg2.errorcodes
import os
import sys
from datetime import datetime

logger = logging.getLogger()
logger.info("Logger got")

class ABConfig():

    def __init__(self, args=None):        
         
        self.config_file = None
        if args is not None:
            self.config_file=args.config_file
            try:
                if args.verbose:
                    self.log_level = logging.DEBUG
                else:
                    self.log_level = logging.INFO
            except:
                self.log_level = logging.INFO         
        self.connection = None
        self.FLAGS_ADD = 1
        self.FLAGS_CSV = 2
        self.FLAGS_PRINT = 5
        self.FLAG_WORD_PRESENCE = 0
        self.FLAG_WORD_VAL = 1
        self.FLAGS_INSERT_REPLACE = True
        self.FLAGS_INSERT_NO_REPLACE = False
        self.URL_ROOT = "https://www.zoopla.co.uk/"
        self.URL_SEARCH_ROOT = self.URL_ROOT + "house-prices/browse/"
        self.URL_HOUSE_PRICE = self.URL_ROOT + "house-prices/"
        self.URL_PROPERTY_ARCHIEVE = self.URL_ROOT + "property/"
        self.URL_PROPERTY_ROOT = self.URL_ROOT + "property-history/"
        self.URL_API_SEARCH_ROOT = self.URL_ROOT + "search/search_results"
        self.URL_PAGE_SEARCH = "/?st=EORST&pn="
        self.SEARCH_LISTINGS_ON_FULL_PAGE = 18
        self.HTTP_PROXY_LIST = []
        self.HTTP_PROXY_LIST_COMPLETE = []
        self.MAX_CONNECTION_ATTEMPTS = 10
        self.REQUEST_SLEEP = 0
        self.HTTP_TIMEOUT = 10.0
        self.RE_INIT_SLEEP_TIME = 60
        self.USER_AGENT_LIST = ['Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko']
        self.FILE_NAME_CSV = "Zoopla_data_"
        self.STARTING_CODE = "FULL"
    