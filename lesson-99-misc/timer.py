"""
Timer:
https://www.confessionsofadataguy.com/replacing-pandas-with-polars-a-practical-guide/
"""


#!/usr/bin/env python
#
#  Python Timer Class - Context Manager for Timing Code Blocks
#  Corey Goldberg - 2012
#


from timeit import default_timer

class Timer(object):
    CONVERSION = {
            "sec": 1,
            "min": 1/60.0,
            "hr": 1/3600.0, 
            "millisec": 1000, 
            "microsec": 1000000,
        }

    def __init__(self, verbose=False, unit="sec"):
        unit = unit.lower()
        if unit.startswith("mil"): unit = "millisec"
        elif unit.startswith("mic"): unit = "microsec"
        elif unit.startswith("h"): unit = "hr"
        self.unit = unit if unit in ["sec", "min", "hr", "millisec", "microsec"] else "sec"
        self.verbose = verbose
        self.timer = default_timer
        self.elapsed = 0
        
    def __enter__(self):
        self.start = self.timer()
        return self
        
    def __exit__(self,  *args):
        self.elapsed = (self.timer() - self.start) * self.CONVERSION[self.unit]
        if self.verbose:
            print(f'Elapsed time: {self.elapsed:.6f} {self.unit}')

if __name__ == '__main__':
    # example:
    #   'HTTP GET' from requests module, inside timer blocks.
    #   invoke the Timer context manager using the `with` statement.
    
    import requests
    
    url = 'https://github.com/timeline.json'
    
    # verbose (auto) timer output
    with Timer(verbose=True) as t:
        r = requests.get(url)

    
    # verbose=False
    with Timer() as t:
        r = requests.get(url)
    print(f'Elapsed time: {t.elapsed:.6f} {t.unit}')
    

    # verbose=False, unit = min
    with Timer(unit="min") as t:
        r = requests.get(url)
    print(f'Elapsed time: {t.elapsed:.6f} {t.unit}')

    # verbose=False, unit = millisec
    with Timer(unit="millisec") as t:
        r = requests.get(url)
    print(f'Elapsed time: {t.elapsed:.6f} {t.unit}')

#  example output:
#
#    $ python timer.py 
#    elapsed time: 652.403831 ms
#    response time (millisecs): 635.49
#    response time (secs): 0.624