# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:48:20 2017

@author: AC
"""

import logging
from lxml import html
import requests
import zoopla_rq
import csv

logger = logging.getLogger()

class HomeListing():
    
    def __init__(self, config, parent_id, parent_address, micro_postcode, parent_attributes, history_id, history_date_val, survey_id, postcode):
        self.config = config
        self.parent_id = parent_id
        self.parent_address = parent_address
        self.micro_postcode = micro_postcode
        self.parent_attributes = parent_attributes 
        self.history_id = history_id
        self.history_date_val = history_date_val
        self.survey_id = survey_id
        self.postcode = postcode
        self.time = None
        self.price = None
        self.property_type = None
        self.property_info = None
        self.property_features = None
        self.property_description = None
        
        # add derived attributes 
        self.property_FlatHouse = ""
        self.property_holding = ""
        self.no_bedrooms = ""
        self.no_baths = ""
        self.no_receps = ""
        self.listing_type = ""
        self.listing_date = ""
        self.listing_FlatHouse = ""
        self.listing_no_bed = ""
        self.listing_price = ""
        self.listing_Furnished = ""
        
        #add other attributes 
        
    def get_property_history_info(self, flag):
        property_history_url = (self.config.URL_PROPERTY_ROOT 
                                + str(self.history_id))
        response = zoopla_rq.rq_request_with_repeats(self.config, 
                                                     property_history_url)
        if response is not None:
            page = response.text
            tree = html.fromstring(page)
            self.__get_history_info_from_tree(tree, flag)
            return True
        else:
            return False    
        
    def __get_time(self, tree):
        temp = tree.xpath('//p[@id="historic-listing-title"]/strong/text()')
        time = temp[0].strip()
        time = time.replace('\n', '')
        # check fo N/A Zoopla error 
        time_NA_index = time.find("N/A")
        if time_NA_index != -1:
            time = time.replace("N/A", self.history_date_val) 
        self.time = time
        
    def __get_price(self, tree):
        temp = tree.xpath('//strong[@class="buyers"]/text()')
        price = temp[0].strip()
        self.price = price
    
    def __get_property_type(self, tree):
        temp = tree.xpath('//strong[@class="nobold"]/text()')
        property_type = temp[0].strip()
        self.property_type = property_type
        
    def __get_property_info(self, tree):
        temp = tree.xpath('//ul[@class="listing-content clearfix noprint"]/li/text()')
        property_info = temp
        property_info = [j.strip() for j in property_info]
        self.property_info = property_info
    
    def __get_property_features(self, tree):
        temp = tree.xpath('//div[@class="historic-listing-old"]/div/div/ul//li//text()')
        property_features = temp
        property_features = [j.strip() for j in property_features]
        self.property_features = property_features
    
    def __get_property_description(self, tree):
        temp = tree.xpath('//div[@itemprop="description"]//text()')
        property_description = temp
        property_description = [j.strip() for j in property_description]
        self.property_description = property_description
        
    def __get_history_info_from_tree(self, tree, flag):
        self.__get_time(tree)
        self.__get_price(tree)
        self.__get_property_type(tree)
        self.__get_property_info(tree)
        self.__get_property_features(tree)
        self.__get_property_description(tree)
        # set the values for analysis 
        self.__set_property_FlatHouse()
        self.__set_property_holding()
        self.__set_no_bedrooms()
        self.__set_no_baths()
        self.__set_no_receps()
        self.__set_listing_type()
        self.__set_listing_date()
        self.__set_listing_FlatHouse()
        self.__set_listing_no_bedrooms()
        self.__set_listing_price()
        self.__set_listing_furnished()
        
        if flag == self.config.FLAGS_CSV:
            self.save()
        elif flag == self.config.FLAGS_PRINT:
            self.print_from_zoopla()
    
    def __get_info_generic(self, word, target, flag, start, end):
        return_value = list()
        #len_target = len(target)
        if flag == self.config.FLAG_WORD_PRESENCE:
            
            position = target.find(word)
            #print("here info", word, target, position )
            return_value.extend([position])
        elif flag == self.config.FLAG_WORD_VAL:
            position = target.find(word)
            return_value.extend([position])
            val = target[(position + start):(position + start) + end]
            #print("here info", word, target, position, val )
            return_value.extend([val])
        return return_value
    def __set_property_FlatHouse(self):
        # Flat = 0 
        # Maisonette = 1
        # Mews house = 2
        # Semi- detached house = 3
        # Studio = 4
        # terraced house = 5 
        # town house = 6 
        Flat = self.__get_info_generic('Flat', self.parent_attributes , 0, 0, 0)
        #print("here ln 146", self.parent_attributes,"value:", Flat)
        Maisonette = self.__get_info_generic('Maoisonette', self.parent_attributes , 0, 0, 0)
        Mews_house = self.__get_info_generic('Mews house', self.parent_attributes , 0, 0, 0)
        Studio = self.__get_info_generic('Studio', self.parent_attributes , 0, 0, 0)
        Terraced_house = self.__get_info_generic('Terraced house', self.parent_attributes , 0, 0, 0)
        Town_house = self.__get_info_generic('Town house', self.parent_attributes , 0, 0, 0)
        if Flat[0] != -1:
            self.property_FlatHouse = 1
        elif Maisonette[0] != -1:
            self.property_FlatHouse = 2
        elif Mews_house[0] != -1:
            self.property_FlatHouse = 3
        elif Studio[0] != -1: 
            self.property_FlatHouse = 4
        elif Terraced_house[0] != -1 :
            self.property_FlatHouse = 5
        elif Town_house[0] != -1:
            self.property_FlatHouse = 6
    
    def __set_property_holding(self):
        # Freehold = 1
        # Leasehold = 2
        # Share of freehold = 3
        Freehold = self.__get_info_generic('Freehold', self.parent_attributes, 0, 0, 0)
        Leasehold = self.__get_info_generic('Leasehold', self.parent_attributes, 0, 0, 0)
        Share_freehold = self.__get_info_generic('Share of freehold', self.parent_attributes, 0, 0, 0)
        if Freehold[0] != -1:
            self.property_holding = 1
        elif Leasehold[0] != -1 :
            self.property_holding = 2
        elif Share_freehold[0] != -1 :
            self.property_holding = 3
            
    def __set_no_bedrooms(self):
        bedrooms = self.__get_info_generic('Bed', self.parent_attributes , 1, -2, 1)
        if bedrooms[0] != -1: 
            self.no_bedrooms = bedrooms[1]
    
    def __set_no_baths(self):
        baths = self.__get_info_generic('Bath', self.parent_attributes , 1, -2, 1)
        if baths[0] != -1: 
            self.no_baths = baths[1]
            
    def __set_no_receps(self):
        receps = self.__get_info_generic('Recep', self.parent_attributes , 1, -2, 1)
        if receps[0] != -1: 
            self.no_receps = receps[1]
    
    def __set_listing_type(self):
        rent = self.__get_info_generic('rent', self.time, 0, 0, 0)
        sale = self.__get_info_generic('sale', self.time, 0, 0, 0)
        if rent[0] != -1:
            self.listing_type = 'Rent'
        elif sale[0] != -1:
            self.listing_type = 'Sale'
    
    def __set_listing_date(self):
        date = self.__get_info_generic('on', self.time, 1, 3, len(self.time))
        if date[0] != -1:
            self.listing_date = date[1]
    
    def __set_listing_FlatHouse(self):
        # flat = 1
        # duplex = 2 
        # triplex = 3
        # maisonette = 4
        # terraced house = 5
        # semi-detached house = 6
        # studio = 7
        # mews house = 8
        Flat = self.__get_info_generic('flat', self.property_type , 0, 0, 0)
        duplex = self.__get_info_generic('duplex', self.property_type , 0, 0, 0)
        triplex = self.__get_info_generic('triplex', self.property_type , 0, 0, 0)
        Maisonette = self.__get_info_generic('maisonette', self.property_type , 0, 0, 0)
        Terraced_house = self.__get_info_generic('terraced house', self.property_type , 0, 0, 0)
        Detached_house = self.__get_info_generic('semi-detached house', self.property_type , 0, 0, 0)
        Studio = self.__get_info_generic('studio', self.property_type , 0, 0, 0)
        Mews_house = self.__get_info_generic('semi-detached house', self.property_type , 0, 0, 0)
        if Flat[0] != -1:
            self.listing_FlatHouse = 1
        elif duplex[0] != -1:
            self.listing_FlatHouse = 2
        elif triplex[0] != -1:
            self.listing_FlatHouse = 3
        elif Maisonette[0] != -1: 
            self.listing_FlatHouse = 4
        elif Terraced_house[0] != -1 :
            self.listing_FlatHouse = 5
        elif Detached_house[0] != -1:
            self.lisitng_FlatHouse = 6
        elif Studio[0] != -1:
            self.lisitng_FlatHouse = 7
        elif Mews_house[0] != -1:
            self.lisitng_FlatHouse = 8    
     
    def __set_listing_no_bedrooms(self):
        bedrooms = self.__get_info_generic('bed', self.property_type , 1, -2, 1)
        if bedrooms[0] != -1: 
            self.listing_no_bed = bedrooms[1]
    
    def __set_listing_price(self):
        price_num = self.price.replace('£','')
        price_num = price_num.replace(',','')
        price_num = price_num.replace('pcm','')
        self.listing_price = price_num
        
    def __set_listing_furnished(self):
        stick_tag_1 = 0
        stick_tag_2 = 0
        for i in range(len(self.property_info)):
            unfur_1 = self.__get_info_generic('unfurnished', self.property_info[i], 0, 0,0)
            unfur_2 = self.__get_info_generic('Unfurnished', self.property_info[i], 0, 0,0)
            fur_1 = self.__get_info_generic('furnished', self.property_info[i], 0, 0,0)
            fur_2 = self.__get_info_generic('Furnished', self.property_info[i], 0, 0,0)
            if unfur_1[0] != -1 or unfur_2[0] != -1:
                stick_tag_1 = 1       
            if fur_1 != -1 or fur_2 != -1:
                stick_tag_2 = 1
        if stick_tag_1 == 1:
            self.listing_Furnished = 'Unfurnished'
        if stick_tag_2 == 1:
            self.listing_Furnished = 'Furnished'
        
    def save(self):
        #print('save to csv')
        # write
        path = self.config.FILE_NAME_CSV + str(self.postcode) +".csv"
        with open(path, "a", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter= ',')
            line = []
            line.append(str(self.survey_id))
            line.append(str(self.postcode))
            line.append(str(self.parent_id))
            line.append(str(self.parent_address))
            line.append(str(self.micro_postcode))
            line.append(str(self.parent_attributes))
            line.append(str(self.history_id))
            line.append(str(self.time))
            line.append(str(self.history_date_val))
            line.append(str(self.price))
            line.append(str(self.property_type))
            line.append(str(self.property_FlatHouse))
            line.append(str(self.property_holding))
            line.append(str(self.no_bedrooms))
            line.append(str(self.no_baths))
            line.append(str(self.no_receps))
            line.append(str(self.listing_type))
            line.append(str(self.listing_date))
            line.append(str(self.listing_price))
            line.append(str(self.listing_FlatHouse))
            line.append(str(self.listing_no_bed))
            line.append(str(self.listing_Furnished))
            line.append(str(self.property_type))
            line.append(str('|'.join(self.property_info)))
            line.append(str('|'.join(self.property_features)))
            line.append(str(''.join(self.property_description)))
            writer.writerow(line)
    
    def print_from_zoopla(self):
        print_string = "Room_info:"
        print_string += "\n\tsurvey_id:\t" + str(self.survey_id)
        print_string += "\n\tpost code:\t" + str(self.postcode)
        print_string += "\n\tproperty_id:\t" + str(self.parent_id)
        print_string += "\n\tproperty_address:\t" + str(self.parent_address)
        print_string += "\n\tmicro_postcode:\t" + str(self.micro_postcode)
        print_string += "\n\tpropery_attributes:\t" + str(self.parent_attributes)
        print_string += "\n\troom_id:\t" + str(self.history_id)
        print_string += "\n\ttime:\t" + str(self.time)
        print_string += "\n\thistory_date_val:\t" + str(self.history_date_val)
        print_string += "\n\tprice:\t" + str(self.price)
        print_string += "\n\tproperty_flatHouse:\t" + str(self.property_FlatHouse)
        print_string += "\n\tproperty_holding:\t" + str(self.property_holding)
        print_string += "\n\tno_bedroom:\t" + str(self.no_bedrooms)
        print_string += "\n\tno_baths:\t" + str(self.no_baths)
        print_string += "\n\tno_receps:\t" + str(self.no_receps)
        print_string += "\n\tlisting_type:\t" + str(self.listing_type)
        print_string += "\n\tlisting_date:\t" + str(self.listing_date)
        print_string += "\n\tlisting_FlatHouse:\t" + str(self.listing_FlatHouse)
        print_string += "\n\tlisting_no_bed:\t" + str(self.listing_no_bed)
        print_string += "\n\tlisting_price:\t" + str(self.listing_price)
        print_string += "\n\tlisting_Furnished:\t" + str(self.listing_Furnished)
        print_string += "\n\tproperty type:\t" + str(self.property_type)
        print_string += "\n\tproperty info:\t" + str(self.property_info)
        print_string += "\n\tproperty features:\t" + str(self.property_features)
        print_string += "\n\tproperty_description:\t" +str(self.property_description)
        print(print_string)
        
    def save_null_history(self, flag):
        self.time = ""
        self.price = ""
        self.property_type = ""
        self.property_info = ""
        self.property_features = ""
        self.property_description = ""
        self.__set_property_FlatHouse()
        self.__set_property_holding()
        self.__set_no_bedrooms()
        self.__set_no_baths()
        self.__set_no_receps()
        if flag == self.config.FLAGS_CSV:
            self.save()
        elif flag == self.config.FLAGS_PRINT:
            self.print_from_zoopla()
        