import multiprocessing
import os
import sys
import urllib
import random
import time

import graphitesend


INTERVAL = 3.0
PERIOD = 10.0


def main():
    download_url = sys.argv[1]
    print('Starting download_url={}'.format(download_url))

    print('Init graphitesend')
    g = graphitesend.init(graphite_server=os.environ['GRAPHITE_SERVER'],
                          graphite_port=int(os.environ['GRAPHITE_PORT']),
                          prefix='bandwidth')

    while True:
        start = time.time()

        filename = 'download{0:07d}'.format(random.randint(0, 1000000))
        p = multiprocessing.Process(target=_download, args=(download_url, filename))
        p.start()
        time.sleep(INTERVAL)
        p.terminate()

        size = _file_size(filename)
        bandwidth = size / INTERVAL
        print('bandwidth={}'.format(bandwidth))
        g.send('time', bandwidth)

        _remove(filename)

        end = time.time()
        if end - start < PERIOD:
            time.sleep(PERIOD - end + start)


def _download(download_url, filename):
    urllib.urlretrieve(download_url, filename)


def _file_size(filename):
    try:
        return os.path.getsize(filename)
    except OSError:
        print('failed to get file size filename={}'.format(filename))
        return 0


def _remove(filename):
    try:
        os.remove(filename)
    except OSError:
        print('failed to remove file filename={}'.format(filename))


if __name__ == '__main__':
    main()
