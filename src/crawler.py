import time
import threading
from airbnbNavigator import Airbnb_Navigator
import db
from datetime import datetime, timedelta

DELAY = 3 # seconds
LIMIT = 100 # Total pages that can be opened by one crawler


class Crawler:
    def __init__(self, webpage):
        self._pages_to_explore = []
        self._root_pages = []
        self._opened = 0
        self._running = False
        self._child_thread = None

        self._navigator = None

        if webpage == 'airbnb':
            self._navigator = Airbnb_Navigator()
        else:
            raise Exception('When starting a crawler, use "airbnb".')

        self._root_pages = self._navigator.seed_roots()

    def start(self):
        print('Web crawler thread starting')
        self._running = True
        self._child_thread = threading.Thread(target = self._step, args = tuple())
        self._child_thread.start()

    def kill(self):
        print('Telling crawler to stop')
        self._running = False

    def wait_for_child(self):
        self._child_thread.join()

    def _step(self):
        while self._running and self._opened < LIMIT:
            #print('zzZ')
            time.sleep(DELAY)
            #input('<enter to continue>')
            print("I wait for no man")

            if self._pages_to_explore:
                page = self._pages_to_explore.pop()
                try:
                    self._visit(page)
                except Exception as e:
                    print('Error visiting page, skipping...')
                    raise e
            else:
                if not self._root_pages:
                    print('Crawler starved, ending early')
                    break

                old_root = self._root_pages.pop()
                self._pages_to_explore = self._navigator.read_pages_from_route(old_root)
                self._root_pages += self._navigator.next_roots(old_root)
            print('Crawled', self._opened, 'so far')

        print('Crawler, signing off...')


    def _visit(self, page):
        result = self._navigator.visit_page(page)

        venueid = -1

        #for key in result:
        #    print(key, ':', result[key])

        '''
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
        '''

        self._opened += 1


    def _simplifyDates(self, venueid, dates):
        i = 0

        while i < len(dates):

            start_date = dates[i]
            cur_date = dates[i]

            while i < len(dates) - 1 and cur_date + timedelta(1) == dates[i+1]:
                cur_date = dates[i+1]
                i += 1

            print(start_date, cur_date)
            i += 1
            db.availabilities.insert(
                venueid, start_date, cur_date
            )


if __name__ == '__main__':
    print('Running crawler test')

    crawler = Crawler('airbnb')

    print('Made')

    crawler.start()

    print('Thread started')

    crawler._child_thread.join()

    print('Crawler finished')
