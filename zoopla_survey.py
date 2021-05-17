# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 19:50:06 2017

@author: AC
"""
import logging
import sys
import random
from datetime import date
import requests
from lxml import html
from HomeListing import HomeListing
import zoopla_rq

logger = logging.getLogger()

class ZSurvey:
    
    def __init__(self, config, survey_id, postcode):
        self.config = config
        self.survey_id = survey_id
        self.postcode = postcode
    
    def search(self, flag, starting_code="FULL"):
        micro_postcodes = self.get_micro_postcodes()
        if len(micro_postcodes) > 0:
            if starting_code == self.config.STARTING_CODE:
                self.__search_loop_micro_postcodes(micro_postcodes, flag)
            else:
                index = micro_postcodes.index(starting_code)
                micro_postcodes = micro_postcodes[index:]
                self.__search_loop_micro_postcodes(micro_postcodes, flag)
    def __search_loop_micro_postcodes(self, micro_postcodes, flag):
        for micro_postcode in micro_postcodes:
            print("Accesing Zoopla archieve for following micro post code: ", micro_postcode)
            # function to get the property info from micro post codes
            self.get_property_history(micro_postcode, flag)
            # test break statements 
            #if micro_postcodes.index(micro_postcode) == 1:
            #    break
    
    def get_property_history(self, micro_postcode, flag):
        url_micro_code = (micro_postcode.replace(" ","-")).lower()
        url = self.config.URL_HOUSE_PRICE + url_micro_code
        response = zoopla_rq.rq_request_with_repeats(self.config, url)
        tree = html.fromstring(response.text)
        page_list = tree.xpath('//div[@class="paginate bg-muted"]/a/text()')
        if len(page_list) > 0:
            page_list.insert(0,'1')
            page_list.remove('Next')
        else:
            page_list = ['1'] 
        property_link = list()
        property_address = list()
        property_attributes = list()
        for page in page_list: 
            page_url = url + self.config.URL_PAGE_SEARCH + page
            response = zoopla_rq.rq_request_with_repeats(self.config, page_url)
            tree = html.fromstring(response.text)
            property_link.extend(tree.xpath('//td[@class="browse-cell-address"]/a[1]/@href'))
            #print('property link len ', len(property_link))
            property_address.extend(tree.xpath('//td[@class="browse-cell-address"]/a[1]/div/text()'))
            property_attributes.extend(tree.xpath('//td[@class="browse-cell-address"]/div[@class="attributes"]/text()'))
        for i in range(len(property_link)):
             property_id = self.id_from_url(property_link[i])
             property_address_listing = property_address[i]
             property_attr_listing = property_attributes[i]
             self.history_from_property(property_id, property_address_listing, micro_postcode, property_attr_listing, flag)
             #mannual code breaks for testing (remove aftet tuning the http request
             #if i == 5:
             #    break
                       
            
    def get_micro_postcodes(self):
        url = self.config.URL_SEARCH_ROOT + self.postcode
        response = zoopla_rq.rq_request_with_repeats(self.config, url)
        tree = html.fromstring(response.text)
        page_list = tree.xpath('//div[@class="paginate bg-muted"]/a/text()')
        if len(page_list) > 0:
            page_list.insert(0,'1')
            page_list.remove('Next')
        else:
            page_list = ['1'] 
        #print(page_list)
        micro_postcodes = list()
        for page in page_list: 
            page_url = url + self.config.URL_PAGE_SEARCH + page
            #print('page url:', page_url)
            response = zoopla_rq.rq_request_with_repeats(self.config, page_url)
            tree = html.fromstring(response.text)
            codes_page_wise = tree.xpath('//a[@class="sold-prices-street-postcode-link"]/text()')
            #print('page:', page)
            micro_postcodes.extend(codes_page_wise)
            #print ('postcode len',len(micro_postcodes))
            #test break statement
            #if page_list.index(page) == 2:
            #    break
        return micro_postcodes
    
    
    def history_from_property(self, property_id, property_address, micro_postcode, property_attributes, flag):
        return_value = self.get_history_pages_links(property_id)
        history_pages_link = return_value[0]
        property_address = property_address.strip()
        property_address = property_address.replace('\n','')
        property_address = " ".join(property_address.split())
        property_attributes = property_attributes.strip()
        property_attributes = property_attributes.replace('\n','')
        history_date = return_value[1]
        if history_pages_link:
            for link_url in history_pages_link:
                history_id = self.id_from_url(link_url)
                history_date_val = history_date[history_pages_link.index(link_url)]
                listing = HomeListing(self.config, property_id, property_address, micro_postcode, property_attributes, history_id, history_date_val, self.survey_id , self.postcode)   
                listing.get_property_history_info(flag)
                # if date is NA then superimpose date from parent                                    
        elif not history_pages_link:
            history_id = ''
            history_date_val = ''
            listing = HomeListing(self.config, property_id, property_address, micro_postcode, property_attributes, history_id, history_date_val, self.survey_id , self.postcode)
            listing.save_null_history(flag)
                
    def get_history_pages_links(self, property_id):
        history_url_return = list()
        url = self.config.URL_PROPERTY_ARCHIEVE + str(property_id)
        #print('property_id url:', url)
        response = zoopla_rq.rq_request_with_repeats(self.config, url)
        tree = html.fromstring(response.text)
        history_url = tree.xpath('//a[@class="year-history-link"]/@href')
        history_year = list()
        history_date = tree.xpath('//a[@class="year-history-link"]/text()')
        for i in range(len(history_date)):
            tmp = tree.xpath('//a[@class="year-history-link"][text()= "{}"]//preceding-sibling::span[@class="year-history-heading"]'.format(history_date[i]))
            history_year.append(tmp[0].text)
        history_date = [j.strip() for j in history_date]
        for i in range(len(history_date)):
            history_date[i] = history_date[i] + " " + history_year[i] 
        # catching the sigle history:  imp fix (implementing in non cool style)
        if not history_date:
            history_single_url = tree.xpath('//div[@id = "historic-result"][@class = "clearfix top"]//strong/a/@href')
            historty_single_date = tree.xpath('//div[@id = "historic-desc"]//p/span[@class = "historic-result-date buyers"]/text()')
            if history_single_url:
                history_url = history_single_url
                history_date_string = historty_single_date[0].strip()
                history_date_string = history_date_string.replace('\n', '')
                position = history_date_string.find("on")
                date_s = history_date_string[position+3:(position+16)]
                history_date.append(date_s)    
        #print('history_url ',history_url)
        #history_time = tree.xpath('//a[@class="time link"]/@href')
        history_url_return.append(history_url)
        history_url_return.append(history_date)
        return history_url_return
        
    def id_from_url(self, link_url):
        #terurn trailing/ id 
        location = link_url.rfind('/')
        id = link_url[location+1:]
        return id
        
        
