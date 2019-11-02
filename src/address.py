class Address:
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
        
        
