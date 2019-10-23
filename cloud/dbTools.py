"""
This module handles all interaction with the database.

Table structures:

VenuDB:

    Venue:
    0   id            int           Identity   PRIMARY KEY
    1   ownerid       int           not null   FK -> Owners(id)
    2   addressid     int           not null   FK -> Addresses(id)
    3   name          varchar(200)  not null
    4   bedCount      tinyint
    5   bathCount     tinyint
    6   carCount      tinyint
    7   description   text
    8   rate          smallmoney
    9   availStart    date
    10  availEnd      date
    11  minStay       int           DEFAULT 1
    12  maxStay       int
    13  details       text

    Owners and Users:
    0   id           int          Identity   PRIMARY KEY
    1   name         varchar(50)  not null
    2   userName     varchar(50)             UNIQUE
    3   email        varchar(100)
    4   phone        varchar(20)
    5   description  text

    Addresses:
    0   id          int        Identity  PRIMARY KEY
    1   location    text

    Bookings:
    0   id          int        Identity  PRIMARY KEY
    1   venueid     int        not null  FK -> Venues(id)
    2   userid      int        not null  FK -> Users(id)
    3   startDate   date       not null
    4   endDate     date       not null
"""

########
# If returning a direct cursor object or cursor attribute, it's good to check if a
# connection was ever made because if not, then unless you are 
# returning something like cursor.func() there is a chance 
# cursor.attr will return a lambda func, or cursor will be a FailedConnectionHandler
# object. You will probably want to instead return None in these cases.  
########

"""
This handles making calls to cursor when a connection was not made.
This is useful for development and debugging but a failed connection
will be a genuine problem if it occurs on the main server.
The return values are based on the context they will be used in.
"""
class FailedConnectionHandler:
    def __getattr__(self, attr):
        return lambda *x: None

    def __getitem__(self, item):
        return 0

class UninitialisedConnectionHandler:
    def __getattr__(self, attr):
        print("Connection has not been established yet. Call dbTools.init() to connect.")
        return FailedConnectionHandler.__getattr__(self, attr)
    def __getitem__(self, item):
        print("Connection has not been established yet. Call dbTools.init() to connect.")
        return FailedConnectionHandler.__getitem__(self, item)



cursor = UninitialisedConnectionHandler()
is_connected = False
pyodbc = FailedConnectionHandler()
def init():
    global cursor
    global is_connected
    try: 
        import connect_config
        cnxn = connect_config.get_connection()
    except:
        print("Unable to connect to database. Function calls will do nothing.")
        cursor = FailedConnectionHandler()
    else:
        print("Successfully connected to database.")
        cursor = cnxn.cursor()
        pyodbc = connect_config.pyodbc
        is_connected = True

def close():
    """
    Close the connection to the database.
    Other programs might have trouble connecting to the database
    with two connections open.
    """
    cursor.close()

def commit():
    """
    Commit recent changes to the database.
    """
    cursor.commit()

def execute(sql, *params):
    """
    Execute a SQL query and return a cursor object. 
    For use of params see: 
    https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters.
    """
    return cursor.execute(sql, params)
    
def get_user(id):
    """
    Return a single user with the matching id from the database

    Returns None if the user does not exist.
    """
    cursor.execute("SELECT * FROM Users WHERE id=?", id)
    result = cursor.fetchone()
    # if result is None:
    return result

def get_user_from_uname(userName):
    """
    Return a single user with the matching username, or None if it doesn't exist.
    """

    cursor.execute("SELECT * FROM Users WHERE userName=?", userName)
    result = cursor.fetchone()
    return result


def get_owner(id):
    """
    Return an owner with the matching id.

    Return None if the owner does not exist.
    """
    cursor.execute("SELECT * FROM Owners WHERE id=?", id)
    return cursor.fetchone()
    

def get_venue(id):
    """
    Return a venue with the matching id.
    """
    cursor.execute("SELECT * FROM Venues WHERE id=?", id)
    return cursor.fetchone()

def get_booking(id):
    """
    Return a booking with the matching id.
    """
    cursor.execute("SELECT * FROM Bookings WHERE id=?", id)
    return cursor.fetchone()

def get_address(id):
    """
    Return an address with the matching id.
    """
    cursor.execute("SELECT * FROM Addresses WHERE id=?", id)
    return cursor.fetchone()

def insert_user(name, userName, email=None, phone=None, description=None):
    """
    Insert a user into the database with the given details. 

    Attempting to add duplicate usernames raises a pyodbc.IntegrityError.

    Returns thqe id of the inserted user.
    """
    
    ## Fields:
    #  id           int          Identity   PRIMARY KEY
    #  name         varchar(50)  not null
    #  userName     varchar(50)
    #  email        varchar(100)
    #  phone        varchar(20)
    #  description  text 
    try:
        cursor.execute(
            "INSERT INTO Users (name, userName, email, phone, description)   \
            OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)", 
            (name, userName, email, phone, description)
        )
    except pyodbc.IntegrityError as e:
        print("Duplicate username on insert.")
        raise e

    return int(cursor.fetchone()[0]) 

