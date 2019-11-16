"""
Availabilities:
    0   avId          int        Identity  PRIMARY KEY
    1   venueid       int                  FK -> Venues(id)
    2   startDate     date
    3   endDate       date
"""

from helpers import execute, dbCursor


def get(id):
    """
    Get an availability matching the given id.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE avId=?", id)
        return cursor.fetchone()


def get_overlapping(startDate, endDate):
    """
    Get all availabilities that contain the given period in their
    start and end dates.
    Returns a list of availability rows.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Availabilities WHERE \
            startDate<? AND endDate>?", (startDate, endDate))
        return cursor.fetchall()


def insert(venueid, startDate, endDate):
    """
    Insert an availability and return the id of the new availability.
    """
    with dbCursor() as cursor:
        cursor.execute(
            "INSERT INTO Availabilities (venueid, startDate, endDate) OUTPUT INSERTED.avId VALUES (?, ?, ?)", (
                venueid, startDate, endDate)
        )
        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None
