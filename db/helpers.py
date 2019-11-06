import pyodbc
class ArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsertionError(Exception):
    def __init__(self, message, col=None, _type=None):
        self.col = col
        self.type = _type
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

from connect_config import get_connection
class dbCursor:
    def __enter__(self):
        try:
            self._cnxn = get_connection()
        except TypeError:
            print("Connection has not been established yet. Call init().")
            self._cnxn = FailedConnectionHandler()
            self._cursor = FailedConnectionHandler()
        except pyodbc.ProgrammingError as e:
            if ("IP address" in str(e)):
                msg = str(e).split("IP address '")[1]
                msg = msg.split("' is not")[0]
                print("Your ip (" + msg + ") was denied.")
            else:
                raise e
            self._cnxn = FailedConnectionHandler()
            self._cursor = FailedConnectionHandler()
        else:
            self._cursor = self._cnxn.cursor()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._cnxn.commit()
        self._cnxn.close()

    def __getattr__(self, attr):
        return self._cursor.__getattribute__(attr)


def execute(sql, *params):
    """
    Execute a SQL query and return a cursor object. 
    For use of params see: 
    https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters.
    """
    with dbc as cursor:
        out = cursor.execute(sql, params)

    return out


dbc = dbCursor()
