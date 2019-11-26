import re

import db
import user
User = user.User

class UserSystemError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class UserCreateError(UserSystemError):
    """Thrown when a user cannot be created"""
    def __init__(self, msg, col=None, err=None):
        # col: column/field causing the error (eg. userName)
        # err: err with the column
        if col is not None:
            msg += f"\nInvalid data in field: {col}"
        if err is not None:
            msg += f"\nError: {err}"
        self.col = col
        self.err = err
        super().__init__(msg)


class UserSystem:
    """
    Handle fetching of users *and* owners from the database,
    and allow updating of existing users and creation of new users.
    """
    def __init__(self):
        self._users = {}
        self._owners = {}

    def add_user(self, uid, user):
        """
        Adds a user to the system
        Sets the id of the user to the given uid.
        """
        self._users[uid] = user
        user._id = uid
        user._type = 'user'
    
    def add_owner(self, oid, owner):
        """
        Adds an owner to the system
        Sets the id of the owner to given oid
        """
        self._owners[oid] = owner
        owner._id = oid
        owner._type = 'owner'

    def get_user(self, userid, u_type='user'):
        '''
        Finds a user or owner given the userID
        u_type should be either 'user' or 'owner'
        Return a user object.
        '''
        if u_type == 'user':
            sys = self._users
            add = self.add_user
            get = db.users.get
        elif u_type == 'owner':
            sys = self._owners
            add = self.add_owner
            get = db.owners.get
        else:
            raise UserSystemError(f"Invalid user type given: '{u_type}'")

        if userid in sys:
            return sys[userid]
        else:
            u = get(userid)
            if u is not None:
                user = User(*u[1:])
                add(userid, user)
                return user
            else:
                return None
    
    def get_owner(self, ownerid):
        '''Finds an owner given the userID'''
        # Might not need this anymore
        if ownerid in self._owners:
            return self._owners[ownerid]
        else:
            u = db.owners.get(ownerid)
            if u is not None:
                owner = User(*u[1:])
                self.add_owner(ownerid, owner)
                return owner
            else:
                return None
 
            

    def create_user(self, name, username, pwd, email, phone, description):
        """
        Attempt to create a user.
        Takes pwd in plain text.
        Return the new user's id on success.
        Return None on failure.
        """
        try:
            _ = User(name, username, email, phone, description)
        except user.EmailError:
            raise UserCreateError("Error creating user.", col='email', err='invalid email')
        except Exception as e:
            raise e
        else:
            try:
                uid = db.users.insert(name, username, pwd, email, phone, description)
            except db.InsertionError as e:
                raise UserCreateError("Error creating user.", col=e.col, err=e.type)        
            else:
                self.get_user(uid) # Adds to the system.
        
        return uid

    def create_owner(self, name, username, pwd, email, phone, description):
        """
        Attempt to create an owner.
        Takes pwd in plain text.
        Return the new owner's id on success.
        Return None on failure.
        """
        try:
            _ = User(name, username, email, phone, description)
        except user.EmailError:
            raise UserCreateError("Error creating user.", col='email', err='invalid email')
        except Exception as e:
            raise e
        else:
            try:
                uid = db.owners.insert(name, username, pwd, email, phone, description)
            except db.InsertionError as e:
                raise UserCreateError("Error creating user.", col=e.col, err=e.type)        
            else:
                self.get_user(uid, 'owner') # Adds to the system.

        return uid

    def set_password(self, uid, new_password, u_type='user'):
        """
        Change the password for a user or owner. The plain password is not
        kept in the user object so the database will be updated when
        this is called, and then the updated user will be reloaded from 
        the database.

        u_type should be either 'user' or 'owner'

        Returns the new user object, which will also be available in
        userSystem under the original id.
        """
        try:
            uid = int(uid)
        except ValueError:
            raise ValueError("uid must be an integer.")

        if u_type == 'user':
            pop = self._users.pop
            update = db.users.update
            get = self.get_user
        elif u_type == 'owner':
            pop = self._owners.pop
            update = db.owners.update
            get = self.get_owner
        else:
            raise UserSystemError("Invalid user type given: '" + u_type + "'")

        pop(uid)
        update(uid, pwdplain=new_password)
        return get(uid)

    def update_user(self, uid, u_type='user'):
        """
        Updates a database record for a user or owner with information
        in the user object from this userSystem. If uid does
        not exist in userSystem an error is raised, because
        there should not be a reason to edit a user that was never loaded.

        u_type should be either 'user' or 'owner'
        """
        if u_type == 'user':
            sys = self._users
            get = db.users.get
            update = db.users.update
        elif u_type == 'owner':
            sys = self._owners
            get = db.owners.get
            update = db.owners.update
        else:
            raise UserSystemError(f"Invalid user type given: '{u_type}'")

        if uid not in sys:
            raise UserSystemError(f"Attempt to edit a {u_type} that has not been loaded.")

        user = sys.pop(uid)

        update(uid,
            name=user.name,
            userName=user.username,
            email=user.email,
            phone=user.mobile,
            description=user.desc
        )
        get(uid)

    def check_user_pass(self, userName, password, u_type='user'):
        """
        Check the user or owner database for a matching username
        and password.

        Return the user's id if found.
        """
        if u_type == 'user':
            check = db.users.check_user_pass
        elif u_type == 'owner':
            check = db.owners.check_user_pass
        else:
            raise UserSystemError(f"Invalid user type given: '{u_type}'")

        r = check(userName, password)
        if r:
            self.get_user(r[0], u_type)
            return r[0]
        else:
            return None

