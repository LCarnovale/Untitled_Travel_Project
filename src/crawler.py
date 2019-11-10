import time
import threading
from airbnbNavigator import Airbnb_Navigator

DELAY = 10 # seconds
LIMIT = 10 # Total pages that can be opened by one crawler




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
            raise Exception('When starting a crawler, use "airbnb".') #TODO: More websites

        self._root_pages = self._navigator.seed_roots()

    def start(self):
        print('Web crawler thread starting')
        self._running = True
        self._child_thread = threading.Thread(target = self._step, args = tuple())
        self._child_thread.start()

    def _step(self):
        if self._pages_to_explore:
            page = self._pages_to_explore.pop()

            self._visit(page)

        else:
            self._pages_to_explore = self._navigator.read_pages_from_route(self._root_pages.pop())

        if self._opened < LIMIT:
            print('zzZ')
            #time.sleep(DELAY)
            input('<enter to continue>')
            self._step()


    def _visit(self, page):
        result = self._navigator.visit_page(page)
        for key in result:
            print(key, ':', result[key]) # Add to db
        self._opened += 1


if __name__ == '__main__':
    print('Running crawler test')

    crawler = Crawler('airbnb')

    print('Made')

    crawler.start()

    print('Thread started')