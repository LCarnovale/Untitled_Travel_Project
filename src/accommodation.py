class NegativeNumberError(Exception):
    pass

class Accommodation:
    _id = 0

    def __init__(self, name, address, numBeds, numBath, owner,
                 stayDetail, details=None):
        self._name = name
        self._addr = address
        self._owner = owner
        self._details = details
        self._stayDetails = stayDetail
        self._id = Accommodation._id
        Accommodation._id += 1

        if int(numBeds) < 0 or int(numBath) < 0:
            raise NegativeNumberError("Please enter a positive number")
        else:
            self._numBeds = numBeds
            self._numBath = numBath

    '''Returns unique ID for the accommodation'''
    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getAddr(self):
        return self._addr.getAddr()

    def getBeds(self):
        return self._numBeds

    def getBathrooms(self):
        return self._numBath

    def getOwnerDetails(self):
        return self._owner.getDetails()

    def getOwnerDesc(self):
        return self._owner.getDesc()

    def getPrice(self):
        return self._stayDetails.getPrice()

    def getAvailStart(self):
        return self._stayDetails.getAvailStart()

    def getAvailEnd(self):
        return self._stayDetails.getAvailEnd()

    def getMinStay(self):
        return self._stayDetails.getMinStay()

    def getMaxStay(self):
        return self._stayDetails.getMaxStay()

    def getStayDetail(self):
        return self._stayDetails.getDetails()

    # True if not booked and in availability period, otherwise False
    def isAvailable(self):
        #TODO
        return True

    def getDesc(self):
        return self._details



