###
# Currently this is mainly for fethcing existing reviews
# from the database, not for creating new reviews.
# New reviews should just be put straight in the database.  

class Review:
    def __init__(self, venueid, userid, postDateTime, reccommends, reviewBad, reviewGood):
        self._venueid = venueid
        self._userid = userid
        self._postDateTime = postDateTime
        self._reccommends = reccommends
        self._reviewBad = reviewBad
        self._reviewGood = reviewGood

    '''
    Properties
    '''


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
    def reccommends(self):
        return self._reccommends

    @property
    def reviewBad(self):
        return self._reviewBad

    @property
    def reviewGood(self):
        return self._reviewGood


