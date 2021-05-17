# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:49:46 2017

@author: Amit Chaudhary 
"""

# file for debugging requests as spyder qt lib not supporting lxml debug 

from lxml import html
import requests
import zoopla_rq
import csv

from airbnb_config import ABConfig
x = ABConfig()
 #page = requests.get(property_url)
#tree = html.fromstring(page.content)

# this url for the single history 
test_url = 'https://www.zoopla.co.uk/property/7866464'

#test_url = 'https://www.zoopla.co.uk/property/25466449'



#test_url = 'https://www.zoopla.co.uk/house-prices/wc1x-8qf'


#response = zoopla_rq.rq_request_with_repeats(x, test_url)
#tree = html.fromstring(response.text)
page = requests.get(test_url)
tree = html.fromstring(page.content)

history_url_return = list()
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
        
        
print('history_url ',history_url)
#history_time = tree.xpath('//a[@class="time link"]/@href')
history_url_return.append(history_url)
history_url_return.append(history_date)

str('|'.join(['a','2','3']))

str(''.join(['View more details about this Flat to rent in Islington', '', 'Located on a quiet sought-after residential street, this spacious two bedroomed flat has been recently refurbished to a high standard throughout and benefits from bright and airy living spaces. Set on the raised ground floor it also comprises a large reception room with access to the communal garden, kitchen, two good-sized bedrooms, smart bathroom, separate WC and off-street parking. Alwyne Road is located in Canonbury within easy reach of the vast and varied range of shops, bars and restaurants of Upper Street while providing motorists with easy access to the A1 road links out of London and to the north. The nearest underground station is Highbury & Islington (Victoria Line, National rail).', '', 'How much is your property worth?']))



history_date = tree.xpath('//a[@class="year-history-link"]/text()')
if not history_date:
            history_single_url = tree.xpath('//div[@id = "historic-result"][@class = "clearfix top"]//strong/a/@href')
            if history_single_url:
                history_date = history_single_url
                history_year.append('2100') 
                
                
history_url = tree.xpath('//div[@id = "historic-result"][@class = "clearfix top"]//strong/a/@href')



history_url = tree.xpath('//a[@class="year-history-link"]/@href')
history_date = tree.xpath('//a[@class="year-history-link"]/text()')
history_year = list()
for i in range(len(history_date)):
            tmp = tree.xpath('//a[@class="year-history-link"][text()= "{}"]//preceding-sibling::span[@class="year-history-heading"]'.format(history_date[i]))
            tmp_1 = tmp[0].text
            print(tmp_1)
            history_year.append(str(tmp_1))




print('//a[@class="year-history-link"][text()= "{}"]//preceding-sibling::span[@class="year-history-heading"]'.format(history_date[0]))
                            
year_date = tree.xpath('//a[@class="year-history-link"][text()= "{}"]//preceding-sibling::span[@class="year-history-heading"]'.format(history_date[5]))

print(year_date[0].text)

ancestor::a[@class="year-history-link"]
/a[@class="year-history-link"]/text()

print(history_date[1].getparent().text) 


prop_add = tree.xpath('//td[@class="browse-cell-address"]/div[@class="attributes"]/text()')

test = tree.xpath('//a[@class="year-history-link"]/text()')
history_date = test
history_date = [j.strip() for j in history_date]
#time 
temp = tree.xpath('//p[@id="historic-listing-title"]/strong/text()')
time = temp[0].strip()
time = time.replace('\n', '')

#price 
temp = tree.xpath('//strong[@class="buyers"]/text()')
price = temp[0].strip()

#type
temp = tree.xpath('//strong[@class="nobold"]/text()')
property_type = temp[0].strip()

#info
temp = tree.xpath('//ul[@class="listing-content clearfix noprint"]/li/text()')
property_info = temp 

#features
features = tree.xpath('//div[@class="historic-listing-old"]/div/div/ul//li//text()')
features = [j.strip() for j in features]


#desc
temp = tree.xpath('//div[@itemprop="description"]//text()')
property_description = temp
property_description = [j.strip() for j in property_description]

path = "test.csv"
with open(path, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter= ',')
    line = []
    line.append(time)
    line.append(price)
    line.append(property_type)
    line.append(property_info)
    line.append(str(features))
    line.append(property_description)
    writer.writerow(line)