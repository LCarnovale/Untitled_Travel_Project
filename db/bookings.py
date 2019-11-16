from helpers import dbc, execute, dbCursor
import pyodbc
"""
 id          int        Identity  PRIMARY KEY
 venueid     int        not null  FK -> Venues(id)
 userid      int        not null  FK -> Users(id)
 startDate   date       not null
 endDate     date       not null
"""
def get(id):
    """
    Return a booking with the matching id.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Bookings WHERE bookid=?", id)
        return cursor.fetchone()

def get_for_user(uid):
    """
    Return all bookings for the given user.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Bookings WHERE userid=?", uid)
        return cursor.fetchall() 

def insert(venueid, userid, startDate, endDate):
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
    with dbCursor() as cursor:
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


def update(bookid, **fields):
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

    with dbCursor() as cursor:
        cursor.execute(query, (*vals, bookid))


def search(**patterns):
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
    with dbCursor() as cursor:
        cursor.execute(query, tuple(patterns[c] for c in cols))

        return cursor.fetchall()
