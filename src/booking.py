import db

class Booking:

    _id = -1
    '''
        acc is the accommodation
        period is the time period for the booking
        user is the user making the booking
    '''
    def __init__(self, venueid, userid, startDate, endDate):
        self._venueid = venueid
        self._userid = userid
        self._start_date = startDate
        self._end_date = endDate

        


    def checkOverlap(self, startDate, endDate):
        """
        Returns True if the given date range overlaps with the
        date range of the booking.
        """
        if (startDate <= self.end_date) and (endDate >= self.start_date):
            return True 
        return False

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

    @property
    def id(self):
        return self._id
         


