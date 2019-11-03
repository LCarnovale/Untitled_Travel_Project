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
"""

########
# If returning a direct cursor object or cursor attribute, it's good to check if a
# connection was ever made because if not, then unless you are 
# returning something like cursor.func() there is a chance 
# cursor.attr will return a lambda func, or cursor will be a FailedConnectionHandler
# object. You will probably want to instead return None in these cases.  
########

class ArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InsertionError(Exception):
    def __init__(self, message, col=None, _type=None):
        self.col = col
        self.type = _type
        super().__init__(message)

class _FailedConnectionHandler:
    """
    This handles making calls to cursor when a connection was not made.
    This is useful for development and debugging but a failed connection
    will be a genuine problem if it occurs on the main server.
    The return values are based on the context they will be used in.
    """
    def __getattr__(self, attr):
        return None

    def execute(self, *args, **kwargs):
        return self

    def _default(self):
        return None

    commit = _default
    close  = _default
    fetchone = _default
    fetchall = _default

class _UninitialisedConnectionHandler(_FailedConnectionHandler):
    def __getattribute__(self, attr, *args, **kwargs):
        print("Connection has not been established yet. Call dbTools.init() to connect.")
        return super().__getattribute__(attr)

class dbCursor:
    get_con = lambda : None
    def __enter__(self):
        try:
            self._cnxn = dbCursor.get_con()
        except TypeError:
            print("Connection has not been established yet. Call init().")
            self._cnxn = _FailedConnectionHandler()
            self._cursor = _FailedConnectionHandler()
        except pyodbc.ProgrammingError as e:
            if ("IP address" in str(e)):
                msg = str(e).split("IP address '")[1]
                msg = msg.split("' is not")[0]
                print("Your ip (" + msg + ") was denied.")
            else:
                raise e
            self._cnxn = _FailedConnectionHandler()
            self._cursor = _FailedConnectionHandler()
        else:
            self._cursor = self._cnxn.cursor()

        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self._cnxn.commit()
        self._cnxn.close()

    def __getattr__(self, attr):
        return self._cursor.__getattribute__(attr)
        
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

def execute(sql, *params):
    """
    Execute a SQL query and return a cursor object. 
    For use of params see: 
    https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters.
    """
    with dbc as cursor:
        out = cursor.execute(sql, params)
    
    return out

def get_user(id):
    """
    Return a single user with the matching id from the database

    Returns None if the user does not exist.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Users WHERE userid=?", id)
        return cursor.fetchone()

def get_user_from_uname(userName):
    """
    Return a single user with the matching username, or None if it doesn't exist.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Users WHERE userName=?", userName)
        return cursor.fetchone()

def get_owner(id):
    """
    Return an owner with the matching id.

    Return None if the owner does not exist.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners WHERE ownerid=?", id)
        return cursor.fetchone()

def get_owner_from_uname(userName):
    """
    Return an owner matching the given userName.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners WHERE userName=?", userName)
        return cursor.fetchone()

def get_venue(id):
    """
    Return a venue with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Venues WHERE venueid=?", id)
        return cursor.fetchone()

def get_all_venues():
    """
    Return a venue with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Venues")
        return cursor.fetchall()
    
def get_booking(id):
    """
    Return a booking with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Bookings WHERE bookid=?", id)
        return cursor.fetchone()

def get_address(id):
    """
    Return an address with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Addresses WHERE aid=?", id)
        return cursor.fetchone()

def get_availability(id):
    """
    Get an availability matching the given id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE avId=?", id)
        return cursor.fetchone()

def get_venue_availabilities(venueid):
    """
    Return all availabilities for a venue with the
    given venueid.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities  \
            WHERE venueid=?", venueid)
        return cursor.fetchall()

def get_overlapping_availability(startDate, endDate):
    """
    Get all availabilities that contain the given period in their
    start and end dates.
    Returns a list of availability rows.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE \
            startDate<? AND endDate>?", (startDate, endDate))
        return cursor.fetchall()

