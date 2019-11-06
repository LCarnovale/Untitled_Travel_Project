from helpers import dbc, execute


def get_all():
    """
    Return a venue with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Venues")
        return cursor.fetchall()


def get(id):
    """
    Return a venue with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Venues WHERE venueid=?", id)
        return cursor.fetchone()


def get_availabilities(venueid):
    """
    Return all availabilities for a venue with the
    given venueid.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities  \
            WHERE venueid=?", venueid)
        return cursor.fetchall()

def get_overlapping_availability(venueid, startDate, endDate):
    """
    Get availabilities that contain the given period in their
    start and end dates for a given venue id.
    Returns a list of availability rows.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE \
            venueid=? AND startDate<=? AND endDate>=?", (venueid, startDate, endDate))
        return cursor.fetchall()


def insert(ownerid, addressid, name, bedCount, bathCount,
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


def select(**patterns):
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
