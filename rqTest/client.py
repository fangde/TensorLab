from redis import Redis
from rq import Queue
from rqtest import count_words_at_url
import time

c=Redis()

import requests
from rq.decorators import  job






q=Queue(connection=c)

print q

j=q.enqueue(count_words_at_url,'http://nvie.com')

time.sleep(3)
j.result

print j.result