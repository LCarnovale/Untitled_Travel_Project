class Booking:
    _bookingID = -1
    '''
        acc is the accommodation
        period is the time period for the booking
        user is the user making the booking
    '''
    def __init__(self, acc, period, user):
        self._acc = acc
        self._period = period
        self._user = user
        self._bookingID += 1

    def checkPeriod(self, period):
        #TODO check if the booking period and given period overlap
        pass

    '''Check if the accommodation is available given the period 
        booking is an object passed in'''
    def checkBooking(self):
        available = False
        #TODO check how the date is being parsed in
        # users cannot book 2 places within the same period
        pass
        # if available during period
        makeBooking(booking)
        # else deny (Give reason why)

    '''Make a booking '''
    def makeBooking(self):
        #TODO make place unavailable during period
        # add the booking to the user
        user.addBooking(self)
        pass
