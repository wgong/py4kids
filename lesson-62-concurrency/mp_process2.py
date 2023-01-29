from multiprocessing import Process


def print_func(arg):
    name, num = arg
    print('The name is : ', name)
    print('The number is : ', num)

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa', 'Asia']
    numbers = list(range(len(names)))
    args = [(names[i],numbers[i]) for i in range(len(names))]

    # instantiating process with arguments
    procs = []
    for arg in args:
        # print(name)
        proc = Process(target=print_func, args=(arg,))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()