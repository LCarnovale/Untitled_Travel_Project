from src.accommodation import Accommodation


class AccommodationSystem:
    def __init__(self):
        self._accommodations = []

    '''Adds accommodations into the system'''
    def addAcc(self, acc):
        self._accommodations.append(acc)

    '''Finds an accommodation by a unique ID'''
    def getAcc(self, id):
        for acc in self._accommodations:
            if int(acc.getID()) == int(id):
                return acc
