import pyodbc
import time

CURSOR_MAX_OPEN_TIME = 30  # seconds

class ArgumentException(Exception):
    """
    Thrown when an invalid argument or insufficient arguments are given
    for a query
    """
    def __init__(self, message):
        super().__init__(message)


class InsertionError(Exception):
    """Thrown when an insertion fails"""
    def __init__(self, message, col=None, _type=None):
        self.col = col
        self.type = _type
        super().__init__(message)

class ConnectionError(Exception):
    """Thrown when a connection fails"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class FailedConnectionHandler:
    """
    This handles making calls to cursor when a connection was not made.
    This is useful for development and debugging but a failed connection
    will be a genuine problem if it occurs on the main server.
    The return values are based on the context they will be used in.
    """
    def __getattr__(self, attr):
        return None

    def execute(self, *args, **kwargs):
        return self

    def _default(self):
        return None

    commit = _default
    close = _default
    fetchone = _default
    fetchall = _default

try:
    from connect_config import get_connection
except:
    print("Warning: connect_config.get_connection() could not be imported.")
    print("Attempts to access the database will likely cause errors.")

_glob_cnxn = None
_glob_cnxn_open_time = CURSOR_MAX_OPEN_TIME + 1

def close():
    """
    Closes the global connection instance. 
    
    Use of a dbCursor object will still work and will reopen
    a database connection.
    """
    global _glob_cnxn
    global _glob_cnxn_open_time

    try:
        _glob_cnxn.close()
    except:
        pass

    _glob_cnxn_open_time = CURSOR_MAX_OPEN_TIME + 1

class dbCursor:
    """
    A wrapper for a pyodbc cursor object that provides the ability
    to use a cursor without checking for a working connection.

    Intended for use as:

        with dbCursor() as cursor:
            cursor.execute(query, parameters)
            ...

    Here the cursor object will have identical external functionality
    to a pyodbc connection.cursor() object.

    Whenever a dbCursor object is created via the `__enter__` method,
    a singleton global connection is referenced, and if it has been opened
    for too long (longer than `CURSOR_MAX_OPEN_TIME`) 
    or is not already open then it will be opened automatically.

    Upon exiting, the cursor commits all changes, hence there is no need
    to manually commit inside a `with` statement.

    Similarly, if the connection has been used recently, then the same
    connection will be used for the subsequent reference, avoiding
    frequent opening and closing of connections.
    """
    def __enter__(self):
        global _glob_cnxn
        global _glob_cnxn_open_time
        time_delta = time.time() - _glob_cnxn_open_time
        if time_delta > CURSOR_MAX_OPEN_TIME:
            # Restart connection
            try:
                _glob_cnxn.close()
            except:
                pass
            finally:            
                try:
                    self._cnxn = get_connection()
                except TypeError:
                    self._cnxn = FailedConnectionHandler()
                    self._cursor = FailedConnectionHandler()
                except pyodbc.ProgrammingError as e:
                    # Give a nice message including the clients IP address
                    if ("IP address" in str(e)):
                        msg = str(e).split("IP address '")[1]
                        msg = msg.split("' is not")[0]
                        raise ConnectionError("Your ip (" + msg + ") was denied.")
                    else:
                        raise e
                _glob_cnxn = self._cnxn
                _glob_cnxn_open_time = time.time()
        else:
            # Use already open connection
            self._cnxn = _glob_cnxn

        self._cursor = self._cnxn.cursor()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self._cnxn.commit()
        except:
            # If the connection closed or failed somehow we
            # won't be able to commit. 
            pass

    def __getattr__(self, attr):
        # Hand over to the actual cursor object
        return self._cursor.__getattribute__(attr)


def execute(sql, *params):
    """
    Execute a SQL query and return a cursor object. 
    For use of params see: 
    https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters.
    """
    with dbCursor() as cursor:
        out = cursor.execute(sql, params)

    return out

