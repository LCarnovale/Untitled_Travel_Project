class User:
    def __init__(self, name, userName, email, mobile, desc=None, pwdhash=None):
        self._name = name
        self._username = userName
        self._email = email
        self._mobile = mobile
        self._desc = desc
        self._pwdhash = pwdhash
        self._authenticated = False
        # self._bookings = [] Use this or use the database?

    # '''Return unique ID for each user'''
    # def getID(self):
    #     return self._id

    # ''' Adds a booking into the user'''
    # def addBooking(self, booking):
    #     self._bookings.append(booking)

    '''
    Properties
    '''
    @property
    def name(self):
        self._name
        
    @property
    def username(self):
        self._username
        
    @property
    def email(self):
        self._email
        
    @property
    def mobile(self):
        self._mobile
        
    @property
    def desc(self):
        self._desc
        
    @property
    def pwdhash(self):
        self._pwdhash
        
    @property
    def authenticated(self):
        self._authenticated
        


