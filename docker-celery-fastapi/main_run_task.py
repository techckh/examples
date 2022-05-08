import time
from main import app
from project.users.tasks import divide, get_page
from celery.result import AsyncResult


if __name__ == '__main__':
    print('starting')

    print('creating task...')
    tasks = list()
    res = divide.delay(1, 2)
    tasks.append(res)

    print('creating task...')
    res = divide.delay(1, 2)
    tasks.append(res)

    print('creating task...')
    res = divide.delay(1, 2)
    tasks.append(res)

    print('creating task...')
    res = get_page.delay('https://www.twitter.com/')
    tasks.append(res)

    pending = tasks
    while True:
        new_pending = list()
        for res in pending:
            if res.ready():
                print('ready, task id, %s, %s' % (res.task_id, res.get()))
            else:
                new_pending.append(res)
        if not new_pending:
            print('all tasks completed')
            break
        print('sleeping 1')
        time.sleep(1)
        pending = new_pending
