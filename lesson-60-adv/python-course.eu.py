
# coding: utf-8

# https://www.python-course.eu/advanced_topics.php
# 
# https://medium.com/python-features/naming-conventions-with-underscores-in-python-791251ac7097

# https://www.python-course.eu/sys_module.php

# In[1]:

import sys


# In[2]:

dir(sys)


# In[5]:

sys.version


# In[7]:

len(sys.argv), sys.argv


# In[8]:

import sys

print("Coming through stdout")

# stdout is saved
save_stdout = sys.stdout

file_name = "test_sys.txt"
fh = open(file_name,"w")

sys.stdout = fh
print(f"This line goes to {file_name}")
print(f"The END")

# return to normal:
sys.stdout = save_stdout

fh.close()


# In[9]:

get_ipython().system('ls {file_name}')


# In[10]:

get_ipython().system('cat {file_name}')


# In[11]:

sys.byteorder


# In[12]:

# Python interpreter
sys.executable


# In[13]:

# names of modules to modules which have already been loaded
sys.modules


# In[14]:

sys.path


# In[15]:

sys.platform


# In[16]:

# current value of the recursion limit, 
# the maximum depth of the Python interpreter stack
sys.getrecursionlimit()


# 
# 
# shell
# - CLI : command-line interface
# - GUI : graphical user interface
# - API : application programming interface
# 
# System programming provides software or services to the computer hardware, while application programming produces software which provides tools or services for the user.
# 
# https://www.python-course.eu/os_module_shell.php
# 
# `os`, `system()`, `exec()` are 3 ways to interact with OS

# In[28]:

import os
def getch():
     os.system("bash -c \"read -n 1\"")
 


# In[29]:

tmp = os.system("cat test_sys.txt")


# In[1]:

import os, platform
if platform.system() == "Windows":
    import msvcrt
def getch():
    if platform.system() == "Linux":
        os.system("bash -c \"read -n 1\"")
    else:
        msvcrt.getch()


# In[ ]:

print("Type a key!")
getch()
print("Okay")


# In[1]:

import os
dir = os.popen("ls").readlines()
print (dir)


# In[2]:

get_ipython().system('pwd')


# In[9]:

import os

command = ""
while (command != "exit"):
    command = input("Command: ").strip()
    handle = os.popen(command)
    line = " "
    while line:
        line = handle.read()
        print (line)
    handle.close()

print ("Ciao that's it!")


# In[11]:

import subprocess


# In[12]:

x = subprocess.Popen(['touch', 'test2.txt'])


# In[13]:

x, x.poll(), x.returncode


# In[17]:

x = subprocess.Popen(['cat', 'test_sys.txt'], stdout=subprocess.PIPE)


# In[18]:

x, x.poll(), x.returncode


# In[19]:

x.stdout.read()


# In[20]:

os.getcwd()


# https://www.python-course.eu/forking.php
# 
# the term fork stands for at least two different aspects:
# 
# - The cloning of a process.
# - In software engineering, a project fork happens when developers take a legal copy of source code from one software package and start independent development on it. This way starting a distinct piece of software.

# In[21]:

import os

def child():
   print('\nA new child ',  os.getpid())
   os._exit(0)  

def parent():
   while True:
      newpid = os.fork()
      if newpid == 0:
         child()
      else:
         pids = (os.getpid(), newpid)
         print("parent: %d, child: %d\n" % pids)
      reply = input("q for quit / c for new fork")
      if reply == 'c': 
          continue
      else:
          break

parent()


# https://www.python-course.eu/threads.php

# In[29]:

import time
from threading import Thread

def sleeper(i):
    print ("\nthread %d sleeps for 5 seconds" % i)
    time.sleep(5)
    print ("\nthread %d woke up" % i)

for i in range(10):
    t = Thread(target=sleeper, args=(i,))
    t.start()


# ### prime factoring

# In[3]:

import threading 
 
class PrimeNumber(threading.Thread): 
  def __init__(self, number): 
    threading.Thread.__init__(self) 
    self.Number = number
 
  def run(self): 
    counter = 2 
    while counter*counter <= self.Number: 
      if self.Number % counter == 0: 
        print ("\n %d = %d * %d [not prime]" % ( self.Number, counter, self.Number / counter) )
        return 
      counter += 1 
    print (f"\n {self.Number} [prime]")
        
