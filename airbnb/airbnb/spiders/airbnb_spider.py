# -*- coding: utf-8 -*-
import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider


class AirbnbSpiderSpider(scrapy.Spider):
    name = 'airbnb_spider'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['https://www.airbnb.com/']


    def start_requests(self):
        url = ('https://www.airbnb.ca/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&client_session_id=6c7f3e7b-c038-4d92-b2b0-0bc7c25f1054%C2%A4cy=CAD&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-CA&luxury_pre_launch=false&metadata_only=false&place_id=ChIJ21P2rgUrTI8Ris1fYjy3Ms4&query=Helsinki%2C%20Finland&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=b7cT9Z3U&satori_version=1.1.9&screen_height=948&screen_size=medium&screen_width=1105&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=-240&version=1.5.7')
        yield scrapy.Request(url=url, callback=self.parse)

    
    
    def parse(self, response):

        has_next_page = True




        last_page_number = self.last_page_in_search(response)
        print("***********************************")
        print("Seuraavassa sivunumero: ")
        print(last_page_number)

        _file_ = "first_page_nyt.json"
        with open(_file_, 'wb') as f:
            f.write(response.body)


    def last_page_in_search(self, response):
        try:
            last_page_number = int(response
                               .xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
                               .extract()[0]
                               .split('page=')[1]
                               )
            return last_page_number
        except IndexError: #If only one page of results

            # Get reason from the page
            reason = response.xpath('//p[@class="text-lead"]/text()').extract()
            # and if it contains the keywords set last page equal to 0
            if reason and ('find any results that matched yours criteria' in reason[0]):
                logging.log(logging.DEBUG, 'No results on page' + response.url)
                return 0
            else:
                # Otherwise we can conclude that the page has resulsts but that there is only
                # one page of them
                return 1
