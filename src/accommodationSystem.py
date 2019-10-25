import cloud.dbTools as db

from src.accommodation import Accommodation

class AccommodationSystem:
    def __init__(self):
        self._accommodations = {}

    def addAcc(self, id, acc):
        '''Adds accommodations into the system'''
        self._accommodations[id] = acc


    def getAcc(self, id):
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
                self.addAcc(id, new_acc)
                return new_acc
            else:
                return None

    def create_accomodation(self, *args):
        """
        Create an accomodation object.
        Takes the arguments for a venue defined in dbTools.py, excluding venueid.        
        """
        # args = (ownerid, addressid, name, bedCount,
        #         bathCount, carCount, description, rate, availStart,
        #         availEnd, minStay, maxStay, details)                
        new_venueid = db.insert_venue(*args)
        new_venue = Accommodation(*args)
        self.addAcc(new_venueid, new_venue)

    def clean_system(self):
        """Remove all stored venues (Not from database)"""
        self._accommodations = {}
