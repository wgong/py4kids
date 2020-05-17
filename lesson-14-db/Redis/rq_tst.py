from redis import Redis
from rq import Queue
import time
from rq_func import *

q = Queue(connection=Redis())

job = q.enqueue(count_words_at_url, 'http://nvie.com')
time.sleep(1)
if job.is_finished:
    print(job.result)
             
job = q.enqueue(count_words_at_url, 'https://python-rq.org/')
time.sleep(1)
if job.is_finished:
    print(job.result)


# submit jobs
jobs = []
for i in range(1,6):

    job = q.enqueue_call(func=sum_list, args=(range(i*10),), result_ttl=5000)
    jobs.append(job)

time.sleep(1)

# poll job status
for j in jobs:
    if j.is_finished:
        print(f"job_id={j.get_id()}, result={j.result}")
    else:
        print(f"job_id={j.get_id()}, result=PENDING")
             

