import db
import datetime
import src

class NegativeNumberError(Exception):
    pass

class NumberError(Exception):
    def __init__(self, msg="Invalid number given"):
        super().__init__(msg)


class Accommodation:
    def __init__(self, *args):
        """
        args should follow the layout (schema) of the venue table
        defined in dbTools.py

        The output from eg. db.get_venue(n) has the form
            get_venue(n) --> (id, *args)
        so it is easiest to pass around a collection of the return values after
        the id instead of track each of the dozen or so fields individually.
        """ 
        self._id = -1 # Will be set by the accomodationSystem,

        self._ownerid,         \
        self._aid,             \
        self._name,            \
        self._bed_count,       \
        self._bath_count,      \
        self._car_count,       \
        self._description,     \
        self._rate,            \
        self._min_stay,        \
        self._max_stay,        \
        self._details,         \
        self._url     =     args

        ### Data validation  ### TODO: Add more tests?
        if self._bed_count < 0:
            raise NegativeNumberError("Invalid bed count")
        if self._bath_count < 0:
            raise NegativeNumberError("Invalid bath count")
        if self._car_count < 0:
            raise NegativeNumberError("Invalid car count")
        
    def get_dates(self):
        """
        Return a list of date ranges representing this venues
        availability, structured as:
            [
                [start1, end1],
                [start2, end2], ...
            ]
        With all dates as d-m-yy
        """
        avails = db.venues.get_availabilities(self._id)
        avails = [[x[2].strftime('%d-%m-%Y'), x[3].strftime('%d-%m-%Y')] for x in avails]

        # return ['10-10-2019', '11-11-2019']
        return avails

    def isAvailable(self, startDate, endDate=None):
        """
        Check if the venue is available during the given range.
        Give single date to check if the venue is available for the
        given day and the next day.
        
        startDate and endDate must be datetime.date types.

        Return True if available.
        """
        
        if (endDate == None):
            endDate = startDate + datetime.timedelta(days=1)
        
        avails = db.venues.get_overlapping_availability(self._id, startDate, endDate)
        #print(avails, startDate, endDate)

        if len(avails) >= 1:
            return True
        else:
            return False

    def get_images(self):
        """
        Return a list of paths of images for this venue.
        """
        images = db.images.get_for_venue(self.id)
        temp = [img[2] for img in images]
        return [image.replace("\\","/") for image in temp]

    '''
    Properties
    '''
    
    @property
    def aid(self):
        """ id of the venue's address in the database."""
        return self._aid

    @aid.setter
    def aid(self, aid):
        # TODO: Verify this is a valid address id?
        self._aid = aid

    @property
    def ownerid(self):
        """ id of the venue's owner in the database."""
        return self._ownerid

    @ownerid.setter
    def ownerid(self, ownerid):
        # TODO: Verify this is a valid owner id?
        self._ownerid = ownerid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def bed_count(self):
        return self._bed_count

    @bed_count.setter
    def bed_count(self, bed_count):
        try:
            bed_count = int(bed_count)
        except ValueError:
            raise NumberError("bed_count must be an integer.")
        else:
            if bed_count <= 0:
                raise NumberError("bed_count must be greater than 0")
        self._bed_count = bed_count

    @property
    def bath_count(self):
        return self._bath_count

    @bath_count.setter
    def bath_count(self, bath_count):
        try:
            bath_count = int(bath_count)
        except ValueError:
            raise NumberError("bath_count must be an integer.")
        else:
            if bath_count <= 0:
                raise NumberError("bath_count must be greater than 0")
        self._bath_count = bath_count

    @property
    def car_count(self):
        return self._car_count

    @car_count.setter
    def car_count(self, car_count):
        try:
            car_count = int(car_count)
        except ValueError:
            raise NumberError("car_count must be an integer.")
        else:
            if car_count <= 0:
                raise NumberError("car_count must be greater than 0")
        self._car_count = car_count

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        try:
            rate = float(rate)
        except ValueError:
            raise NumberError("rate must be a float.")
        else:
            if rate <= 0:
                raise NumberError("rate must be a positive number.")
        self._rate = rate

    @property
    def min_stay(self):
        return self._min_stay

    @min_stay.setter
    def min_stay(self, min_stay):
        try:
            min_stay = int(min_stay)
        except ValueError:
            raise NumberError("min_stay must be an integer.")
        else:
            if min_stay <= 0:
                raise NumberError("min_stay must be greater than zero.")
        self._min_stay = min_stay

    @property
    def max_stay(self):
        return self._max_stay

    @max_stay.setter
    def max_stay(self, max_stay):
        try:
            max_stay = int(max_stay)
        except ValueError:
            raise NumberError("max_stay must be an integer.")
        else:
            if max_stay <= 0:
                raise NumberError("max_stay must be greater than zero.")
        self._max_stay = max_stay

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, details):
        self._details = details

    @property
    def id(self):
        return self._id

    @property
    def address(self):
        # Get address for the venue
        address = db.addresses.get(self.aid)
        return src.address.Address(*address[1:])

    @property
    def url(self):
        # Get the url of the source of this venue.
        return self._url