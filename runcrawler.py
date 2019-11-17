from src.crawler import Crawler
import time

if __name__ == '__main__':
    print('Running crawler test')

    crawler = Crawler('airbnb')

    print('Made')

    crawler.start()

    print('Thread started')

    time.sleep(20)
    crawler.kill()

    crawler.wait_for_child()

    print('Crawler finished')