import re

import cloud.dbTools as db
from user import User

class UserSystemError(Exception):
    def __init__(self, msg):
        super().__init__(msg)



class UserSystem:
    def __init__(self):
        self._users = {}

    def add_user(self, uid, user):
        self._users[uid] = user
        user.__id = uid

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
        # TODO: Verify user input in here
        # Might not be needed since the setters in User() are already checking

        uid = db.insert_user(name, username, pwd, email, phone, description)
        return uid

    def set_password(self, uid, new_password):
        """
        Change the password for a user. The plain password is not
        kept in the user object so the database will be updated when
        this is called, and then the updated user will be reloaded from 
        the database.

        Returns the new user object, which will also be available in
        userSystem under the original id.
        """
        try:
            uid = int(uid)
        except ValueError:
            raise ValueError("uid must be an integer.")
        
        self._users.pop(uid, None)
        db.update_user(uid, pwdplain=new_password)
        return self.get_user(uid)

    def update_user(self, uid):
        """
        Updates a database record for a user with information
        in the user object from this userSystem. If uid does
        not exist in userSystem an error is raised, because
        there should not be a reason to edit a user that was never loaded.
        """
        if uid not in self._users:
            raise UserSystemError("Attempt to edit a user that has not been loaded.")

        user = self.get_user(uid)

        db.update_user(uid,
            name=user.name,
            userName=user.username,
            email=user.email,
            phone=user.mobile,
            description=user.desc
        )

        




