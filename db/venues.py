"""
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
    12  ExtSource     URL           null
"""
from helpers import dbCursor, ArgumentException
import pyodbc

def get_all():
    """
    Return a venue with the matching id.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Venues")
        return cursor.fetchall()


def get(id):
    """
    Return a venue with the matching id.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Venues WHERE venueid=?", id)
        return cursor.fetchone()

def get_for_owner(ownerid):
    """
    Return all venues associated with the given owner.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Venues WHERE ownerid=?", ownerid)
        return cursor.fetchall()

def get_availabilities(venueid):
    """
    Return all availabilities for a venue with the
    given venueid.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Availabilities  \
            WHERE venueid=?", venueid)
        return cursor.fetchall()

def get_overlapping_availability(venueid, startDate, endDate):
    """
    Get availabilities that contain the given period in their
    start and end dates for a given venue id.
    Returns a list of availability rows.

    Edge cases are included.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE \
            venueid=? AND startDate<=? AND endDate>=?", (venueid, startDate, endDate))
        return cursor.fetchall()

def get_available(startDate, endDate):
    """
    Get all venues available in the given date range.

    `startDate`, `endDate` should be datetime types.

    Returns a list of venues and a list of the matching availbilities.
    """
    query = """SELECT * FROM Venues 
    INNER JOIN Availabilities ON Venues.venueid = Availabilities.venueid
    WHERE startDate<=? AND endDate>=?
    """
    with dbCursor() as cursor:
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()
        v = [r[:13] for r in result]
        av = [r[13:] for r in result]
        return (v, av) 


def insert(ownerid, addressid, name, bedCount, bathCount,
                 carCount, description, rate,
                 minStay, maxStay, details, source=None):
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
    # ExtSource     url
    with dbCursor() as cursor:
        try:
            cursor.execute("INSERT INTO Venues (ownerid, addressid, name,     \
                bedCount, bathCount, carCount, description, rate, minStay,    \
                maxStay, details, ExtSource) OUTPUT INSERTED.venueid          \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (ownerid, addressid, name, bedCount, bathCount,
                            carCount, description, rate,
                            minStay, maxStay, details, source)
                           )
        except pyodbc.IntegrityError as e:
            print("Invalid venueid or userid on insert.")
            raise e
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None


def update(venueid, **fields):
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
        "carCount", "description", "rate", "minStay", "maxStay", 
        "details", "ExtSource"
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
    with dbCursor() as cursor:
        cursor.execute(query, (*vals, venueid))

def search_area_circle(centre, radius):
    """
    Return venues within the given `radius` from `centre`.

    Distances are calculated with 

    `centre` should be a (lat, lng) pair and `radius` should be in metres.
    
    Returns 3 lists: list of venue rows, list of matching addresses, and list of matching distances
    from centre (in metres)
    """
	
    query = """
    SELECT *, geography::Point(lat, lng, 4326).STDistance(geography::Point(?, ?, 4326)) as distance From Venues 
    INNER JOIN Addresses ON Venues.addressid = Addresses.aid
    WHERE ?>geography::Point(lat, lng, 4326).STDistance(geography::Point(?, ?, 4326))
    ORDER BY distance"""
    with dbCursor() as cursor:
        cursor.execute(query, (*centre, radius, *centre))
        result = cursor.fetchall()
        v_rows = [r[:13] for r in result]
        a_rows = [r[13:-1] for r in result]
        d_rows = [r[-1] for r in result]
        return v_rows, a_rows, d_rows

def search_area_box(lower_left, upper_right):
    """
    Return all venues with locations within the given rectangle.
    lower_left and upper_right should both be (lat, lng) pairs

    Returns 2 lists: a list venue rows, and a list of matching address rows.
    """
    minLat, maxLat, minLng, maxLng =  \
    lower_left[0], upper_right[0], lower_left[1], upper_right[1]

    query = """SELECT * FROM Venues 
    INNER JOIN Addresses ON Venues.addressid = Addresses.aid 
    WHERE Addresses.lat > ? AND Addresses.lat < ?
    AND   Addresses.lng > ? AND Addresses.lng < ?
    """

    with dbCursor() as cursor:
        cursor.execute(query, (minLat, maxLat, minLng, maxLng))
        result = cursor.fetchall()
        v_rows = [r[:13] for r in result]
        a_rows = [r[13:] for r in result]
        return v_rows, a_rows
    
def search(join='AND', **patterns):
    """
    Provide patterns of the form {"column":"pattern"} 
    referring to the following fields,
    and a query will be constructed like:

        SELECT * FROM Venues WHERE 
        column1 pattern1 AND
        column2 pattern2 ...
    
    Place a `~` at the beginning of a pattern to perform a
    LIKE comparison, ie match a string pattern.

    By default the comparisons are joined by 'AND', but a different term
    can be specified with `join`, ie `join='OR'` will do an `or` instead 
    of an `and` comparison.

    Returns a list of matching rows.    
        
    For example: 
        select_venues(name="~test%", details="~%d%", bedCount=">1") 

    will return all venues with names starting with test,
    'd' in the details, and more than 1 beds.

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
        minStay       int          
        maxStay       int
        details       text
        ExtSource     url
    """
    # SELECT * FROM Venues WHERE <key> <[LIKE] value>
    query = "SELECT * FROM Venues WHERE "
    # Create parts then join by 'AND'
    parts = []
    subs = []
    for field in patterns:
        val = patterns[field]
        if type(val) != str:
            val = f'= {val}'
        elif val[0] == "~":
            subs.append(val[1:])
            val = 'LIKE ?'
        
        parts.append(f"{field} {val}")
    
    parts = f' {join} '.join(parts)
    query += ' ' + parts

    with dbCursor() as cursor:
        cursor.execute(query, subs)
        return cursor.fetchall()
