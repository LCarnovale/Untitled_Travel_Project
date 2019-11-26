import re
from datetime import datetime
from geopy.distance import geodesic
import src.review
from src.accommodation import Accommodation

class Search():
    '''
    Search object for encapsulating search logic.
    Usage:
    x = Search(items) # See __init__
    result = x.advancedSearch(...) # See advanced search for details
    '''

    def __init__(self, items):
        '''
        Initialise the Search class
        items: a dictionary of id: Accommodation, as in AccommodationSystem._accommodations
        '''
        self._items = items
        self._scores = []    
        self._most_recent = [] 

    def advancedSearch(self, search, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        '''
        Performs an advanced search on the items given in initialisation.

        This works by giving each item a score, and then ranking them with the highest score first

        All arguments should be strings, as follows:
        search: Text representing the keyword search, can be set to '' or None if no keywords.
        startdate: dd/mm/YYYY, represents the start of the period searched.
        enddate: dd/mm/YYYY, represents the end of the period searched.
        beds: Should be a positive number (as a string), representing number of bedrooms searched
        bathrooms: As with beds, for bathrooms
        parking: As with beds, for number of car spaces
        location: Should be two comma-separated floats, representing latitude and longitude of location search
        distance: Should be an integer representing the number of metres away from the location (radius) to search
        '''
        self._scores = []

        if len(self._items) == 0:
            return []

        # Generates scores based on the keyword search.
        if search:
            self._keywordSearch(search)
        else:
            self._scores = [(x,0.0) for x in self._items]
        
        # Filter by date range
        startdate = datetime.strptime(startdate, '%d/%m/%Y')
        enddate = datetime.strptime(enddate, '%d/%m/%Y')
        self._filterDates(startdate, enddate)
        
        # Optimisation for early return if no results are found
        if not self._scores:
            return self._scores

        # Filter by amenities.
        if beds:
            self._filterBeds(int(beds))
        if bathrooms:
            self._filterBaths(int(bathrooms))
        if parking:
            self._filterParking(int(parking))
		
        # Adding scores based on reviews
        self._scoreReviews()
        # Searching by distance
        if location:
            if not distance:
                distance = '2000'

            distance = int(distance)
            self._filterLocation(location, distance)

        # Sorting the results, highest score first
        self._scores = sorted(self._scores,key = lambda score: score[1], reverse = True)
        return [x[0] for x in self._scores]


    def _keywordSearch(self, search):
        '''Gives each result a score between 0 and 3 based on how well it matches the search'''
        search = self._cleanString(search)
        search = search.split(' ')

        scores = []

        for ad_id in self._items:
            ad = self._items[ad_id]
            title_score = 0.0
            body_score = 0.0

            name = ad.name
            name = self._cleanString(name)
            name = name.split(' ')

            desc = ad.description
            desc = self._cleanString(desc)
            desc = desc.split(' ')

            for keyword in search:
                if len(name) != 0:
                    title_score += 2 * name.count(keyword)/len(name)
                if len(desc) != 0:
                    body_score += 1 * desc.count(keyword)/len(desc)
            scores.append((ad_id, title_score + body_score))

        self._scores = scores


    def _filterDates(self, startdate, enddate):
        '''Filters out all results which are unavailable/booked during the period specified'''
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            dates = ad.get_dates()

            for start, end in dates:
                start = datetime.strptime(start, '%d-%m-%Y')
                end = datetime.strptime(end, '%d-%m-%Y')

                if start <= startdate and end >= enddate:
                    result.append((ad_id, score))

        self._scores = result


    def _filterBeds(self, beds):
        '''Filters out all results which don't have enough beds. +0.5 points if exact num of beds.'''
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]

            if (ad.bed_count >= beds):
                if ad.bed_count == beds:
                    score+=0.5

                result.append((ad_id, score))

        self._scores = result


    def _filterBaths(self, baths):
        '''Filters out all results which don't have enough bathrooms. +0.5 points if exact num of bathrooms.'''
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]

            if (ad.bath_count >= baths):
                if ad.bath_count == baths:
                    score+=0.5

                result.append((ad_id, score))

        self._scores = result


    def _filterParking(self, spots):
        '''Filters out all results which don't have enough parking. +0.5 points if exact num of car spots.'''
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]

            if (ad.car_count >= spots):
                if ad.car_count == spots:
                    score+=0.5

                result.append((ad_id, score))

        self._scores = result


    def _scoreReviews(self):
        '''Adds 1 point for every positive review at the place, subtracts 1 for each negative review.'''
        result = []
        for id,score in self._scores:
            reviews = src.review.get_for_venue(id)

            for review in reviews:
                if review._recommends:
                    score+= 1.0 
                else:
                    score-= 1.0

            result.append((id, score))

        self._scores = result


    def _filterLocation(self, location, max_dist):
        '''
        Filters out every location outside of the given radius max_dist
        Ranks the results based on distance, and gives points between 2 
		and 0 based on proximity
        '''

        result = []
        lat = float(location.split(',')[0])
        lon = float(location.split(',')[1])

        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            dist = geodesic((lat, lon), (ad.address.lat, ad.address.lng)).km

            if (dist <= max_dist/1000):
                result.append((ad_id, score, dist))

        # Order results and score accordingly
        result.sort(key = lambda x: x[2])
        final = []
        for ad_id, score, dist in result:
            final.append((ad_id, score+ (max_dist-dist)/max_dist*2.0))

        self._scores = final


    def _cleanString(self, string):
        '''
        Replaces all contiguous non-alphanumeric characters with a space
        And converts to lower case
        '''
        return re.sub(r'[\W_]+', ' ', string).lower()