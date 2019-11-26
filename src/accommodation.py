import db
import datetime
import src
from datetime import datetime, timedelta, time
from booking import Booking

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
        # Get availability from the database
        avails = db.venues.get_availabilities(self._id)

        # Get all bookings for this venue
        dates = db.bookings.get_for_venue(self._id)

        # If there are no booking dates, then return available
        if (not dates):
            avails = [[x[2].strftime('%d-%m-%Y'), x[3].strftime('%d-%m-%Y')] for x in avails]
            return avails

        availableDates = [[x[2], x[3]] for x in avails]

        for i in range(0, len(dates)):
            for j in range(0, len(availableDates)):
                # Get the start and end times for the venue from db
                startAvail = availableDates[j][0]
                endAvail = availableDates[j][1]

                # Get the booking start and end dates
                bookStart = dates[i][3]
                bookEnd = dates[i][4]
                # booking range is within the range from DB
                if bookStart >= startAvail and bookEnd <= endAvail:
                    # Remove the start and end time and replace with new start and end
                    # case 1, bookStart = startAvail and bookEnd < endAvail
                    if bookStart == startAvail and bookEnd < endAvail:
                        availableDates.pop(j)
                        availableDates.insert(j,[(bookEnd+timedelta(days=1)), endAvail])
                        continue
                    # case 2, bookEnd = endAvail, bookStart > startAvail
                    elif bookEnd == endAvail and bookStart > startAvail:
                        availableDates.pop(j)
                        availableDates.insert(j,[startAvail, (bookStart-timedelta(days=1))])
                        continue
                        # case 3, bookStart > startAvail and bookEnd < endAvail
                    elif bookStart > startAvail and bookEnd < endAvail:
                            availableDates.pop(j)
                            availableDates.insert(j,[startAvail, (bookStart - timedelta(days=1))])
                            availableDates.insert(j+1,[(bookEnd + timedelta(days=1)), endAvail])
                            continue
                        # case 4, bookStart = startAvail and bookEnd = endAvail
                    elif bookStart == startAvail and bookEnd == endAvail:
                            # then the available range is unavailable
                            continue

        availableDates = [[x[0].strftime('%d-%m-%Y'), x[1].strftime('%d-%m-%Y')] for x in availableDates]
        print(availableDates)
        return availableDates

    def isAvailable(self, startDate, endDate=None):
        """
        Check if the venue is available during the given range.
        Give single date to check if the venue is available for the
        given day and the next day.
        
        startDate and endDate must be datetime.date types.

        Return True if available.
        """
        
        if (endDate == None):
            endDate = startDate + timedelta(days=1)
        
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

    def get_bookings(self):
        booking_rows = db.bookings.get_for_venue(self._id)
        return sorted([Booking(*row[1:]) for row in booking_rows], key=lambda x: x.start_date)

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
        """Name of the venue"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def bed_count(self):
        """Number of bedrooms the property has"""
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
        """Number of bathrooms the property has"""
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
        """Number of parking spaces the property has"""
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
        """Text description of the property"""
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def rate(self):
        """Rate (in $ per night) to book the place"""
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
        """Minimum number of days you can stay at the place"""
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
        """Maximum number of days you can stay at the place"""
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
        """Additional rules for staying at the venue"""
        return self._details

    @details.setter
    def details(self, details):
        self._details = details

    @property
    def id(self):
        """Id of the venue in the database. Preferrably use """
        return self._id

    @property
    def address(self):
        """Get address for the venue"""
        address = db.addresses.get(self.aid)
        return src.address.Address(*address[1:])

    @property
    def external_url(self):
        """Url of the external site, as stored by the database"""
        return self._url
    
    @property
    def display_url(self):
        """Url of the external site, but without any extra url args"""
        return self.external_url.split('?')[0]

    @property
    def url_base(self):
        """Domain of the external site"""
        return self.external_url.split('//')[1].split('/')[0]

    @property
    def reviews(self):
        """Get a list of Review classes related to the venue"""
        revs = db.reviews.get_for_venue(self._id)
        return [src.review.Review(*x[1:]) for x in revs]