import cloud.dbTools as dbTools

class UserSystem:
    def __init__(self):
        self._users = []

    def addUser(self, user):
        self._users.append(user)

        # TODO: Naughty use of '_' properties here
        dbTools.insert_user(user._name, 
            "sample_username", 
            user._email, 
            user._mobile, 
            user._desc)


    '''Finds user given the userID'''
    def getUser(self, userID):
        for user in self._users:
            if int(userID) == int(user.getID()):
                return user
