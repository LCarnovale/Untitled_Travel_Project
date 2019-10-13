from accommodation import Accommodation


class AccommodationSystem:
    def __init__(self):
        self.accommodations = []

    '''Adds accommodations into the system'''
    def addAcc(self, acc):
        self.accommodations.append(acc)

    '''Finds an accommodation by a unique ID'''
    def getAcc(self, id):
        for acc in self.accommodations:
            if int(acc.id) == int(id):
                return acc