def get_overlapping_availability_venue(venueid, startDate, endDate):
    """
    Get availabilities that contain the given period in their
    start and end dates for a given venue id.
    Returns a list of availability rows.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE \
            venueid=? AND startDate<=? AND endDate>=?", (venueid, startDate, endDate))
        return cursor.fetchall()

def insert_user(name, userName, password, email=None, phone=None, description=None):
    """
    Insert a user into the database with the given details. 
    Give the raw text password and the SHA2_512 hash will be stored,
    calculated with HASHBYTES('SHA2_512', '<password>').

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

    # Make sure username is unique:
    with dbc as cursor:
        if (cursor.execute("SELECT * FROM users WHERE username = ?", userName).fetchone()):
            raise InsertionError(
                "Username already exists in users table.", col='userName', _type='duplicate')

        try:
            cursor.execute(
                "INSERT INTO Users (name, userName, email, phone, description, pwdhash)   \
                OUTPUT INSERTED.userid VALUES (?, ?, ?, ?, ?, HASHBYTES('SHA2_512', ?))", 
                (name, userName, email, phone, description, password)
            )
        except pyodbc.IntegrityError as e:
            raise e
            # raise InsertionError("SQL Integrity Error, likely a duplicate username on insert.")

        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def insert_owner(name, userName, password, email=None, phone=None, description=None):
    """
    Insert an owner into the database with the given details. 
    Give the raw text password and the SHA2_512 hash will be stored,
    calculated with HASHBYTES('SHA2_512', '<password>').

    Attempting to add duplicate usernames raises a pyodbc.IntegrityError.

    Returns the id of the inserted owner.
    """
    with dbc as cursor:
        try:
            cursor.execute(
                "INSERT INTO Owners (name, userName, email, phone, description, pwdhash)   \
                OUTPUT INSERTED.ownerid VALUES (?, ?, ?, ?, ?, HASHBYTES('SHA2_512', ?))", 
                (name, userName, email, phone, description, password)
            )
        except pyodbc.IntegrityError as e:
            print("Duplicate username on insert.")
            raise e

        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

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
    with dbc as cursor:
        try:
            cursor.execute("INSERT INTO Bookings (venueid, userid, startDate, endDate) \
                OUTPUT INSERTED.bookid VALUES (?, ?, ?, ?)", (venueid, userid, startDate, endDate))
        except pyodbc.IntegrityError as e:
            print("Invalid venueid or userid on insert.")
            raise e
        
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def insert_venue(ownerid, addressid, name, bedCount, bathCount,
                 carCount, description, rate,
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
    # minStay       int           DEFAULT 1
    # maxStay       int
    # details       text
    with dbc as cursor:
        try:
            cursor.execute("INSERT INTO Venues (ownerid, addressid, name,     \
                bedCount, bathCount, carCount, description, rate, minStay,    \
                maxStay, details) OUTPUT INSERTED.venueid                     \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ownerid, addressid, name, bedCount, bathCount,
                carCount, description, rate,
                minStay, maxStay, details)
            )
        except pyodbc.IntegrityError as e:
            print("Invalid venueid or userid on insert.")
            raise e
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def insert_address(location, lat, lng):
    """
    Insert the given location into the database.

    location should be an address as text,
    lat and lng should be latitude and longitude, as float or string.

    Return the id of the inserted address.
    """
    with dbc as cursor:
        cursor.execute("INSERT INTO Addresses (location, lat, lng) OUTPUT INSERTED.aid VALUES (?, ?, ?)", 
            location, lat, lng)
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def insert_availability(venueid, startDate, endDate):
    """
    Insert an availability and return the id of the new availability.
    """
    with dbc as cursor:
        cursor.execute(
            "INSERT INTO Availabilities (venueid, startDate, endDate) OUTPUT INSERTED.avId VALUES (?, ?, ?)", (
                venueid, startDate, endDate)
        )
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def update_venue(venueid, **fields):
    """
    Update a venue record. Takes the id of the venue to be updated (venueid)
    and keyword arguments corresponding to the table's schema.

    valid fields are:
        ownerid, addressid, name, bedCount, bathCount, 
        carCount, description, rate, minStay, maxStay, details     

    Usage:
        update_venue(1, bedCount=3) # Set the bedCount value to 3
    Or
        kwargs = {'name':'Red Centre', 'rate':20}
        update_venue(2, **kwargs) # Set name to 'Red Centre' and rate to 20.
    """

    valid_fields = (
        "ownerid", "addressid", "name", "bedCount", "bathCount",
        "carCount", "description", "rate", "minStay", "maxStay", "details"
    )

    if 'venueid' in fields:
        raise ArgumentException("Unable to change a venue's id.")

    query = "UPDATE Venues SET "

    for f in fields:
        if f not in valid_fields:
            raise ArgumentException("Invalid field name: " + f)

    # Build the rest of the query
    keys = [f for f in fields]
    # Do this to ensure dict ordering is irrelevant
    vals = [fields[k] for k in keys]
    s = [f"{f} = ?" for f in keys]
    s = ' AND '.join(s)
    query += s
    query += " WHERE venueid=?"
    with dbc as cursor:
        cursor.execute(query, (*vals, venueid))

def update_user(userid, **fields):
    """
    Update a user record. Takes the id of the user to be updated (userid)
    and keyword arguments corresponding to the table's schema.
    pwdhash and pwdplain must not be supplied at the same time, as both
    affect the pwdhash field.

    ** To update the password: **
    Changing the pwdhash is not recommended. Instead, provide a plain text 
    password for the keyword pwdplain and the hash will be calculated and
    stored.

    valid fields are:
        name, userName, email, phone, description, pwdhash, pwdplain

    Usage:
        update_user(1, email='e@mail.com')  # Change the user's email.
    Or
        kwargs = {'email': 'e@mail.com', 'phone': '12345'}
        update_user(2, **kwargs)  # Change the user's phone number and email.
    """

    valid_fields = (
        "name", "userName", "email", "phone", "description", "pwdhash", "pwdplain"
    )

    if 'userid' in fields:
        raise ArgumentException("Unable to change a user's id.")

    if 'pwdplain' in fields and 'pwdhash' in fields:
        raise ArgumentException(
            "Can not change plain text password and password hash fields simultaneously.")

    query = "UPDATE Users SET "

    for f in fields:
        if f not in valid_fields:
            raise ArgumentException("Invalid field name: " + f)

    # Build the rest of the query
    keys = [f for f in fields]
    # Do this to ensure dict ordering is irrelevant
    vals = [fields[k] for k in keys if k != 'pwdplain']
    s = [f"{f} = ?" for f in keys if f != 'pwdplain']
    if 'pwdplain' in keys:
        s.append("pwdhash = HASHBYTES('SHA2_512', ?)")
        vals.append(fields['pwdplain'])
    s = ' , '.join(s)
    query += s
    query += " WHERE userid=?"
    with dbc as cursor:
        cursor.execute(query, (*vals, userid))

