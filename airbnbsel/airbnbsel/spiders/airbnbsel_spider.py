# -*- coding: utf-8 -*-
#import scrapy
# -*- coding: utf-8 -*-

# Lähteinä: https://towardsdatascience.com/web-scraping-a-less-brief-overview-of-scrapy-and-selenium-part-ii-3ad290ce7ba1


import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider

import requests
import requests
import time
import argparse
#mport urlparse
from bs4 import BeautifulSoup

import selenium
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome('/home/ari/ohjelmistotiedostot/chromedriver/chromedriver', chrome_options=chrome_options)
driver.get('https://www.airbnb.com/s/Helsinki--Finland/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki%2C%20Finland&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&source=structured_search_input_header&search_type=search_query')


scrapy_selector = Selector(text = driver.page_source)
scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')


class AirbnbselSpiderSpider(scrapy.Spider):
    name = 'airbnbsel_spider'
    allowed_domains = ['www.airbnb.com']
    #start_urls = ['http://www.airbnb.com/']
    start_urls = ['https://www.airbnb.com/s/Helsinki--Finland/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki%2C%20Finland&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&source=structured_search_input_header&search_type=search_query']


    def start_requests(self):
        driver.get('https://www.airbnb.com/s/Helsinki--Finland/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki%2C%20Finland&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&source=structured_search_input_header&search_type=search_query')

        time.sleep(15)

        scrapy_selector = Selector(text = driver.page_source)
        #scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')
        
        # homes_selector = scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')
        # #print("There's a total of " + str(len(homes_selector)) + " links")
        # links = []
        # i = 0
        # for home_selector in homes_selector:
        #     url = home_selector.xpath('//*[@itemprop = "url"]/@content').extract()[i]
        #     # Nyt url:t toimivat
        #     url = 'https://' + url.replace('undefined', 'airbnb.com')
        #     print(url)
        #     i = i +1

        yield scrapy.request


        home_links = self.get_home_links(scrapy_selector)

        print("**** HOME LINKS")
        #print(home_links)

        yield scrapy_selector

    def get_home_links(self, scrapy_selector):
        home_links = []


        homes_selector = scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')
        #print("There's a total of " + str(len(homes_selector)) + " links")
        links = []
        i = 0
        for home_selector in homes_selector:
            url = home_selector.xpath('//*[@itemprop = "url"]/@content').extract()[i]
            # Nyt url:t toimivat
            url = 'https://' + url.replace('undefined', 'airbnb.com')
            print(url)
            i = i +1
            home_links.append(url)
        return home_links
        
        #homes_selector = scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')

        # try:
        #     s = 0  
        #     for home_selector in homes_selector:
        #         url = home_selector.xpath('//*[@itemprop = "url"]/@content').extract()[s]

        #         print(url)

        #         # If you wanted to not take in to account 'rooms plus', you could do this
        #         if '/rooms/plus/' not in url:
        #             home_link = 'https://' + url.replace('adults=0&children=0&infants=0&guests=0','adults=1&guests=1&toddlers=0')
        #             home_links.distinct.append(home_link)
        #             s = s+1
        #         else:
        #             s = s+1
        # except:
        #     self.logger.info('Reached last iteration #' + str(s))

        # return home_links                    









    def parse(self, response):
        pass
