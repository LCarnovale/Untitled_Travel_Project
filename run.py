#!/usr/bin/env python3
from routes import app
import cloud.dbTools as db

if __name__ == '__main__':
    # SIGINT to stop (Ctrl + C)
    app.run(debug=True)
    print("Closing db connection.")
    try:
        print("Committing changes")
        db.commit()
    except:
        pass
    db.close()
