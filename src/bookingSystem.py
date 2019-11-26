import db
from booking import Booking
from accommodationSystem import AccommodationSystem
from accommodation import Accommodation

class BookingError(Exception):
    '''
    Error specific to Booking objects.
    '''
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self, msg)

class BookingSystem:
    '''
    The BookingSystem should be a global instance, with the responsibility of managing all Booking objects.

    It stores a cache of booking objects, as well as interacting with the database when needed.
    '''

    def __init__(self):
        '''Creates an empty BookingSystem'''
        self._bookings = {}

    def add_booking(self, booking_id, booking):
        """
        Add a booking to the system.
        Stores the id of the booking with the given booking_id
        """
        self._bookings[booking_id] = booking

    def create_booking(self, venueid, userid, startDate, endDate):
        """
        Create a new booking object and insert it into the database.
        startDate, endDate should be type `datetime.date`
        """

        # Verify the booking is allowed
        # -----------------------------

        # Check that the booking is allowed for the venue.
        venue_avails = db.venues.get_overlapping_availability(venueid, startDate, endDate)
        if not venue_avails:
            # No availabilities exist for that period
            raise BookingError("Venue is not available for the requested date range.")
        
        # Check that the venue is not booked for the requested period.
        clashes = db.bookings.get_for_venue_overlapping(venueid, startDate, endDate)
        if clashes:
            raise BookingError("The venue is already booked for the requested period.")
        

        # Booking is valid, insert into system
        # ------------------------------------
        
        new_bookingid = db.bookings.insert(venueid, userid, startDate, endDate)
        new_booking = Booking(venueid, userid, startDate, endDate)
        self.add_booking(new_bookingid, new_booking)

        return new_bookingid

    def get_booking(self, bookid):
        """
        Find a booking in the stored bookings or from the database.

        Returns `None` if a booking cannot be found in the system nor database
        """
        if bookid in self._bookings:
            return self._bookings[bookid]
        else:
            b = db.bookings.get(bookid)
            if b is not None:
                book = Booking(*b[1:])
                self.add_booking(bookid, book)
                return book
            else:
                return None

