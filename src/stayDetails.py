from accommodation import NegativeNumberError
from datetime import datetime
class TimeError(Exception):
    pass

class StayDetails:
    def __init__(self, price, avail_start, avail_end, min_stay, max_stay, details):
        self._price = price
        self._details = details
        # If the min_stay is less than 0 or if the max stay is > min stay
        # Raise an error
        if int(min_stay) < 0 or int(max_stay) < 0:
            raise NegativeNumberError("Please enter a positive number")
        elif int(min_stay) > int(max_stay):
            raise TimeError("Please enter a valid stay period")
        else:
            self._min_stay = min_stay
            self._max_stay = max_stay
        # Checks if the dates are correct
        start = datetime.strptime(avail_start, '%Y-%m-%d')
        end = datetime.strptime(avail_end, '%Y-%m-%d')
        now = datetime.now()
        print(now)
        if start < now:
            raise TimeError("Please enter a date after today")
        if start > end:
            raise TimeError("Please enter a valid availability period")
        else:
            self._avail_start = start
            self._avail_end = end


    def getPrice(self):
        return self._price

    def getAvailStart(self):
        #TODO delete print
        print(self._avail_start)
        return self._avail_start

    def getAvailEnd(self):
        #TODO delete print
        print(self._avail_end)
        return self._avail_end

    def getMinStay(self):
        return self._min_stay

    def getMaxStay(self):
        return self._max_stay

    def getDetails(self):
        return self._details
