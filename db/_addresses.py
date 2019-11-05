"""
Addresses:
    0   aid         int        Identity  PRIMARY KEY
    1   location    text
    2   lat         varchar(10)
    3   lng         varchar(10)
"""
from helpers import dbc, execute

def get(id):
    """
    Return an address with the matching id.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Addresses WHERE aid=?", id)
        return cursor.fetchone()


def get_from_venue(venueid):
    """
    Get the address of a given venue.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Addresses WHERE venueid=?", venueid)
        return cursor.fetchone()


def insert(location, lat, lng):
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


def update(aid, location=None):
    """
    Update the location of an address row.
    """
    if location is not None:
        with dbc as cursor:
            cursor.execute(
                'UPDATE Addresses SET location=? WHERE aid=?', (location, aid))
