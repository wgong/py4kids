# https://www.digitalocean.com/community/tutorials/python-multiprocessing-example

from multiprocessing import Pool

import time

work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])


def worker(work_data):
    print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
    time.sleep(int(work_data[1]))
    print(" Process %s Finished." % work_data[0])


def pool_handler():
    p = Pool(5)
    p.map(worker, work)


if __name__ == '__main__':
    pool_handler()