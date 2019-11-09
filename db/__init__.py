"""
This module handles all interaction with the database.

Table structures: 
    Indexes match the index of values in the rows
    returned for each table. ie, when calling get_user(n),
    a row from the user table will be returned, which will be 
    a tuple of values in the order shown below.

    Venue:
    0   venueid       int           Identity   PRIMARY KEY
    1   ownerid       int           not null   FK -> Owners(id)
    2   addressid     int           not null   FK -> Addresses(id)
    3   name          varchar(200)  not null
    4   bedCount      tinyint
    5   bathCount     tinyint
    6   carCount      tinyint
    7   description   text
    8   rate          smallmoney
    9   minStay       int
    10  maxStay       int
    11  details       text

    Availabilities:
    0   avId          int        Identity  PRIMARY KEY
    1   venueid       int                  FK -> Venues(id)
    2   startDate     date
    3   endDate       date

    Owners and Users:
    0   ownerid/userid  int          Identity   PRIMARY KEY
    1   name            varchar(50)  not null
    2   userName        varchar(50)             UNIQUE
    3   email           varchar(100)
    4   phone           varchar(20)
    5   description     text
    6   pwdhash         bytes

    Addresses:
    0   aid         int        Identity  PRIMARY KEY
    1   location    text
    2   lat         varchar(10)
    3   lng         varchar(10)

    Bookings:
    0   bookid      int        Identity  PRIMARY KEY
    1   venueid     int        not null  FK -> Venues(id)
    2   userid      int        not null  FK -> Users(id)
    3   startDate   date       not null
    4   endDate     date       not null

    Reviews:
    0    revid         int        Identity  PRIMARY KEY
    1    venueid       int        not null  FK -> Venues(id)
    2    userid        int        not null  FK -> Users(id)
    3    postDateTime  datetime
    4    recommends    bit
    5    reviewBad     text
    6    reviewGood    text

"""

import sys
sys.path.append('db/')

__all__ = ['users', 'owners', 'venues','addresses',
        'reviews', 'bookings', 'availabilities', 'images']

import users
import owners
import venues
import addresses
import reviews
import bookings
import availabilities
import images


