from src.crawler import Crawler
import time

if __name__ == '__main__':
    print('Running crawler...')

    crawler = Crawler('airbnb')
    crawler.start()

    print('Thread started')

    try:
        time.sleep(900)
    except KeyboardInterrupt:
        print("** Killing crawler")
    else:
        print("** Times up, ending crawl.")
    finally:
        crawler.kill()



    crawler.wait_for_child()

    print('** Crawler finished')