threads = [] 
while True: 
    numbers = [int(n) for n in input("numbers (space delimited, enter 0 to exit): ").split()]
    if len(numbers) == 1 and numbers[0] < 2: 
        break 
 
    for n in numbers:
        if n < 2: continue
        thread = PrimeNumber(n) 
        threads += [thread] 
        thread.start() 

for x in threads: 
    x.join()


# add return_value
# 
# https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python

# In[9]:

def prime_factor(n):
    if n < 2:
        return None
    counter = 2 
    while counter*counter <= n: 
      if n % counter == 0: 
        factor = int(n / counter)
        print ("\n %d = %d * %d [not prime]" % ( n, counter, factor) )
        return (counter, factor)
      counter += 1 
    print (f"\n {n} [prime]")
    return (n,)


# In[12]:

prime_factor(11), prime_factor(1), prime_factor(121)


# In[ ]:

from threading import Thread

class PrimeNumber(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return
        
threads = [] 
while True: 
    numbers = [int(n) for n in input("numbers (space delimited, enter 0 to exit): ").split()]
    if len(numbers) == 1 and numbers[0] < 2: 
        break 
 
    _n2t = {}
    for n in numbers:
        if n < 2: 
            _n2t[n] = None
            continue
        thread = PrimeNumber(target=prime_factor, args=(n,))
        _n2t[n] = thread
        thread.start() 

_n2p = {}
for n,t in _n2t.items():
    if t:
        p = t.join()
        _n2p[n] = p
        


# In[17]:

print(_n2p)


# ### port scan

# In[18]:

import os, re, threading

class ip_check(threading.Thread):
   def __init__ (self,ip):
      threading.Thread.__init__(self)
      self.ip = ip
      self.__successful_pings = -1
   def run(self):
      ping_out = os.popen("ping -q -c2 "+self.ip,"r")
      while True:
        line = ping_out.readline()
        if not line: break
        n_received = re.findall(received_packages,line)
        if n_received:
           self.__successful_pings = int(n_received[0])
   def status(self):
      if self.__successful_pings == 0:
         return "no response"
      elif self.__successful_pings == 1:
         return "alive, but 50 % package loss"
      elif self.__successful_pings == 2:
         return "alive"
      else:
         return "shouldn't occur"
received_packages = re.compile(r"(\d) received")

check_results = []
for suffix in range(20,70):
   ip = "192.168.178."+str(suffix)
   current = ip_check(ip)
   check_results.append(current)
   current.start()

for el in check_results:
   el.join()
   print ("Status from ", el.ip,"is",el.status())


# In[19]:

import os


# In[20]:

os.pipe()


# In[21]:

os.fork()


# In[26]:

def ping(addr):
    import platform
    import socket
    os_type = platform.system() #  "Windows"

    _dict_ports = {
        "Windows" : [135, 137, 138, 139, 445], 
        "Linux" : [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995], 
        "Mac" : [22, 445, 548, 631]
    }
    
    try:
        ports = _dict_ports[os_type]
    except:
        return -1
    
    for port in ports:
        socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = socket_obj.connect_ex((addr,port))
        socket_obj.close()
        if result == 0:
            print(f"{addr}:{port} is open")
            return result
    return 1


# In[27]:

ping("192.168.0.107")


# #### Pytest
# 
# https://www.python-course.eu/python3_pytest.php

# ### Graph
# 
# https://www.python-course.eu/graphs_python.php

# #### NetworkX
# 
# https://www.python-course.eu/networkx.php

# ### Polynomials
# 
# https://www.python-course.eu/polynomial_class_in_python.php

# ### Currying
# 
# https://www.python-course.eu/currying_in_python.php

# ### Finite State Machine (FSM)
# 
# https://www.python-course.eu/finite_state_machine.php

# ### Turing Machine
# 
# https://www.python-course.eu/turing_machine.php

# ### Levenshtein Distance
# 
# https://www.python-course.eu/levenshtein_distance.php

# ### Towers of Hanoi
# 
# https://www.python-course.eu/towers_of_hanoi.php

# ### Mastermind 
# 
# https://www.python-course.eu/mastermind.php

# ### SQL
# 
# https://www.python-course.eu/sql_python.php

# ### Musical score
# 
# https://www.python-course.eu/python_scores.php

# ## Numerical Programming with Python
# 
# https://www.python-course.eu/numerical_programming_with_python.php

# ## Machine Learning
# 
# https://www.python-course.eu/machine_learning.php

# ## Python Tkinter
# 
# https://www.python-course.eu/python_tkinter.php

# In[ ]:



