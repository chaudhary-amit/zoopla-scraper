# zoopla-scraper
Code to scrape the history of property listings from zoopla website 

zoopla-scraper is a tool that allows data scientists to crape the history of property listings from zoopla website.

See data section of my paper: ***Effects of Airbnb on the Housing market: Evidence from London*** for more details.   
## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.4 or later vesrion  
* Dependency: lxml (either got the lxml website or use Anaconda distribution of python which included lxml


## Using zoopla-scraper script

To use zoopla-scraper, follow these steps:

Change following line in zoopla.py file to run on different post code. (I am in process of merging sql database code to main repo)  
```
survey = ZSurvey(ab_config, '<survey id>', '<post code>')
```
Run the code 
```
python zoopla.py 
```

Output is stored in Zoopla_data_<post code>.csv file. 

[Sample output for this project](sample/Zoopla_data_NW6.csv) 
