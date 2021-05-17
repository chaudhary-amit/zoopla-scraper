# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:48:20 2017

@author: AC
"""

import logging
from lxml import html
import requests
import zoopla_rq

logger = logging.getLogger()

class HomeListing():
    
    def __init__(self, config, parent_id, history_id, survey_id):
        self.config = config
        self.parent_id = parent_id
        self.history_id = history_id
        self.survey_id = survey_id
        self.time = None
        self.price = None
        #add other attributes 
        
    def get_property_history_info(self):
        property_history_url = (self.config.URL_PROPERTY_ROOT 
                                + str(self.room_id))
        response = zoopla_rq.rq_request_with_repeats(self.config, 
                                                     property_history_url)
        if response is not None:
            page = response.text
            tree = html.fromstring(page)
            self.__get_history_info_from_tree(tree)
            return True
        else:
            return False
        
    def __get_time(self, tree):
        temp = tree.xpath('//p[@id="historic-listing-title"]/strong/text()')
        time = temp[0].strip()
        time = time.replace('\n', '')
        self.time = time
        
    def __get_price(self, tree):
        temp = tree.xpath('//strong[@class="buyers"]/text()')
        price = temp[0].strip()
        self.price = price
        
    def __get_history_info_from_tree(self, tree):
        self.__get_time(tree)
        self.__get_price(tree)
        
        