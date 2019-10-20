# Initialise the backend in this program
import server


def bootstrap_system():
    import cloud.dbTools as db
    db.init()
    
    # Debug: Get the latest commit
    f = open(".git/HEAD", 'r')
    com = f.read()
    f.close()
    if 'ref:' in com:
        f = open(".git/" + com[5:-1], 'r')
        com = f.read()
        f.close()
    
    server.DBG_current_commit = com