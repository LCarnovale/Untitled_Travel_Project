import cloud.dbTools as db

class UserSystem:
    def __init__(self):
        self._users = []

    def addUser(self, user):
        self._users.append(user)

        # TODO: Naughty use of '_' properties here
        db.insert_user(user._name, 
            "sample_username", 
            user._email, 
            user._mobile, 
            user._desc)


    '''Finds user given the userID'''
    def getUser(self, userID):
        for user in self._users:
            if int(userID) == int(user.getID()):
                return user

def create_user(name, username, pwd, email, phone, description):
    """
    Attempt to create a user.
    Return the new user's id on success.
    Return None on failure.
    """
    
    # TODO: Verify user input in here
    uid = db.insert_user(name, username, pwd, email, phone, description)
    return uid
    