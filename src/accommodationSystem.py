from src.accommodation import Accommodation
from src.search import Search

class AccommodationSystem:
    def __init__(self):
        self._accommodations = []

    '''Adds accommodations into the system'''
    def addAcc(self, acc):
        self._accommodations.append(acc)

    '''Finds an accommodation by a unique ID'''
    def getAcc(self, id):
        for acc in self._accommodations:
            if int(acc.getID()) == int(id):
                return acc

    def keywordSearch(self, search):
        s = Search(self._accommodations[:])
        return s.keywordSearch(search)

    def advancedSearch(self, search, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        s = Search(self._accommodations[:])
        return s.advancedSearch(search, startdate, enddate, beds,
                                bathrooms, parking, location, distance)