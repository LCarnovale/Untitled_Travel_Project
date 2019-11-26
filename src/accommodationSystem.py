from src.accommodation import Accommodation
from src.search import Search
import datetime
import db

class AccommodationSystem:
    '''
    The AccommodationSystem class is responsible for managing all Accommodation objects in (non-database) storage.
    It is also responsible for high-level interaction with the database related to Accommodation objects.

    This should be a global variable, and it will store a cached list of Accommodation objects, so as to
     reduce the number of times the database needs to be called.
    '''
    def __init__(self):
        '''
        Initialise the empty AccommodationSystem
        '''
        self._accommodations = {}

    def add_acc(self, id, acc):
        '''Adds Accommodation objects into the system'''
        try:
            id = int(id)
        except ValueError:
            raise ValueError("Can not convert %s to an int." % id)

        acc._id = id
        self._accommodations[id] = acc
    
    def add_acc_row(self, row):
        """
        Insert an accommodation object created from a row returned
        from the database. Use this to avoid calling the database multiple times.
        """
        new_acc = Accommodation(*row[1:])
        self.add_acc(row[0], new_acc)
        return new_acc


    def get_acc(self, id):
        '''
        Finds an accommodation by a unique ID
        Returns None if none are found.

        If id is a list of id's, returns a list of corresponding objects.
        '''
        # Try the stored list:
        print('GET', id)
        if type(id) == str:
            id = int(id)
        else:
            try:
                iter(id)
            except:
                pass
            else:
                return [self.get_acc(x) for x in id] 
                
        if id in self._accommodations:
            # Return the local copy
            return self._accommodations[id]
        else:
            # Fetch from database
            acc = db.venues.get(id)
            if acc is not None:
                new_acc = Accommodation(*acc[1:])
                self.add_acc(id, new_acc)
                return new_acc
            else:
                return None

    def create_accomodation(self, ownerid, addressid, name, bedCount,
                            bathCount, carCount, description, rate, minStay, 
                            maxStay, details, url=None):
        """
        Create an Accomodation object.
        Takes the arguments for a venue defined in dbTools.py, excluding venueid.
        Stores the created object in self._accommodations, with the generated id.
        Returns the generated id.
        """
        args = (ownerid, addressid, name, bedCount,
                bathCount, carCount, description, rate, 
                minStay, maxStay, details, url)
        new_venueid = db.venues.insert(*args)
        new_venue = Accommodation(*args)
        self.add_acc(new_venueid, new_venue)
        return new_venueid

    def advancedSearch(self, search, startdate, enddate, beds,
                       bathrooms, parking, location, distance):
        '''
        Perform an advanced search on the database

        Firstly, advancedSearch will use database joins to efficiently filter out
         all items outside the given date range and location.
        It will then use the Search class to perform a search on the remaining items.

        All arguments should be strings. Dates are in the form dd/mm/YYYY.
        See Search.advancedSearch for a description of the arguments.

        The only required arguments are the start and end date, which should be set to today if not specified.
        All other options may be set to the empty string '' or None if they are not provided.
        '''

        # -----------------
        # 1. Pre-processing
        # -----------------

        refine = False

        if startdate and enddate:
            self.get_available(startdate, enddate, refine=refine)
            refine = True
        else:
            raise Exception('No dates were found when searching.')

        if location:
            self.get_near(location.split(', '), distance, refine=refine)
            refine=True


        # ------------
        # 2. Searching
        # ------------

        s = Search(self._accommodations)
        result = s.advancedSearch(search, startdate, enddate, beds,
                                  bathrooms, parking, location, distance)
        return result


    def clean_system(self):
        """Remove all stored venues (Not from database)"""
        self._accommodations = {}

    def get_for_owner(self, ownerid):
        """
        Get all venues associated with the given owner.
        """
        venues = db.venues.get_for_owner(ownerid)
        return [self.add_acc_row(v) for v in venues]

    def get_near(self, point, distance, refine=False):
        """
        Load all venues within `distance` metres of `point`.
        Set `refine=True` to remove venues that do not appear in the 
        search result from the system, and exclude results that don't
        already exist in the system.

        `point` should be a lat-lon pair.
        """
        venues, addresses, dists = db.venues.search_area_circle(point, distance)

        if refine:
            _refine(self._accommodations, [v[0] for v in venues],
                    venues, addresses, dists)

            self.clean_system()
        
        
        for v in venues:
            self.add_acc_row(v)
        
        return [v[0] for v in venues]

    def get_within(self, lower_left, upper_right, refine=False):
        """
        Load all venues within the given region.
        Set `refine=True` to remove venues that do not appear in the 
        search result from the system, and exclude results that don't
        already exist in the system.
        """
        venues, addresses = db.venues.search_area_box(lower_left, upper_right)

        if refine:
            _refine(self._accommodations, [v[0] for v in venues], venues, addresses)
            self.clean_system() 


        for v in venues:
            new_venue = Accommodation(*v[1:])
            self.add_acc(v[0], new_venue)

        return [v[0] for v in venues]
    
    def get_like(self, refine=False, **patterns):
        """ Load all venues with matching patterns in the given fields.

        Set `refine=True` to remove venues that do not appear in the 
        search result from the system, and exclude results that don't
        already exist in the system.

        patterns with value None are ignored. (Use `'NULL'` to check for null values.)

        See db.venues.search() for more info.
        
        Return a list of the ids of venues found, or `None` if all given
        patterns have None as a value.
        """
        patterns = {p:patterns[p] for p in patterns if patterns[p]}
        if not patterns: return None
        venues = db.venues.search(**patterns)


        if refine:
            _refine(self._accommodations, [v[0] for v in venues], venues)
            self.clean_system()
        
        for v in venues:
            new_venue = Accommodation(*v[1:])
            self.add_acc(v[0], new_venue)

        return [v[0] for v in venues]

    def get_available(self, startdate, enddate, refine=False):
        """
        Load all venues available within the given date range.
        
        Set `refine=True` to remove venues that do not appear in the 
        search result from the system, and exclude results that don't
        already exist in the system.

        Return a list of the ids of venues loaded.
        """

        if type(startdate) == str:
            startdate = datetime.datetime.strptime(startdate, "%d/%m/%Y")
            enddate = datetime.datetime.strptime(enddate, "%d/%m/%Y")
        
        venues, avails = db.venues.get_available(startdate, enddate)

        if refine:
            _refine(self._accommodations, [v[0] for v in venues], venues, avails)
            self.clean_system()
            
        for v in venues:
            new_venue = Accommodation(*v[1:])
            self.add_acc(v[0], new_venue)
        
        return [v[0] for v in venues]
        

def _refine(existing, found, *lists):
    """
    For all `found[i]` not in `existing`,
    removes `list[i]` for all given lists.

    Performs modifications in place, also returns the given lists.
    """
    c = 0
    for i, id in enumerate(found):
        if id not in existing:
            for l in lists:
                l.pop(i - c)
            c += 1
    
    return lists
