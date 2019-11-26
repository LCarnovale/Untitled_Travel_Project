class Address:
    '''
    Class representing the address of a venue

    Generally used to interact with an entry in the database without having to
     pass around a tuple of the row in the database.

    This class has properties as per db/addresses.py, and is created with a row
    from the database sans the aid.
    '''
    def __init__(self, street_address, lat, lng):
        self._street_address = street_address
        self._lat = lat
        self._lng = lng

    '''
    Properties
    '''

    @property
    def street_address(self):
        return self._street_address
        
    @property
    def lat(self):
        return self._lat
        
    @property
    def lng(self):
        return self._lng
        
        
