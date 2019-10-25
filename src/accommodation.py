class NegativeNumberError(Exception):
    pass


class Accommodation:
    def __init__(self, *args):
        """
        args should follow the layout (schema) of the venue table
        defined in dbTools.py

        The output from eg. db.get_venue(n) has the form
            get_venue(n) --> (id, *args)
        so it is easiest to pass around a collection of the return values after
        the id instead of track each of dozen or so fields individually.
        """ 
        # XXX: Changes to the layout of the venue table will need
        #      to be reflected here
        self._aid,             \
        self._ownerid,         \
        self._name,            \
        self._bed_count,       \
        self._bath_count,      \
        self._car_count,       \
        self._description,     \
        self._rate,            \
        self._avail_start,     \
        self._avail_end,       \
        self._min_stay,        \
        self._max_stay,        \
        self._details =     args

        ### Data validation  ### TODO: Add more tests?
        if self._bed_count < 0:
            raise NegativeNumberError("Invalid bed count")
        if self._bath_count < 0:
            raise NegativeNumberError("Invalid bath count")
        if self._car_count < 0:
            raise NegativeNumberError("Invalid car count")
        

    '''
    Properties
    '''
    
    @property
    def aid(self):
        return self._aid

    @property
    def ownerid(self):
        return self._ownerid

    @property
    def name(self):
        return self._name

    @property
    def bed_count(self):
        return self._bed_count

    @property
    def bath_count(self):
        return self._bath_count

    @property
    def car_count(self):
        return self._car_count

    @property
    def description(self):
        return self._description

    @property
    def rate(self):
        return self._rate

    @property
    def avail_start(self):
        return self._avail_start

    @property
    def avail_end(self):
        return self._avail_end

    @property
    def min_stay(self):
        return self._min_stay

    @property
    def max_stay(self):
        return self._max_stay

    @property
    def details(self):
        return self._details

    # True if not booked and in availability period, otherwise False
    def isAvailable(self):
        #TODO
        return True

