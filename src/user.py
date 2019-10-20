import re

class EmailError(Exception):
    pass

class User:
    _id = -1
    def __init__(self, name, email, mobile, desc=None, addr=None):
        self._name = name
        self._mobile = mobile
        self._desc = desc
        self._addr = addr
        self._id += 1
        self._bookings = []

        if self.checkEmail(email) is None:
            raise EmailError("Please enter a valid email address")
        else:
            self._email = email

    '''Return unique ID for each user'''
    def getID(self):
        return self._id

    ''' Adds a booking into the user'''
    def addBooking(self, booking):
        self._bookings.append(booking)

    def getDesc(self):
        return self._desc

    def getDetails(self):
        return "Email: " + self._email + "Mobile: " + self._mobile

    def checkEmail(self, email):
        x = re.search("[\w0-9]+@[\w0-9]+\.com", email)
        return x
