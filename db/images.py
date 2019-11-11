"""
Images:
    imId     int      PRIMARY KEY
    venueid  int      FK -> Venues(venueid)
    path     varchar(250)
"""

from helpers import dbc, execute, dbCursor
import helpers
import pyodbc

def get(id):
    """
    Geth the path and venue information for a given image id.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM images WHERE id = ?", id)
        return cursor.fetchone()

def get_for_venue(venueid):
    """
    Fetch all image rows for a given venue.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM images WHERE venueid = ?", venueid)
        return cursor.fetchall()

def insert(venueid, path):
    """
    Insert a new image for a given venue.
    """
    with dbCursor() as cursor:
        try:
            cursor.execute("INSERT INTO images (venueid, path) \
                OUTPUT INSERTED.imId                           \
                VALUES (?, ?)", (venueid, path))
        except pyodbc.IntegrityError:
            print("Integrity error: venueid must refernce an existing venue.")
            raise helpers.InsertionError("venueid must refernce an existing venue.", 
                col='venueid')
        else:
            return cursor.fetchone()[0]