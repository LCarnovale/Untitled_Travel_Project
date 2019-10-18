class StayDetails:
    def __init__(self, price, avail_start, avail_end, min_stay, max_stay, details):
        self._price = price
        self._avail_start = avail_start
        self._avail_end = avail_end
        self._min_stay = min_stay
        self._max_stay = max_stay
        self._details = details

    def getPrice(self):
        return self._price

    def getAvailStart(self):
        return self._avail_start

    def getAvailEnd(self):
        return self._avail_end

    def getMinStay(self):
        return self._min_stay

    def getMaxStay(self):
        return self._max_stay

    def getDetails(self):
        return self._details
