#!/usr/bin/env python3
from routes import app
import db
import os

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # SIGINT to stop (Ctrl + C)
        app.run(debug=False)
    else:
        # SIGINT to stop (Ctrl + C)
        app.run(debug=False)
