import re

import cloud.dbTools as db
from user import User


class EmailError(Exception):
    pass

class UserSystem:
    def __init__(self):
        self._users = {}

    def add_user(self, uid, user):
        self._users[uid] = user

    def get_user(self, userid):
        '''Finds user given the userID'''
        if userid in self._users:
            return self._users[userid]
        else:
            u = db.get_user(userid)
            if u is not None:
                user = User(*u[1:])
                self.add_user(userid, user)
                return user
            else:
                return None
            

    def create_user(self, name, username, pwd, email, phone, description):
        """
        Attempt to create a user.
        Takes pwd in plain text.
        Return the new user's id on success.
        Return None on failure.
        """
        if self.checkEmail(email) is None:
            raise EmailError("Please enter a valid email address")
        else:
            self._email = email
        # TODO: Verify user input in here

        uid = db.insert_user(name, username, pwd, email, phone, description)
        return uid

    def checkEmail(self, email):
        x = re.search(r"[\w0-9]+@[\w0-9]+\.com", email)
        return x
