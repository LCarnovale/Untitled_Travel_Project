#!/usr/bin/env python3
from routes import app
import db
from src.crawler import Crawler
import os

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        '''
        print('In flask child, running crawler...')

        crawler = Crawler('airbnb')
        crawler.start()

        print('Crawler started')
        '''

        # SIGINT to stop (Ctrl + C)
        app.run(debug=True)

        '''
        print('Server finished, waiting for crawler')

        crawler.kill()
        crawler.wait_for_child()

        print('Crawler finished')
        '''

    else:
        # SIGINT to stop (Ctrl + C)
        app.run(debug=True)
