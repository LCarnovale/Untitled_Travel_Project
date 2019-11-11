import re
from datetime import datetime
from geopy.distance import geodesic

from src.accommodation import Accommodation

class Search():
    def __init__(self, items):
        self._items = items
        self._scores = []
        self._most_recent = []

    def advancedSearch(self, search, text_bounds, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        self._scores = []
        print('ADV search')

        if search:
            self._keywordSearch(search)
        else:
            self._scores = [(x,0.0) for x in self._items]
            #print(self._scores)

        print('Done keys')

        if text_bounds:
            self._limitRegion(text_bounds)

        print('Done region')

        if startdate:
            startdate = datetime.strptime(startdate, '%d/%m/%Y')
        else:
            startdate = datetime.today()
        if enddate:
            enddate = datetime.strptime(enddate, '%d/%m/%Y')
            self._filterDates(startdate, enddate)

        print('Done dates')

        if beds:
            self._filterBeds(int(beds))
        if bathrooms:
            self._filterBaths(int(bathrooms))
        if parking:
            self._filterParking(int(parking))

        print('Done half')

        if location:
            if not distance:
                distance = '2000'
            distance = int(distance)
            self._filterLocation(location, distance)

        print('Done search.')
        return [x[0] for x in self._scores]

    def _keywordSearch(self, search):
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
                    title_score += (2/3) * name.count(keyword)/len(name)
                if len(desc) != 0:
                    body_score += (1/3) * desc.count(keyword)/len(desc)

            if title_score + body_score != 0:
                scores.append((ad_id, title_score + body_score))

        self._scores = scores

    def _limitRegion(self, text_bounds):
        southwest, northeast = text_bounds.split('+')
        southwest = tuple(map(float, southwest.split(',')))
        northeast = tuple(map(float, northeast.split(',')))

        limited = []

        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            if (southwest[0] < ad.getLocation()[0] and # TODO: fix location
                southwest[1] < ad.getLocation()[1] and
                northeast[0] > ad.getLocation()[0] and
                northeast[1] > ad.getLocation()[1]):
                limited.append((ad, score))

        if limited != []:
            self._scores = limited


    def _filterDates(self, startdate, enddate):
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            print('Check avail')
            if (ad.isAvailable(startdate, enddate)):
                result.append((ad, score))

        self._scores = result


    def _filterBeds(self, beds):
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            if (ad.bed_count >= beds):
                result.append((ad, score))

        self._scores = result

    def _filterBaths(self, baths):
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            if (ad.bath_count >= baths):
                result.append((ad, score))

        self._scores = result

    def _filterParking(self, spots):
        result = []
        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            if (ad.car_count >= spots):
                result.append((ad, score))

        self._scores = result


    def _filterLocation(self, location, dist):
        print(location)
        result = []
        lat = float(location.split(',')[0])
        lon = float(location.split(',')[1])

        for ad_id, score in self._scores:
            ad = self._items[ad_id]
            if (geodesic((lat, lon), (ad.address.lat, ad.address.lng)).km <= dist/1000):
                result.append((ad, score))

        self._scores = result

    # Replaces all contiguous non-alphanumeric characters with a space
    # And converts to lower case
    def _cleanString(self, string):
        return re.sub(r'[\W_]+', ' ', string).lower()

    # Returns a list of all ads mentioning at least one keyword in the search
    # Ordered by increasing score:
    #  score = sum of [(2/3) * frequency of keyword in name +
    #                  (1/3) * frequency of keyword in description]
    #          over all keywords
    def keywordSearch(self, search):
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
                    title_score += (2/3) * name.count(keyword)/len(name)
                if len(desc) != 0:
                    body_score += (1/3) * desc.count(keyword)/len(desc)

            if title_score + body_score != 0:
                scores.append((ad, title_score + body_score))

        scores.sort(key=lambda x: -x[1])

        self._most_recent = scores
        return [x[0] for x in scores]
