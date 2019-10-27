import re
from datetime import datetime
from geopy.distance import geodesic

class Search():
    def __init__(self, items):
        self._items = items
        self._scores = []
        self._most_recent = []

    def advancedSearch(self, search, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        self._scores = []

        if search:
            self._keywordSearch(search)
        else:
            self._scores = [(x,0.0) for x in self._items]

        if startdate:
            startdate = datetime.strptime(startdate, '%d-%m-%Y')
            self._filterStart(startdate)
        if enddate:
            enddate = datetime.strptime(enddate, '%d-%m-%Y')
            self._filterStart(enddate)

        if beds:
            self._filterBeds(int(beds))
        if bathrooms:
            self._filterBaths(int(bathrooms))
        if parking:
            self._filterParking(int(parking))

        if location:
            if not distance:
                distance = '2000'
            distance = int(distance)
            self._filterLocation(location, distance)

        return [x[0] for x in self._scores]

    def _keywordSearch(self, search):
        search = self._cleanString(search)
        search = search.split(' ')

        scores = []

        for ad in self._items:
            title_score = 0.0
            body_score = 0.0

            name = ad.getName()
            name = self._cleanString(name)
            name = name.split(' ')

            desc = ad.getDesc()
            desc = self._cleanString(desc)
            desc = desc.split(' ')

            for keyword in search:
                if len(name) != 0:
                    title_score += (2/3) * name.count(keyword)/len(name)
                if len(desc) != 0:
                    body_score += (1/3) * desc.count(keyword)/len(desc)

            if title_score + body_score != 0:
                scores.append((ad, title_score + body_score))

        self._scores = scores

    def _filterStart(self, startdate):
        result = []
        for ad, score in self._scores:
            if (ad.getAvailEnd() >= startdate):
                result.append((ad, score))

        self._scores = result

    def _filterEnd(self, enddate):
        result = []
        for ad, score in self._scores:
            if (ad.getAvailStart() <= enddate):
                result.append((ad, score))

        self._scores = result


    def _filterBeds(self, beds):
        result = []
        for ad, score in self._scores:
            if (ad.getBeds() >= beds):
                result.append((ad, score))

        self._scores = result

    def _filterBaths(self, baths):
        result = []
        for ad, score in self._scores:
            if (ad.getBathrooms() >= baths):
                result.append((ad, score))

        self._scores = result

    def _filterParking(self, spots):
        print('#TODO: Parking unimplemented')
        '''
        result = []
        for ad, score in self._scores:
            if (ad.getParking() >= spots):
                result.append((ad, score))

        self._scores = result
        '''


    def _filterLocation(self, location, dist):
        result = []
        lat = float(location.split(' ')[0])
        lon = float(location.split(' ')[1])

        for ad, score in self._scores:
            if (geodesic((lat, lon), ad.getLocation()).km <= dist/1000):
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

        for ad in self._items:
            title_score = 0.0
            body_score = 0.0

            name = ad.getName()
            name = self._cleanString(name)
            name = name.split(' ')

            desc = ad.getDesc()
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