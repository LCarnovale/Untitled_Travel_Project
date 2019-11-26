###
# Currently this is mainly for fethcing existing reviews
# from the database, not for creating new reviews.
# New reviews should just be put straight in the database.  

import db

def get_for_venue(venueid):
    """
    Get a list of review objects for a given venue.
    Returns a list of Reviews.

    Unlike similar classes, reviews are not cached as they are too numerous.
    Because of this, there is no class to store them, just a function.
    """
    reviews = db.reviews.get_for_venue(venueid)
    return [Review(*x[1:]) for x in reviews]



class Review:
    """
    Holds attributes for a review based on the columns in the review
    table in the database.
    """
    def __init__(self, venueid, userid, postDateTime, recommends, reviewBad, reviewGood):
        """
        Holds attributes for a review based on the columns in the review
        table in the database.
        """
        self._venueid = venueid
        self._userid = userid
        self._postDateTime = postDateTime
        self._recommends = recommends
        self._reviewBad = reviewBad
        self._reviewGood = reviewGood

    '''
    Properties
    '''

    @property
    def username(self):
        user = db.users.get(self.userid)
        return user[2]

    @property
    def venueid(self):
        return self._venueid

    @property
    def userid(self):
        return self._userid

    @property
    def postDateTime(self):
        return self._postDateTime

    @property
    def recommends(self):
        return self._recommends

    @property
    def reviewBad(self):
        return self._reviewBad

    @property
    def reviewGood(self):
        return self._reviewGood


