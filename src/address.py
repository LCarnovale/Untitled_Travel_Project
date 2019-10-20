class Address:
    def __init__(self, street, postcode=None, aptNum=None):
        self._street = street
        self._postcode = postcode
        self._state = "NSW"
        self._aptNum = aptNum


    def getAddr(self):
        return self._street
