"""
Database methods for owners.
Table schema:

    Owners:
    0   ownerid/userid  int          Identity   PRIMARY KEY
    1   name            varchar(50)  not null
    2   userName        varchar(50)             UNIQUE
    3   email           varchar(100)
    4   phone           varchar(20)
    5   description     text
    6   pwdhash         bytes

"""
from helpers import dbc, execute


def get(id):
    """
    Return an owner with the matching id.

    Return None if the owner does not exist.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners WHERE ownerid=?", id)
        return cursor.fetchone()

def get_from_uname(userName):
    """
    Return an owner matching the given userName.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners WHERE userName=?", userName)
        return cursor.fetchone()

def insert(name, userName, password, email=None, phone=None, description=None):
    """
    Insert an owner into the database with the given details. 
    Give the raw text password and the SHA2_512 hash will be stored,
    calculated with HASHBYTES('SHA2_512', '<password>').

    Attempting to add duplicate usernames raises a pyodbc.IntegrityError.

    Returns the id of the inserted owner.
    """
    with dbc as cursor:
        try:
            cursor.execute(
                "INSERT INTO Owners (name, userName, email, phone, description, pwdhash)   \
                OUTPUT INSERTED.ownerid VALUES (?, ?, ?, ?, ?, HASHBYTES('SHA2_512', ?))",
                (name, userName, email, phone, description, password)
            )
        except pyodbc.IntegrityError as e:
            print("Duplicate username on insert.")
            raise e

        res = cursor.fetchone()
        if res is not None:
            return int(res[0])
        else:
            return None


def update(ownerid, **fields):
    """
    Update a owner record. Takes the id of the owner to be updated (ownerid)
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
        update_owner(1, email='e@mail.com')  # Change the owner's email.
    Or
        kwargs = {'email': 'e@mail.com', 'phone': '12345'}
        update_owner(2, **kwargs)  # Change the owner's phone number and email.
    """

    valid_fields = (
        "name", "userName", "email", "phone", "description", "pwdhash", "pwdplain"
    )

    if 'ownerid' in fields:
        raise ArgumentException("Unable to change a owner's id.")

    if 'pwdplain' in fields and 'pwdhash' in fields:
        raise ArgumentException(
            "Can not change plain text password and password hash fields simultaneously.")

    query = "UPDATE Owners SET "

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
    query += " WHERE ownerid=?"
    with dbc as cursor:
        cursor.execute(query, (*vals, ownerid))

def check_user_pass(username, password_text):
    """
    Search owners for an owner with the matching username and password.
    
    If username and password match, return that row.
    Otherwise return None.
    """
    with dbc as cursor:
        cursor.execute("SELECT * FROM Owners \
            WHERE userName=? AND pwdhash=HASHBYTES('SHA2_512', ?)", (username, password_text))

        return cursor.fetchone()
