# Tools to interact with our database.
# import pyodbc

# This handles making calls to cursor when a connection was not made.
# This is useful for development and debugging but a failed connection
# will be a genuine problem if it occurs on the main server.
class FailedConnectionHandler:
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return lambda *x: None

try: 
    import connect_config
    cnxn = connect_config.get_connection()
except:
    print("Unable to connect to database. Function calls will do nothing.")
    cursor = FailedConnectionHandler()
else:
    cursor = cnxn.cursor()

########
# If returning a direct cursor object or cursor attribute, it's good to check if a
# connection was ever made because if not, then unless you are 
# returning something like cursor.func() there is a chance 
# cursor.attr will return a lambda func, or cursor will be a FailedConnectionHandler
# object. You will probably want to instead return None in these cases.  
########

def execute(sql, *params):
    """
    Execute a SQL query and return a cursor object. 
    For use of params see: 
    https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters.
    """
    return cursor.execute(sql, params)
    
def get_user(id):
    """
    Return a user with the matching id from the database

    Returns None if the user does not exist.
    """
    cursor.execute("SELECT * FROM Users WHERE id=?", id)
    result = cursor.fetchone()
    # if result is None:
    return result

def insert_user(name, userName, email=None, phone=None, description=None):
    cursor.execute(
        "INSERT INTO users (name, userName, email, phone, description)   \
         VALUES (?, ?, ?, ?, ?)"
    )


    





