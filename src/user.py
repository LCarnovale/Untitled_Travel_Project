import re
import json
import db
from booking import Booking
class EmailError(Exception):
    """Thrown when an email address is invalid."""
    def __init__(self, msg="Attempting to set email with invalid email address."):
        super().__init__(msg)


class User:
    '''
    The User class stores a local copy of a user entry in the database.
    It includes all info as per users.py, but also with some functions to assist with authentication.
    It does not store the password, but does recieve a password hash.
    '''
    def __init__(self, name, userName, email, mobile, desc=None, pwdhash=None):
        self._id = -1 # Will be set by userSystem

        # Use setters to validate data
        self.name = name
        self.username = userName
        self.email = email
        self.mobile = mobile
        self.desc = desc
        # Set these directly
        self._pwdhash = pwdhash
        self._authenticated = False
        self._type = None

    def get_bookings(self):
        """Get the bookings for this user from the database."""
        booking_rows = db.bookings.get_for_user(self._id)
        return sorted([Booking(*row[1:]) for row in booking_rows], key=lambda x: x.start_date)


    def todict(self):
        """
        Return a dict object with attributes of the user other than pwdhash.
        """
        return {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'mobile': self.mobile,
            'desc': self.desc,
        }

    '''
    Properties
    '''
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
        
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        '''Verifies the email is in a valid email format'''
        if email:
            x = re.search(r'[\w\.-]+@[\w\.-]+(\.[\w])+', email)
            if x is not None:
                self._email = email
            else:
                raise EmailError
        else:
            self._email = email # Allow null emails
        
    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        self._mobile = mobile
        
    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc
        
    @property
    def pwdhash(self):
        return self._pwdhash

        
    @property
    def authenticated(self):
        return self._authenticated

    @property
    def type(self):
        return self._type
        


