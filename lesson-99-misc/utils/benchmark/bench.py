# https://gist.github.com/apalala/3fbbeb5305584d2abe05

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


=======
$ python -OO bench.py
2.8172007999999984 2.820085500000001 2.820299500000001 # dell (old)

4.219677300000001 4.3009831 4.419679899999999   # hp laptop

3.641036200000002 3.6584530000000006 3.660798399999999  # hp laptop - SSD win10
3.6480506000000004 3.7242099000000017 3.728094200000001

### ubuntu desktop (gong/old)
2.487754242000392 2.497233943000083 2.514756731000034  
2.487754242000392 2.497233943000083 2.514756731000034

### new HP laptop - SSD win11 2023-01-13
# run in windows terminal
1.9440819000000005 1.9506948000000008 1.9515835000000017
# run in wsl terminal
0.9696858639999988 0.9833493269999991 0.9867643839999971

### ubuntu desktop (wengong w/ gpu)
1.014563090000138 1.0159679270000197 1.0165140320000319  
0.9325788260000252 0.933943456999998 0.9367006509999953  
0.9086168119999911 0.9109127770000214 0.9206913379999833 
0.9934165070000063 0.9940060090000316 0.9941820540000208  # ubuntu 22.04
0.9086168119999911 0.9109127770000214 0.9206913379999833 

# Gaming PC Win desktop
1.6540939000000003 1.6591958 1.6695383999999998          # Anaconda py3.7 - 2023-07-02
0.8121546999999936 0.815331999999998 0.8159291999999994  # wsl - ubuntu py 3.7.3
1.8178790000001754 1.8855526999996073 1.9135384999999587  # Anaconda py3.10 - 2023-07-02

$ cd ~/lesson-99-misc/benchmark
$ micromamba create -n py39 python=3.9
$ micromamba activate py39
$ python --version
Python 3.9.13
$ python bench.py 
1.8920940999999978 1.8966619999999992 1.901398900000002

$ micromamba create -n py311 python=3.11
$ micromamba activate py311
$ python --version
Python 3.11.6
$ python bench.py 
1.8258523999829777 1.8263571000134107 1.8272148000251036

# Gaming PC (duckpod101) - ibuypower.com 
## windows - anaconda python 3.11
0.8525097000019741 0.8558419999972102 0.8566847999973106
## WSL python 3.10
0.40655699500001674 0.4066487719999827 0.4069020829999772
## Ubuntu py 3.11.5
0.3376696390005236 0.3383675219993165 0.33882533100040746

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