"""
    Reviews:
    0    revid      int        Identity  PRIMARY KEY
    1    venueid    int        not null  FK -> Venues(id)
    2    userid     int        not null  FK -> Users(id)
    3    postTime   time
    4    postDate   date
    5    rating     tinyint
    6    review     text
"""
from helpers import dbc, execute

def get(id):
    with dbc as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE revid =?", id)
        return cursor.fetchone()

def insert(venueid, userid, postTime, postDate, rating, review):
    with dbc as cursor:
        cursor.execute("INSERT INTO Reviews (venueid, userid, postTime, postDate, rating, review) \
            OUTPUT INSERTED.revid                                                                 \
            VALUES (?, ?, ?, ?, ?, ?)", (venueid, userid, postTime, postDate, rating, review))
        return cursor.fetchone()

def get_from_venue(venueid):
    """
    Fetch all reviews for a given venue.
    Return a list of 
        [ (revid, venueid, userid, postTime, postDate, rating, review), ... ]
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE venueid = ?", (venueid))
        return cursor.fetchall()
