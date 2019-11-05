# Initialise the backend in this program
import server


def bootstrap_system():
    import db
    db.init()