def update_owner(ownerid, **fields):
    """
    Update a owner record. Takes the id of the owner to be updated (ownerid)
    and keyword arguments corresponding to the table's schema.
    pwdhash and pwdplain must not be supplied at the same time, as both
    affect the pwdhash field.

    ** To update the password: **
    Changing the pwdhash is not recommended. Instead, provide a plain text 
    password for the keyword pwdplain and the hash will be calculated and
    stored.

    valid fields are:
        name, userName, email, phone, description, pwdhash, pwdplain

    Usage:
        update_owner(1, email='e@mail.com')  # Change the owner's email.
    Or
        kwargs = {'email': 'e@mail.com', 'phone': '12345'}
        update_owner(2, **kwargs)  # Change the owner's phone number and email.
    """

    valid_fields = (
        "name", "userName", "email", "phone", "description", "pwdhash", "pwdplain"
    )

    if 'ownerid' in fields:
        raise ArgumentException("Unable to change a owner's id.")

    if 'pwdplain' in fields and 'pwdhash' in fields:
        raise ArgumentException(
            "Can not change plain text password and password hash fields simultaneously.")

    query = "UPDATE Owners SET "

    for f in fields:
        if f not in valid_fields:
            raise ArgumentException("Invalid field name: " + f)

    # Build the rest of the query
    keys = [f for f in fields]
    # Do this to ensure dict ordering is irrelevant
    vals = [fields[k] for k in keys if k != 'pwdplain']
    s = [f"{f} = ?" for f in keys if f != 'pwdplain']
    if 'pwdplain' in keys:
        s.append("pwdhash = HASHBYTES('SHA2_512', ?)")
        vals.append(fields['pwdplain'])
    s = ' , '.join(s)
    query += s
    query += " WHERE ownerid=?"
    with dbc as cursor:
        cursor.execute(query, (*vals, ownerid))

def update_booking(bookid, **fields):
    """
    Update a booking record. Takes the id of the booking to be updated (bookid)
    and values for available fields:
    
    fields:
        venueid, userid, startDate, endDate

    Similar usage to update_owner()
    """
    valid_fields = (
        "venueid", "userid", "startDate", "endDate"
    )

    if 'bookid' in fields:
        raise ArgumentException("Unable to change a booking's id.")

    for f in fields:
        if f not in valid_fields:
            raise ArgumentException(f"Invalid field name: {f}")

    query = "UPDATE Bookings SET "

    keys = [f for f in fields]
    vals = [fields[f] for f in keys]
    s = [f"{f} = ?" for f in keys]
    s = ' , '.join(s)
    query += s
    query += " WHERE bookid=?"

    with dbc as cursor:
        cursor.execute(query, (*vals, bookid))

def update_address(aid, location=None):
    """
    Update the location of an address row.
    """
    if location is not None:
        with dbc as cursor:
            cursor.execute('UPDATE Addresses SET location=? WHERE aid=?', (location, aid))
    
def check_user_pass(username, password_text):
    """
    Search users for a user with the matching username and password.
    
    If username and password match, return that row.
    Otherwise return None.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Users \
            WHERE userName=? AND pwdhash=HASHBYTES('SHA2_512', ?)", (username, password_text))
    
        return cursor.fetchone()

def check_owner_pass(username, password_text):
    """
    Search owners for an owner with the matching username and password.
    
    If username and password match, return that row.
    Otherwise return None.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners \
            WHERE userName=? AND pwdhash=HASHBYTES('SHA2_512', ?)", (username, password_text))
        
        return cursor.fetchone()

def select_venues(**patterns):
    """
    Provide patterns of the form {"column":"pattern"} 
    referring to the following fields,
    and a query will be constructed like:

        SELECT * FROM Venues WHERE 
        column1 LIKE pattern1 AND
        column2 LIKE pattern2 ...

    Returns a list of matching rows.    
        
    For example: 
        select_venues(name="test%", details="%d%") 

    will return all venues with names starting with test,
    and 'd' in the details.

    See https://www.w3schools.com/sql/sql_like.asp for 
    information on patterns.

    Available fields:
        venueid       int          
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
    with dbc as cursor:
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

    Returns a list of matching rows.

    See https://www.w3schools.com/sql/sql_like.asp for 
    information on patterns.

    Available fields:
        bookid      int    
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
    with dbc as cursor:
        cursor.execute(query, tuple(patterns[c] for c in cols))

        return cursor.fetchall()
