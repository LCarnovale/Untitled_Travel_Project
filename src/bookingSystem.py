import db
from booking import Booking

class BookingSystem:
    def __init__(self):
        self._bookings = {}

    def add_booking(self, booking_id, booking):
        self._bookings[booking_id] = booking

    def create_booking(self, venueid, userid, startDate, endDate):
        """
        Create a new booking object and insert it into the database.
        startDate, endDate should be type `datetime.date`
        """

        # TODO: Verify the booking is allowed

        new_bookingid = db.bookings.insert(venueid, userid, startDate, endDate)
        new_booking = Booking(venueid, userid, startDate, endDate)
        self.add_booking(new_bookingid, new_booking)
        return new_bookingid

    def get_booking(self, bookid):
        """
        Find a booking in the stored bookings or from the database.

        Returns `None` if a booking cannot be found in the system or database
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


