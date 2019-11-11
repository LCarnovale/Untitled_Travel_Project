import pyodbc

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
    0    revid      int        Identity  PRIMARY KEY
    1    venueid    int        not null  FK -> Venues(id)
    2    userid     int        not null  FK -> Users(id)
    3    postTime   time
    4    postDate   date
    5    rating     tinyint
    6    review     text
"""

########
# If returning a direct cursor object or cursor attribute, it's good to check if a
# connection was ever made because if not, then unless you are 
# returning something like cursor.func() there is a chance 
# cursor.attr will return a lambda func, or cursor will be a FailedConnectionHandler
# object. You will probably want to instead return None in these cases.  
########

        
dbc = dbCursor()
cursor = _UninitialisedConnectionHandler()
is_connected = False

def init():
    """
    Establish a connection to the database. This must be called
    before any other methods can be used. 
    If a connection can not be established then a FailedConnectionHandler 
    will be used instead, which is designed to handle the same requests as
    a cursor but instead will safely fail for all requests. 
    """
    global cursor
    global is_connected
    from server import USE_DATABASE
    try: 
        if not USE_DATABASE:
            print('Please set USE_DATABASE in server.py to True for database.')
            raise Exception("Not using database")
        import connect_config
        cnxn = connect_config.get_connection()
    except pyodbc.ProgrammingError as e:
        if ("IP address" in str(e)): 
            msg = str(e).split("IP address '")[1]
            msg = msg.split("' is not")[0]
            print("Your ip (" + msg + ") was denied.")
        else:
            print(e)
        print("Unable to connect to database. Function calls will do nothing.")
        cursor = _FailedConnectionHandler()
    else:
        print("Successfully connected to database.")
        dbCursor.get_con = connect_config.get_connection
        cnxn.close()
        is_connected = True







