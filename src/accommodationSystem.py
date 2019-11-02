from src.accommodation import Accommodation
from src.search import Search
import cloud.dbTools as db

class AccommodationSystem:
    def __init__(self):
        self._accommodations = {}

    def add_acc(self, id, acc):
        '''Adds accommodations into the system'''
        acc.__id = id
        self._accommodations[id] = acc


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

    def create_accomodation(self, ownerid, addressid, name, bedCount,
                            bathCount, carCount, description, rate, minStay, maxStay, details):
        """
        Create an accomodation object.
        Takes the arguments for a venue defined in dbTools.py, excluding venueid.        
        """
        args = (ownerid, addressid, name, bedCount,
                bathCount, carCount, description, rate, minStay, maxStay, details)                
        new_venueid = db.insert_venue(*args)
        new_venue = Accommodation(*args)
        self.add_acc(new_venueid, new_venue)
        return new_venueid


    def keywordSearch(self, search):
        s = Search(self._accommodations)
        return s.keywordSearch(search)

    def advancedSearch(self, search, text_bounds, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        print('SEARCHING')
        print(self._accommodations)
        s = Search(self._accommodations)
        return s.advancedSearch(search, text_bounds, startdate, enddate, beds,
                                bathrooms, parking, location, distance)
    def clean_system(self):
        """Remove all stored venues (Not from database)"""
        self._accommodations = {}

    def get_all_ads(self):
        # TODO: UPDATE CHANGES
        self.clean_system()

        accs = db.get_all_venues()

        for acc in accs:
            new_acc = Accommodation(*acc[1:])
            self.add_acc(acc[0], new_acc)
            print(new_acc.__id)

        print(self._accommodations)