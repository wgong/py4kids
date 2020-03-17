# https://docs.python.org/3/tutorial/stdlib.html
# Brief Tour of the Standard Library

# Which Version of Python Am I Using?

import sys
print(sys.version)


## Date and Time
# tell me the time
import time
print(time.time())
# number of seconds since January 1, 1970, at 00:00:00 AM

# measure time lapse of each loop
t1 = time.time()
for x in range(0, max):
    print(x)
t2 = time.time()
print('it took %s seconds' % (t2-t1))

print(time.asctime())
t = (2020, 2, 23, 10, 30, 48, 6, 0, 0)
print(time.asctime(t))

local_time = time.localtime()
print(local_time)
year, month, day = t[0], t[1], t[2]

# time to sleep 

for x in range(1, 61):
    print(x)
    time.sleep(1)
    

# dates are easily constructed and formatted
from datetime import date
now = date.today()
now
datetime.date(2003, 12, 2)
now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
# '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

# dates support calendar arithmetic
birthday = date(1964, 7, 31)
age = now - birthday
age.days
#14368


## Random number generator

import random
print(random.randint(1, 100))     # pick a number randomly between 1 and 100
print(random.randint(100, 1000))  # pick a number randomly between 100 and 1000

# Guess a number between 1 and 100
num = random.randint(1, 100)
while True:
    print('Guess a number between 1 and 100')
    guess = input()
    i = int(guess)
    if i == num:
        print('You guessed right')
        break
    elif i < num:
        print('Try higher')
    elif i > num:
        print('Try lower')
        
desserts = ['ice cream', 'pancakes', 'brownies', 'cookies', 'candy']
print(random.choice(desserts))

random.shuffle(desserts)
print(desserts)


    
# pickle python stuff
import pickle
game_data = {
    'player-position' : 'N23 E45',
    'pockets' : ['keys', 'pocket knife', 'polished stone'],
    'backpack' : ['rope', 'hammer', 'apple'],
    'money' : 158.50
}
save_file = open('py-pickle.dat', 'wb')
pickle.dump(game_data, save_file)
save_file.close()
# look at the file

load_file = open('py-pickle.dat', 'rb')
loaded_game_data = pickle.load(load_file)
load_file.close()

print(loaded_game_data)

## math
import statistics
data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
statistics.mean(data)
statistics.median(data)
statistics.variance(data)


## read internet
from urllib.request import urlopen
with urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl') as response:
    for line in response:
        line = line.decode('utf-8')  # Decoding the binary data to text.
        if 'EST' in line or 'EDT' in line:  # look for Eastern Time
            print(line)