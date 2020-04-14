# -*- coding: utf-8 -*-
import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
#from scrapy import JsonRequest
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider

import json
import re
import scrapy

from datetime import date, timedelta
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from airbnb.items import AirbnbItem

#from deepbnb.items import DeepbnbItem

import requests
#import requests
#import time
#import argparse
#import urlparse

#import selenium
from scrapy.selector import Selector
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#chrome_options = webdriver.ChromeOptions()


#driver = webdriver.Chrome('/home/ari/ohjelmistotiedostot/chromedriver/chromedriver', chrome_options=chrome_options)
#driver.get('https://www.airbnb.com/s/Helsinki--Finland/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki%2C%20Finland&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&source=structured_search_input_header&search_type=search_query')


#crapy_selector = Selector(text = driver.page_source)
#scrapy_selector.xpath('//*[@itemtype="http://schema.org/ListItem"]')

#print(scrapy_selector)


print("testi päätyy ____________________________________")
class AirbnbSpiderSpider(scrapy.Spider):
    name = 'airbnb_spider'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['https://www.airbnb.com/']
    #url = ['https://www.airbnb.com/s/Helsinki/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&checkin=2020-04-14&checkout=2020-04-15&adults=1&source=structured_search_input_header&search_type=search_query']
    url =['https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&client_session_id=6c7f3e7b-c038-4d92-b2b0-0bc7c25f1054%C2%A4cy=EUR&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-CA&luxury_pre_launch=false&metadata_only=false&place_id=ChIJ21P2rgUrTI8Ris1fYjy3Ms4&query=Helsinki%2C%20Finland&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=b7cT9Z3U&satori_version=1.1.9&screen_height=948&screen_size=medium&screen_width=1105&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=-240&version=1.5.7&checkin=2020-04-14&checkout=2020-04-15&adults=1']
    default_currency = 'EUR'

    offset_str = '&items_offset='
    listing_url_beginning = 'https://www.airbnb.com/api/v2/pdp_listing_details/'

    listing_url_end = '?_format=for_rooms_show&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'
    listing_url_checkin_checkout = '&checkin=2020-04-14&checkout=2020-04-15'
    guests = '&adults=1'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'test.csv'
    }
    
    #default_max_price = 2000
    #default_min_price = 100
    #default_price_increment= 100
    #price_range = (0, default_max_price, default_price_increment)
    #page_limit = 20
    #start_urls = 
    #query = "Helsinki, Finland"

    # def __init__(
    #         self,
    #         #query,
    #         checkin=None,
    #         checkout=None,
    #         currency=default_currency,
    #         max_price=None,
    #         min_price=None,
    #         ne_lat=None,
    #         ne_lng=None,
    #         sw_lat=None,
    #         sw_lng=None,
    #         **kwargs
    # ):
    #     """Class constructor."""
    #     super().__init__(**kwargs)
    #     self._api_key = None
    #     self._checkin = checkin
    #     self._checkout = checkout
    #     self._currency = currency
    #     self._data_cache = {}
    #     self._geography = {}
    #     self._ids_seen = set()
    #     self._ne_lat = ne_lat
    #     self._ne_lng = ne_lng
    #     self._place = query
    #     self._search_params = {}
    #     self._set_price_params(max_price, min_price)
    #     self._sw_lat = sw_lat
    #     self._sw_lng = sw_lng


    def start_requests(self):
        url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&client_session_id=6c7f3e7b-c038-4d92-b2b0-0bc7c25f1054%C2%A4cy=EUR&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-CA&luxury_pre_launch=false&metadata_only=false&place_id=ChIJ21P2rgUrTI8Ris1fYjy3Ms4&query=Helsinki%2C%20Finland&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=b7cT9Z3U&satori_version=1.1.9&screen_height=948&screen_size=medium&screen_width=1105&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=-240&version=1.5.7')
        #url = ('https://www.airbnb.ca/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&client_session_id=6c7f3e7b-c038-4d92-b2b0-0bc7c25f1054%C2%A4cy=CAD&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en-CA&luxury_pre_launch=false&metadata_only=false&place_id=ChIJ21P2rgUrTI8Ris1fYjy3Ms4&query=Helsinki%2C%20Finland&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=b7cT9Z3U&satori_version=1.1.9&screen_height=948&screen_size=medium&screen_width=1105&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=-240&version=1.5.7')
        #url = ['https://www.airbnb.com/s/Helsinki/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&checkin=2020-04-14&checkout=2020-04-15&adults=1&source=structured_search_input_header&search_type=search_query']
        #url = ('https://www.airbnb.com/s/Helsinki/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Helsinki&place_id=ChIJkQYhlscLkkYRY_fiO4S9Ts0&checkin=2020-04-12&checkout=2020-04-13&adults=1&source=structured_search_input_header&search_type=search_query')
        #url = ('https://www.airbnb.com/s/helsinki/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query')
        #first = False
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        #data = json.loads(response.text)
        tab = data['explore_tabs'][0]

        ## Handling pagination
        next_section = {}
        pagination = tab['pagination_metadata']
        has_next_page = self.has_next_page(data)
        print("************* NEXT PAGE: ", has_next_page)
        offset = data.get('explore_tabs')[0]['pagination_metadata']['items_offset']

        #gen_listings = data.get('explore_tabs')[0].get('sections')[2]
        listings = None
        if offset > 18:
            # When on first page, offset is 18. After this, the listings are in another section.
            listings = data.get('explore_tabs')[0].get('sections')[0].get('listings')
        else:
            listings = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        j = 0
        for i in listings:
            i = i.get('listing')
            # Pricing quote is not under listings, so we need to do this
            pricing_quote = listings[j].get('pricing_quote')
            # Information about the host, like whether they're verified
            verified = listings[j].get('verified')
            id = i.get('id')
            listing_url = self.get_listing_url(id)
            #yield scrapy.JsonRequest(url=listing_url, callback=self.parse_listing_contents)



            #pricing_quote = self.get_pricing_quote(gen_listings, j)
            #yield scrapy.Request(i, pricing_quote, verified, callback=self.parse_listing)
            item = AirbnbItem()

            item['id'] = i.get('id')
            item['name'] = i.get('name')
            item['is_business_travel_ready'] = i.get('is_business_travel_ready')
            item['is_new_listing'] = i.get('is_new_listing')
            item['is_super_host'] = i.get('is_superhost')

            item['kicker_content_message'] = i.get('kicker_content').get('messages')[0]


            item['latitude'] = i.get('lat')
            item['longitude'] = i.get('lng')
            item['localized_city'] = i.get('localized_city')
            item['localized_neighborhood'] = i.get('localized_neighborhood')
            item['neighborhood'] = i.get('neighborhood')

            item['person_capacity'] = i.get('person_capacity')
            item['picture_count'] = i.get('picture_count')
            item['preview_amenities'] = i.get('preview_amenities')
            item['property_type_id'] = i.get('property_type_id')
            item['reviews_count'] = i.get('reviews_count')
            item['room_and_property_type'] = i.get('room_and_property_type')
            item['room_type_category'] = i.get('room_type_category')
            item['room_type'] = i.get('room_type')
            item['space_type'] = i.get('space_type')
            item['star_rating'] = i.get('star_rating')
            item['avg_rating'] = i.get('avg_rating')
            item['min_nights'] = i.get('min_nights')
            item['max_nights'] = i.get('max_nights')
            item['cancel_policy'] = i.get('cancel_policy')

            # Pricing quote -osuuden hakeminen
            item['can_instant_book'] = pricing_quote.get('can_instant_book')
            item['monthly_price_factor'] = pricing_quote.get('monthly_price_factor')
            item['price_string'] = pricing_quote.get('price_string')
            item['rate_type'] = pricing_quote.get('rate_type')
            item['weekly_price_factor'] = pricing_quote.get('weekly_price_factor')
            #can_instant_book = listing.get('pricing_quote').get('can_instant_book')


            item['host_verified'] = verified.get('enabled')
            #self.parse_listing_contents(id)
            item['bedrooms'] = i.get('bedrooms')
            item['bedroom_label'] = i.get('bedroom_label')
            item['beds'] = i.get('beds')
            item['bathrooms'] = i.get('bathrooms')
            item['city'] = i.get('city')

            #item = 


            item['listing_url'] = self.get_listing_url(id)

            yield item


            #self.parse_listing(i, pricing_quote, verified)
            #yield item
            #self.parse_listing(i, pricing_quote, verified)
            j = j +1

        if has_next_page:
            url = self.url[0]+self.offset_str+str(offset)
            print()
            print("***************URL: ", url)
            yield scrapy.Request(url=url, callback=self.parse)

        # bathrooms2 = listings[0].get('listing').get('bathrooms')
        # print("**********BATHROOMS2: ", bathrooms2)

        # print("************************LENLISTINGS: ", len(listings))
        # print(len(listings))

        

        # bathrooms1 = data.get('explore_tabs')[0].get('sections')[2].get('listings')[0].get('listing').get('bathrooms')
        # print("***********bathrooms1")
        # print(bathrooms1)
        # #listing = listings.extract()
        # #print(listing)
        # print("***************LISTINGS")
        # #print(listings.text)
        # #view(listings)



        # # Next page?
        # # if pagination['has_next_page']:
        # #     items_offset = pagination['items_offset']
        # #     print("items offset: ", items_offset)
        # #     #AirbnbSpiderSpider._add_search_params(next_section, response)
        # #     next_section.update({'items_offset': items_offset})

        # #     # Jäi kusemaan tästä
        # #     yield self._api_request(params = next_section, response=response)
        


        

        # # Next page


        # #offset = data.get('explore_tabs')[0]['pagination_metadata']['items_offset']
        # #print("*********** OFFFSET: ", offset)
        # #has_next_page = data.get('explore_tabs')[0]['pagination_metadata']['has_next_page']
        

        # listings = self.get_listings(data)
        # print('__________-------------_______________________')
        # #print(listings)
        # print('__________-------------_______________________')

        # #listings = data.get('explore_tabs')[0].get('sections')[1].get('listings')
        # #logging.log(logging.DEBUG, '"******LISTINGS***"' + listings)

        # BASE_URL = 'https://www.airbnb.com/rooms/'




        # # last_page_number = self.last_pagenumer_in_search(response)
        # # print("-----------------------")
        # # print("last_page_number: ", last_page_number)
        # # print("-----------------------")
        # has_next_page = True

        


        # #### OFFSETIN HAKEMINEN ONNISTUU NÄIN
        # # Vinkki tähän saatu täältä: https://gist.github.com/prehensile/aed87c98677da07c8f042cd019a04ebf0
        # offset = data.get('explore_tabs')[0]['pagination_metadata']['items_offset']
        # print("******OFFSET***")
        # print(offset)

        # # Ei osaa vielä hakea Listingssejä
        # # https://gist.github.com/prehensile/aed87c98677da07c8f042cd01904ebf0/380524e7cb9f7f9e91548b8cbf2b1b3cf77c7f50#file-airbnb-search-py-L28
        # #page_data = get_bootstrap_data_for_hypernova_key( buf, "spaspabundlejs" )
        # #section = page_data["bootstrapData"]["reduxData"]["exploreTab"]["response"]["explore_tabs"][0]["sections"][0]
        # #listings = section["listings"]
        # #items_offset = page_data["bootstrapData"]["reduxData"]["exploreTab"]["response"]["explore_tabs"][0]["pagination_metadata"]["items_offset"]

        # homes_sections = data.get('explore_tabs')[0]['sections'][0]


        # #### LISTINGSEIHIN PÄÄSEE KÄSIKSI NÄIN:
        # #homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        # #print("****** homes_sections****")
        # #print(homes_sections)
        # #home_section = homes_sections['listings']
        # #print("****** homes_section ****")
        # #print(home_section)


        # #homes = data.get('explore_tabs')[0].get('sections')[3].get('listings')

        # #BASE_URL = "airbnb.ca"


        # last_page_number = self.last_page_in_search(response)
        # print("***********************************")
        # print("Seuraavassa sivunumero: ")
        # print(last_page_number)

        _file_ = "first_page_nyt.json"
        with open(_file_, 'wb') as f:
            f.write(response.body)


    #def parse_listing_contents(self, response):
        #item = 
    def get_listing_url(self, listing_id):
        listing_url = self.listing_url_beginning+str(listing_id)+self.listing_url_end+self.listing_url_checkin_checkout+self.guests
        print("_________LISTINGURL")
        print(listing_url)
        return listing_url

    def get_listing_page(self, listing_id):
        listing_url = self.get_listing_url(listing_id)
        
        return scrapy.Request(listing_url, self.parse_listing)

    
    def parse_listing_contents(self, response):
        print("************LISTING CONTENTS")
        #print(response.text)
        response = response.text
        #data = self.read_data(response)
        #print(data)
        #data = json.loads(response.text)
        #print(data)
        #listing_page =  json.loads(response.body)
        #listing_page = self.get_listing_page(listing_id)
        #print(listing_page)
        #listing_data = json.loads(listing_page.body)
        #data = json.loads(response)

        #print(data)


        pdp = response.get('listing_detail')
        additional_house_rules = pdp.get('additional_house_rules')




        print("**********************PARSE LISTING CONTENTS")
        #listing_page = self.get_listing_page(response)

        #pdp = listing_page.get('listing_detail')
        additional_house_rules = pdp.get('additional_house_rules')
        print("*********** ADDITIONAL HOUSE RULES")
        print(additional_house_rules)


    def read_data(self, response):
        self.logger.debug(f"Parsing {response.url}")
        data = json.loads(response.body)
        return data


    def parse_listing(self, listing, pricing_quote, verified):
        item = AirbnbItem()

        item['id'] = listing.get('id')
        item['name'] = listing.get('name')
        item['is_business_travel_ready'] = listing.get('is_business_travel_ready')
        item['is_new_listing'] = listing.get('is_new_listing')
        item['is_super_host'] = listing.get('is_superhost')

        item['kicker_content_message'] = listing.get('kicker_content').get('messages')[0]


        item['latitude'] = listing.get('lat')
        item['longitude'] = listing.get('lng')
        item['localized_city'] = listing.get('localized_city')
        item['localized_neighborhood'] = listing.get('localized_neighborhood')
        item['neighborhood'] = listing.get('neighborhood')

        item['person_capacity'] = listing.get('person_capacity')
        item['picture_count'] = listing.get('picture_count')
        item['preview_amenities'] = listing.get('preview_amenities')
        item['property_type_id'] = listing.get('property_type_id')
        item['reviews_count'] = listing.get('reviews_count')
        item['room_and_property_type'] = listing.get('room_and_property_type')
        item['room_type_category'] = listing.get('room_type_category')
        item['room_type'] = listing.get('room_type')
        item['space_type'] = listing.get('space_type')
        item['star_rating'] = listing.get('star_rating')
        item['avg_rating'] = listing.get('avg_rating')
        item['min_nights'] = listing.get('min_nights')
        item['max_nights'] = listing.get('max_nights')
        item['cancel_policy'] = listing.get('cancel_policy')

        # Pricing quote -osuuden hakeminen
        item['can_instant_book'] = pricing_quote.get('can_instant_book')
        item['monthly_price_factor'] = pricing_quote.get('monthly_price_factor')
        item['price_string'] = pricing_quote.get('price_string')
        item['rate_type'] = pricing_quote.get('rate_type')
        item['weekly_price_factor'] = pricing_quote.get('weekly_price_factor')
        #can_instant_book = listing.get('pricing_quote').get('can_instant_book')


        item['host_verified'] = verified.get('enabled')
        #self.parse_listing_contents(id)
        item['bedrooms'] = listing.get('bedrooms')
        item['bedroom_label'] = listing.get('bedroom_label')
        item['beds'] = listing.get('beds')
        item['bathrooms'] = listing.get('bathrooms')
        item['city'] = listing.get('city')

        #item = 


        item['listing_url'] = self.get_listing_url(id)
        #yield scrapy.Request(listing_url, callback=self.parse_listing_contents)

        #listing_url = self.get_listing_url(id)

        # print("********** id: ", id)
        # print('********* Name: ', name)
        # print("********* is business travel ready: ", is_business_travel_ready)
        # print("********* new? ", is_new_listing)
        # print("********* is_super_host: ", is_super_host)
        # print("********* kicker: ", kicker_content_message)
        # print("*********bedrooms: ", bedrooms)
        # print("********* bedroom_label: ", bedroom_label)
        # print("********* beds: ", beds)
        # print("*********BATHROOMS2 METODISTA:", bathrooms2)
        # print("********* city: ", city)
        # print("********* can_instant_book: ", can_instant_book)
        # print("********* monthly: ", monthly_price_factor)
        # print('********* pricing_string: ', price_string)
        # print("********* rate_type: ", rate_type)
        # print("********* weekly: ", weekly_price_factor)
        # print("********* host verified: ", host_verified)
        #print(item)
        yield (item)
        #yield {'id': id}

        

    #def parse_listing_results_page(self, response):
    #def has_next_page(self, )

    def get_pricing_quote(self, response, number):
        pricing_quote = response[number].get('pricing_quote')
        return pricing_quote

    def get_pricing_quote(self, listing):
        quote = listing.get('pricing_quote')
        return quote

    def has_next_page(self, data):
        return data.get('explore_tabs')[0]['pagination_metadata']['has_next_page']


    
    def get_listings(self, data):

        print("SAATTOI HAKEA LISTINGSIT=================0")

        data.get('explore_tabs')[0].get('sections')
        listings = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        #print('__________-------------_______________________')
        #print(listings)
        #logging.log(logging.DEBUG, '***************LISTINGS***************' , listings)
        #print('__________-------------_______________________')
        return listings

    #def parse_listings(self, data):



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

    # def _api_requests(self, params=None, response=None, callback=None):
    #     """ Perform API request."""
    #     if response:
    #         request = response.follow
    #     else:
    #         request = scrapy.Request
        
    #     callback = callback or self.parse

    #     return request(self.get_sear)

    # def _get_search_api_url(self, params=None):
    #     _api_path = '/api/v2/explore_tabs'
    #     if self._api_key is None:
    #         self._api_key = self.settings.get("AIRBNB_API_KEY")

    #     query = {
    #         '_format':                       'for_explore_search_web',
    #         'auto_ib':                       'true',  # was false?
    #         'currency':                      self._currency,
    #         'current_tab_id':                'home_tab',
    #         'experiences_per_grid':          '20',
    #         # 'federated_search_session_id': '',
    #         'fetch_filters':                 'true',
    #         'guidebooks_per_grid':           '20',
    #         'has_zero_guest_treatment':      'false',
    #         'hide_dates_and_guests_filters': 'false',
    #         'is_guided_search':              'true',
    #         'is_new_cards_experiment':       'true',
    #         'is_standard_search':            'true',
    #         # 'items_offset': '0',
    #         'items_per_grid':                '50',
    #         'key':                           self._api_key,
    #         # 'last_search_session_id': '',
    #         'locale':                        'en',
    #         'metadata_only':                 'false',
    #         # 'neighborhood_ids[]': ,
    #         # 'place_id': '',
    #         # 'price_max': None,
    #         # 'price_min': 10,
    #         'query':                         self._place,
    #         'query_understanding_enabled':   'true',
    #         'refinement_paths[]':            '/homes',
    #         'room_types[]':                  'Entire home/apt',
    #         'satori_version':                '1.2.0',
    #         # 'section_offset': '0',
    #         'screen_height':                 635,
    #         'screen_size':                   'large',
    #         'screen_width':                  2040,
    #         'show_groupings':                'true',
    #         'supports_for_you_v3':           'true',
    #         'timezone_offset':               '-480',
    #         'version':                       '1.6.5'
    #     }

    #     if params:
    #         query.update(params)

    #     if self.settings.get('PROPERTY_AMENITIES'):
    #         amenities = self.settings.get('PROPERTY_AMENITIES').values()
    #         query = list(query.items())  # convert dict to list of tuples because we need multiple identical keys
    #         for a in amenities:
    #             query.append(('amenities[]', a))

    #     return self._build_airbnb_url(_api_path, query)