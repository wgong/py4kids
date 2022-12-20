import multiprocessing
import random
import time
import sys

EXPONENT = 3

def do_calculation(data):
    # data = (number, exponent)
    num, exp = data
    sl_time = random.randint(1,3)
    time.sleep(sl_time)
    return num, num ** exp, f"sl_time:{sl_time}"


def start_process():
    print('Starting', multiprocessing.current_process().name)

def processor_multi(max_n, pool_factor, first_n=20):
    ts_start = time.time()
    inputs = [(n, EXPONENT) for n in range(max_n)]
    print(f'max_n = {max_n}, pool_factor = {pool_factor} \nInput: {inputs[:first_n]}')

    # builtin_outputs = map(do_calculation, inputs)
    # print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * pool_factor
    pool = multiprocessing.Pool(
        processes=pool_size,
        # initializer=start_process,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    ts_stop = time.time()
    print(f'Output:  {pool_outputs[:first_n]}')
    print(f"completed in {ts_stop - ts_start} sec")

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 2: 
        processor_multi(int(sys.argv[1]), int(sys.argv[2]))
