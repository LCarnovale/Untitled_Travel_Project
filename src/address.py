class Address:
    def __init__(self, street, postcode=None, aptNum=None):
        self._street = street
        self._postcode = postcode
        self._state = "NSW"
        self._aptNum = aptNum


    def getAddr(self):
        return self._street

    '''
    Properties
    '''


    @property
    def street(self):
        return self._street
        
    @property
    def postcode(self):
        return self._postcode
        
    @property
    def state(self):
        return self._state
        
    @property
    def aptNum(self):
        return self._aptNum
        
