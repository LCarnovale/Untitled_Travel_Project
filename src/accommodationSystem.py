from src.accommodation import Accommodation
from src.search import Search
import cloud.dbTools as db

from src.accommodation import Accommodation

class AccommodationSystem:
    def __init__(self):
        self._accommodations = {}

    def add_acc(self, id, acc):
        '''Adds accommodations into the system'''
        self._accommodations[id] = acc
        acc.__id = id


    def get_acc(self, id):
        '''
        Finds an accommodation by a unique ID
        Returns None if none are found.
        '''
        # Try the stored list:
        if id in self._accommodations:
            return self._accommodations[id]
        else:
            # Fetch from database
            acc = db.get_venue(id)
            if acc is not None:
                new_acc = Accommodation(*acc[1:])
                self.add_acc(id, new_acc)
                return new_acc
            else:
                return None

    def create_accomodation(self, *args):
        """
        Create an accomodation object.
        Takes the arguments for a venue defined in dbTools.py, excluding venueid.        
        """
        # args = (ownerid, addressid, name, bedCount,
        #         bathCount, carCount, description, rate, minStay, maxStay, details)                
        new_venueid = db.insert_venue(*args)
        new_venue = Accommodation(*args)
        self.add_acc(new_venueid, new_venue)
        return new_venueid


    def keywordSearch(self, search):
        s = Search(self._accommodations)
        return s.keywordSearch(search)

    def advancedSearch(self, search, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        s = Search(self._accommodations)
        return s.advancedSearch(search, startdate, enddate, beds,
                                bathrooms, parking, location, distance)
    def clean_system(self):
        """Remove all stored venues (Not from database)"""
        self._accommodations = {}
