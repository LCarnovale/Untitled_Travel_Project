import time
import threading
from airbnbNavigator import Airbnb_Navigator
import db
from datetime import datetime, timedelta

DELAY = 3   # minimum time in seconds between each site visit
LIMIT = 100 # Total pages that can be opened by one crawler before it stops itself


class Crawler:
    '''
    Generic web crawler class

    The web crawler should run on a completely separate machine to the server,
    to avoid any database synchronisation issues.

    Navigator classes are duck-typed and must implement the following:
        seed_roots(): initialise root urls
        next_roots(prev_root): return a list of root urls, given the root url prev_root is exhausted.
        read_pages_from_route(root_path): given a root url, return a list of all the urls of visitable pages.
        visit_page(page_path): visit a page at the page_path url. Return the following:
        {
            'name':         # str

            'location':     # str
            'lat':          # str
            'lng':          # str

            'bedCount':     # str or int
            'bathCount':    # str or int
            'carCount':     # str or int
            'description':  # str

            'rate':         # str, int or float
            'minStay':      # str
            'maxStay':      # str
            'details':      # str

            'images':       # [str]
            'dates':        # [datetime.datetime]

            'ad_url':       # str
            'poster_url':   # str
        }
    '''

    def __init__(self, webpage):
        '''
        Initialises a Crawler class.

        webpage is a string representing the webpage to crawl.
        Currently, only 'airbnb' is available.
        '''

        self._pages_to_explore = [] # List of pages the crawler is going to explore
        self._root_pages = []       # List of "root pages", typically search result pages.
        self._opened = 0            # Number of pages visited
        self._running = False       # Whether the crawler is running. If set to False, crawler will stop after the current iteration.
        self._child_thread = None   # Object representing the child thread of the crawler.

        self._navigator = None      # Abstract object for site-specific navigation

        if webpage == 'airbnb':
            self._navigator = Airbnb_Navigator()
        else:
            raise Exception('When starting a crawler, use "airbnb".')

        # Get the first set of root pages
        self._root_pages = self._navigator.seed_roots()

    def start(self):
        '''
        Starts the crawler running in a new thread.
        '''
        print('Web crawler thread starting')

        self._running = True
        self._child_thread = threading.Thread(target = self._run, args = tuple())
        self._child_thread.start()

    def kill(self):
        '''
        Stops a crawler thread smoothly, after the current page is done.
        If this is called on a crawler that is already stopped, it does nothing.
        '''
        print('Telling crawler to stop')
        self._running = False

    def wait_for_child(self):
        '''Halts current process until the crawler (child thread) finishes.'''
        self._child_thread.join()

    def _run(self):
        '''
        Where the crawler starts execution.
        Crawler will visit a page if there are any, or request new pages if there aren't.
        This repeats every DELAY seconds, until the crawler is kill()'d,
         or it has visited LIMIT-many sites
        '''
        while self._running and self._opened < LIMIT:
            time.sleep(DELAY)

            if self._pages_to_explore:
                # Explore a lisitng
                page = self._pages_to_explore.pop()
                try:
                    self._visit(page)
                except Exception as e:
                    print('Error visiting page, skipping...')

            else:
                # Find more search results
                if not self._root_pages: # No root pages left to make further root pages
                    print('Crawler starved, ending early')
                    break

                old_root = self._root_pages.pop()
                self._pages_to_explore = self._navigator.read_pages_from_route(old_root)
                self._root_pages += self._navigator.next_roots(old_root)

            print('Crawled', self._opened, 'so far')

        print('Crawler, signing off...')


    def _visit(self, page):
        '''Visit a single page, parsing it and inserting into database'''
        result = self._navigator.visit_page(page)

        venueid = -1

        aid = db.addresses.insert(result['location'],
                                  result['lat'].strip(),
                                  result['lng'].strip())

        venueid = db.venues.insert(
            -1, int(aid), result['name'], int(result['bedCount']),
            int(result['bathCount']), int(result['carCount']),
            result['description'],   float(result['rate']), int(result['minStay']),
            int(result['maxStay']), result['details'], result['ad_url']
        )

        for url in result['images']:
            db.images.insert(venueid, url)

        self._simplifyDates(venueid, result['dates'])


        self._opened += 1


    def _simplifyDates(self, venueid, dates):
        '''
        Simplifies the list of available dates 'dates' to a series of date ranges.
        Inserts this into the database for venueid.
        '''
        i = 0

        while i < len(dates):
            start_date = dates[i]
            cur_date = dates[i]

            while i < len(dates) - 1 and cur_date + timedelta(1) == dates[i+1]:
                cur_date = dates[i+1]
                i += 1

            db.availabilities.insert(
                venueid, start_date, cur_date
            )

            i += 1