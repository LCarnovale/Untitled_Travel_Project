"""
Database methods for the Users table.
Table schema:

    Users:
    0   ownerid/userid  int          Identity   PRIMARY KEY
    1   name            varchar(50)  not null
    2   userName        varchar(50)             UNIQUE
    3   email           varchar(100)
    4   phone           varchar(20)
    5   description     text
    6   pwdhash         bytes
"""
from helpers import dbc, execute, dbCursor

def get(id):
    """
    Return a single user with the matching id from the database

    Returns None if the user does not exist.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE userid=?", id)
        return cursor.fetchone()

def get_from_uname(userName):
    """
    Return a single user with the matching username, or None if it doesn't exist.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE userName=?", userName)
        return cursor.fetchone()

def insert(name, userName, password, email=None, phone=None, description=None):
    """
    Insert a user into the database with the given details. 
    Give the raw text password and the SHA2_512 hash will be stored,
    calculated with HASHBYTES('SHA2_512', '<password>').

    Attempting to add duplicate usernames raises a pyodbc.IntegrityError.

    Returns thqe id of the inserted user.
    """

    ## Fields:
    #  id           int          Identity   PRIMARY KEY
    #  name         varchar(50)  not null
    #  userName     varchar(50)
    #  email        varchar(100)
    #  phone        varchar(20)
    #  description  text

    # Make sure username is unique:
    with dbCursor() as cursor:
        if (cursor.execute("SELECT * FROM users WHERE username = ?", userName).fetchone()):
            raise InsertionError(
                "Username already exists in users table.", col='userName', _type='duplicate')

        try:
            cursor.execute(
                "INSERT INTO Users (name, userName, email, phone, description, pwdhash)   \
                OUTPUT INSERTED.userid VALUES (?, ?, ?, ?, ?, HASHBYTES('SHA2_512', ?))",
                (name, userName, email, phone, description, password)
            )
        except pyodbc.IntegrityError as e:
            raise e
            # raise InsertionError("SQL Integrity Error, likely a duplicate username on insert.")

        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None

def update(userid, **fields):
    """
    Update a user record. Takes the id of the user to be updated (userid)
    and keyword arguments corresponding to the table's schema.
    pwdhash and pwdplain must not be supplied at the same time, as both
    affect the pwdhash field.

    ** To update the password: **
    Changing the pwdhash is not recommended. Instead, provide a plain text 
    password for the keyword pwdplain and the hash will be calculated and
    stored.

    valid fields are:
        name, userName, email, phone, description, pwdhash, pwdplain

    Usage:
        update_user(1, email='e@mail.com')  # Change the user's email.
    Or
        kwargs = {'email': 'e@mail.com', 'phone': '12345'}
        update_user(2, **kwargs)  # Change the user's phone number and email.
    """

    valid_fields = (
        "name", "userName", "email", "phone", "description", "pwdhash", "pwdplain"
    )

    if 'userid' in fields:
        raise ArgumentException("Unable to change a user's id.")

    if 'pwdplain' in fields and 'pwdhash' in fields:
        raise ArgumentException(
            "Can not change plain text password and password hash fields simultaneously.")

    query = "UPDATE Users SET "

    for f in fields:
        if f not in valid_fields:
            raise ArgumentException("Invalid field name: " + f)

    # Build the rest of the query
    keys = [f for f in fields]
    # Do this to ensure dict ordering is irrelevant
    vals = [fields[k] for k in keys if k != 'pwdplain']
    s = [f"{f} = ?" for f in keys if f != 'pwdplain']
    if 'pwdplain' in keys:
        s.append("pwdhash = HASHBYTES('SHA2_512', ?)")
        vals.append(fields['pwdplain'])
    s = ' , '.join(s)
    query += s
    query += " WHERE userid=?"
    with dbCursor() as cursor:
        cursor.execute(query, (*vals, userid))

def check_user_pass(username, password_text):
    """
    Search users for a user with the matching username and password.
    
    If username and password match, return that row.
    Otherwise return None.
    """
    with dbCursor() as cursor:
        cursor.execute("SELECT * FROM Users \
            WHERE userName=? AND pwdhash=HASHBYTES('SHA2_512', ?)", (username, password_text))

        return cursor.fetchone()

