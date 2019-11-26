"""
    Reviews:
    0    revid         int        Identity  PRIMARY KEY
    1    venueid       int        not null  FK -> Venues(id)
    2    userid        int        not null  FK -> Users(id)
    3    postDateTime  datetime
    4    recommends   bit
    5    reviewBad     text
    6    reviewGood    text

"""
from helpers import dbCursor

def get(id):
    """Return a review with the given id"""
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE revid =?", id)
        return cursor.fetchone()

def insert(venueid, userid, postDateTime, recommends, reviewBad, reviewGood):
    """
    Insert a review into the database.
    
    `venueid`, `userid` should be ints,
    `postDateTime` should be type `datetime.datetime`,
    `recommends` should be True/False, and all others should be strings.
    """
    with dbCursor() as cursor:
        cursor.execute(
            """INSERT INTO Reviews
            (venueid, userid, postDateTime, recommends, reviewBad, reviewGood)    
            OUTPUT INSERTED.revid                                                        
            VALUES (?, ?, ?, ?, ?, ?)""", 
            (venueid, userid, postDateTime, recommends, reviewBad, reviewGood)
        )
        return cursor.fetchone()

def get_for_venue(venueid):
    """
    Fetch all reviews for a given venue.
    Return a list of 
        [ (revid, venueid, userid, postTime, postDate, rating, review), ... ]
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE venueid = ?", (venueid))
        return cursor.fetchall()
