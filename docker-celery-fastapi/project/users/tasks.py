import time
import requests
from celery import shared_task


@shared_task
def divide(x, y):
    time.sleep(2)
    return x / y


@shared_task
def get_page(url):

    # experiment with task within a task
    a = divide.delay(1, 2)
    while not a.ready():
        time.sleep(1)

    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    else:
        return "error"