def insert_owner(name, userName, email=None, phone=None, description=None):
    """
    Insert an owner into the database with the given details. 

    Attempting to add duplicate usernames raises a pyodbc.IntegrityError.

    Returns the id of the inserted owner.
    """
    try:
        cursor.execute(
            "INSERT INTO Owners (name, userName, email, phone, description)   \
            OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?)", (name, userName, email, phone, description)
        )
    except pyodbc.IntegrityError as e:
        print("Duplicate username on insert.")
        raise e

    return int(cursor.fetchone()[0]) 

def insert_booking(venueid, userid, startDate, endDate):
    """
    Add a booking record. Must use an existing venueid and userid.
    If either given id's don't exist in their tables an error is raised.

    Returns the id of the new record.

    ** Date should be of type datetime.date
    """
    ## Fields:
    #  id          int        Identity  PRIMARY KEY
    #  venueid     int        not null  FK -> Venues(id)
    #  userid      int        not null  FK -> Users(id)
    #  startDate   date       not null
    #  endDate     date       not null
    try:
        cursor.execute("INSERT INTO Bookings (venueid, userid, startDate, endDate) \
            OUTPUT INSERTED.id VALUES (?, ?, ?, ?)", (venueid, userid, startDate, endDate))
    except pyodbc.IntegrityError as e:
        print("Invalid venueid or userid on insert.")
        raise e
    
    return int(cursor.fetchone()[0]) 
    
def insert_venue(ownerid, addressid, name, bedCount, bathCount, 
        carCount, description, rate, availStart, availEnd,
        minStay, maxStay, details):
    """
    Insert a venue.
    ** Dates should be type datetime.date

    Returns the id of the inserted venue.
    """
    # Fields:
    # id            int           Identity   PRIMARY KEY
    # ownerid       int           not null   FK -> Owners(id)
    # addressid     int           not null   FK -> Addresses(id)
    # name          varchar(200)  not null
    # bedCount      tinyint
    # bathCount     tinyint
    # carCount      tinyint
    # description   text
    # rate          smallmoney
    # availStart    date
    # availEnd      date
    # minStay       int           DEFAULT 1
    # maxStay       int
    # details       text
    try:
        cursor.execute("INSERT INTO Venues (ownerid, addressid, name, bedCount, \
            bathCount, carCount, description, rate, availStart, availEnd,       \
            minStay, maxStay, details) OUTPUT INSERTED.id                       \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (ownerid, addressid, name, bedCount, bathCount, 
            carCount, description, rate, availStart, availEnd,
            minStay, maxStay, details)
        )
    except pyodbc.IntegrityError as e:
        print("Invalid venueid or userid on insert.")
        raise e
    return int(cursor.fetchone()[0]) 

def insert_address(location):
    """
    Insert the given location into the database.

    Return the id of the inserted address.
    """
    cursor.execute("INSERT INTO Addresses (location) OUTPUT INSERTED.id VALUES (?)", location)

    return int(cursor.fetchone()[0]) 

def select_venues(**patterns):
    """
    Provide patterns of the form {"column":"pattern"} 
    referring to the following fields,
    and a query will be constructed like:

    ```SQL
        SELECT * FROM Venues WHERE 
        column1 LIKE pattern1 AND
        column2 LIKE pattern2 ...
    ```    
    For example: 
        select_venues(name="test%", details="%d%") 
    will return all venues with names starting with test,
    and 'd' in the details.

    See https://www.w3schools.com/sql/sql_like.asp for 
    information on patterns.

    Available fields:
        id            int          
        ownerid       int          
        addressid     int          
        name          varchar(200) 
        bedCount      tinyint
        bathCount     tinyint
        carCount      tinyint
        description   text
        rate          smallmoney
        availStart    date
        availEnd      date
        minStay       int          
        maxStay       int
        details       text
    """
    query = "SELECT * FROM Venues WHERE "
    cols = [c for c in patterns]

    query += f"{cols[0]} LIKE ?"
    for c in cols[1:]:
        query += f" AND {c} LIKE ?"

    cursor.execute(query, tuple(patterns[c] for c in cols))

    return cursor.fetchall()

def select_bookings(**patterns):
    """
    Provide patterns of the form {"column":"pattern"} 
    referring to the following fields,
    and a query will be constructed like:
    
    SELECT * FROM Bookings 
    WHERE 
    column1 LIKE pattern1 AND
    column2 LIKE pattern2 ...

    See https://www.w3schools.com/sql/sql_like.asp for 
    information on patterns.

    Available fields:
        id          int    
        venueid     int    
        userid      int    
        startDate   date   
        endDate     date   
    """
    query = "SELECT * FROM Bookings WHERE "
    cols = [c for c in patterns]

    query += f"{cols[0]} LIKE ?"
    for c in cols[1:]:
        query += f" AND {c} LIKE ?"

    cursor.execute(query, tuple(patterns[c] for c in cols))

    return cursor.fetchall()