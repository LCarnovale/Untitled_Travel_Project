from src.crawler import Crawler
import time

TIME_LIMIT = 900    # time in seconds, after which the crawler is forcibly stopped.

if __name__ == '__main__':
    print('Running crawler...')

    crawler = Crawler('airbnb')
    crawler.start()

    print('Thread started, Ctrl-c to stop early.')


    try:
        time.sleep(TIME_LIMIT)
    except KeyboardInterrupt:
        print("** Killing crawler")
    else:
        print("** Times up, ending crawl.")
    finally:
        crawler.kill()

    crawler.wait_for_child()


    print('** Crawler finished')
