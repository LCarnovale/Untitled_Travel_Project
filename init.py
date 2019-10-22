# Initialise the backend in this program
import server


def bootstrap_system():
    import cloud.dbTools as db
    db.init()
    