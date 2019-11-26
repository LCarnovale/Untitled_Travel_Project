import db

class Booking:
    '''
    Represents a booking in the database, created with a row of data as per bookings.py
    Used to easily use data related to a booking without needing to pass around the database row.
    '''
    def __init__(self, venueid, userid, startDate, endDate):
        '''
        Creates a Booking, with data as per bookings.py sans the id.
        '''
        self._venueid = venueid
        self._userid = userid
        self._start_date = startDate
        self._end_date = endDate

    '''
    Properties
    '''
    @property
    def venueid(self):
        return self._venueid
         
    @property
    def userid(self):
        return self._userid
         
    @property
    def start_date(self):
        return self._start_date
         
    @property
    def end_date(self):
        return self._end_date
         


