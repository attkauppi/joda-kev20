# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    is_business_travel_ready = scrapy.Field()
    is_new_listing = scrapy.Field()
    is_super_host = scrapy.Field()

    kicker_content_message = scrapy.Field()


    latitude = scrapy.Field()
    longitude = scrapy.Field()
    localized_city = scrapy.Field()
    localized_neighborhood = scrapy.Field()
    neighborhood = scrapy.Field()

    person_capacity = scrapy.Field()
    picture_count = scrapy.Field()
    preview_amenities = scrapy.Field()
    property_type_id = scrapy.Field()
    reviews_count = scrapy.Field()
    room_and_property_type = scrapy.Field()
    room_type_category = scrapy.Field()
    room_type = scrapy.Field()
    space_type = scrapy.Field()
    star_rating = scrapy.Field()
    avg_rating = scrapy.Field()
    min_nights = scrapy.Field()
    max_nights = scrapy.Field()
    cancel_policy = scrapy.Field()

    # Pricing quote -osuuden hakeminen
    can_instant_book = scrapy.Field()
    monthly_price_factor = scrapy.Field()
    price_string = scrapy.Field()
    rate_type = scrapy.Field()
    weekly_price_factor = scrapy.Field()
    #can_instant_book = listing.get('pricing_quote').get('can_instant_book')


    host_verified = scrapy.Field()
    #self.parse_listing_contents(id)
    bedrooms = scrapy.Field()
    bedroom_label = scrapy.Field()
    beds = scrapy.Field()
    bathrooms = scrapy.Field()
    city = scrapy.Field()
    

    pass


class CompleteAirbnbItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    neighborhood = scrapy.Field()
    localized_neighborhood = scrapy.Field()
    localized_city = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    person_capacity = scrapy.Field()
    pass
