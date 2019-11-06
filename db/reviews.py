"""
    Reviews:
    0    revid         int        Identity  PRIMARY KEY
    1    venueid       int        not null  FK -> Venues(id)
    2    userid        int        not null  FK -> Users(id)
    3    postDateTime  datetime
    4    reccommends   bit
    5    reviewBad     text
    6    reviewGood    text

"""
from helpers import dbc, execute

def get(id):
    with dbc as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE revid =?", id)
        return cursor.fetchone()

def insert(venueid, userid, postDateTime, recommends, reviewBad, reviewGood):
    with dbc as cursor:
        cursor.execute(
            """INSERT INTO Reviews
            (venueid, userid, postDateTime, reccommends, reviewBad, reviewGood)    
            OUTPUT INSERTED.revid                                                        
            VALUES (?, ?, ?, ?, ?, ?)""", 
            (venueid, userid, postDateTime, reccommends, reviewBad, reviewGood)
        )
        return cursor.fetchone()

def get_for_venue(venueid):
    """
    Fetch all reviews for a given venue.
    Return a list of 
        [ (revid, venueid, userid, postTime, postDate, rating, review), ... ]
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Reviews WHERE venueid = ?", (venueid))
        return cursor.fetchall()
