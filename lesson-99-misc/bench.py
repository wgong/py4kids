from __future__ import print_function
from math import sin, cos, radians
import timeit

'''
A simple Python benchmark.
Results on an overclocked AMD FX-8150 Eight-Core CPU @ 3.0 GHz, and
an Intel Core i5-2410M CPU @ 2.30GHz.
$ python -OO bench.py
1.99843406677 2.00139904022 2.0145778656
2.38226699829 2.38675498962 2.38853287697
$ python3 -OO bench.py
2.2073315899979207 2.2098999509980786 2.222747125000751
2.273064840992447  2.274112678001984 2.2759074380010134
$ pypy -OO bench.py
0.245079994202 0.24707698822  0.247714996338
0.241708040237 0.242873907089 0.245008945465
$ pypy3 -OO bench.py
1.1291401386260986 1.1360960006713867 1.1375579833984375
1.2108190059661865 1.2172389030456543 1.2178328037261963
'''


def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product

if __name__ == '__main__':
    result = timeit.repeat('bench.bench()', setup='import bench', number=10, repeat=10)
    result = list(sorted(result))
    print(*result[:3])
