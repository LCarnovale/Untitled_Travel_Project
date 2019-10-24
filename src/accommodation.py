class NegativeNumberError(Exception):
    pass

class Accommodation:
    _id = -1

    def __init__(self, name, address, numBeds, numBath, owner,
                 stayDetail, details=None):
        self._name = name
        self._addr = address
        self._owner = owner
        self._details = details
        self._stayDetails = stayDetail
        self._id += 1

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

    def getMinStay(self):
        return self._stayDetails.getMinStay()

    def getMaxStay(self):
        return self._stayDetails.getMaxStay()

    def getStayDetail(self):
        return self._stayDetails.getDetails()

    # True if not booked and in availability period, otherwise False
    def isAvailable(self):
        return self._stayDetails.isAvailable()

    def getDesc(self):
        return self._details

    def getDates(self):
        return self._stayDetails.getDates()

    def getAvailStart(self):
        pass

    def getAvailEnd(self):
        pass



