class UserSystem:
    def __init__(self):
        self._users = []

    def addUser(self, user):
        self._users.append(user)

    '''Finds user given the userID'''
    def getUser(self, userID):
        for user in self._users:
            if int(userID) == int(user.getID()):
                return user
