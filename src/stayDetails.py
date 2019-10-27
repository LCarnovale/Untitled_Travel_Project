from accommodation import NegativeNumberError
import re
from datetime import datetime
class TimeError(Exception):
    pass

class StayDetails:
    def __init__(self, price, avail_dates, min_stay, max_stay, details):
        self._details = details
        self._avail_dates = []
        # Check if the price is positive
        if int(price) < 0:
            raise NegativeNumberError("Please enter a positive number")
        else:
            self._price = price
        # If the min_stay is less than 0 or if the max stay is > min stay
        # Raise an error
        if int(min_stay) < 0 or int(max_stay) < 0:
            raise NegativeNumberError("Please enter a positive number")
        elif int(min_stay) > int(max_stay):
            raise TimeError("Please enter a valid stay period")
        else:
            self._min_stay = min_stay
            self._max_stay = max_stay

        now = datetime.now()
        # Dates are given as a string separated by commas
        # Dates are already sorted
        dates = re.split(', ', avail_dates)
        # Check if the first date is after today
        first_date = dates[0]
        start = datetime.strptime(first_date, '%d-%m-%Y')
        if start < now:
            raise TimeError("Please enter a dates after today")
        else:
            self._avail_dates = dates

    def getPrice(self):
        return self._price

    def getMinStay(self):
        return self._min_stay

    def getMaxStay(self):
        return self._max_stay

    def getDetails(self):
        return self._details

    def isAvailable(self):
        if self._avail_dates:
            return True
        else:
            return False

    def getDates(self):
        return self._avail_dates


