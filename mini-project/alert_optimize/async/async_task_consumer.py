# coding: utf-8

import time
import redis
import asyncio
import aiohttp


G_REDIS = redis.Redis(host='10.206.66.79', port=6379, db=0)


class Task:

    def __init__(self, check_offline_time=10, check_cms_time=10, ccca_domain='https://www.baidu.com'):
        self.check_offline_time = check_offline_time
        self.check_cms_time = check_cms_time
        self.ccca_domain = ccca_domain


async def check_offline(ck_time):
    status = G_REDIS.hget('offline', 'jason')
    # print(status)
    await asyncio.sleep(ck_time)


async def check_cms_status(ck_time):
    status = G_REDIS.hget('cms_status', 'jason')
    # print(status)
    await asyncio.sleep(ck_time)


async def check_ccca(session, url):
    async with session.get(url) as resp:
        if resp.status != 200:
            print(f'request fail with status: {resp.status}')
        else:
            data = await resp.text()
            # print(len(data))
            # print(data)


class AdminAlertConsumer:

    def __init__(self, task_num=100):
        self.curr_tasks = None
        self.task_num = task_num

    def get_tasks(self, number=100):
        url = 'http://10.206.66.73'
        return [Task(ccca_domain=url) for i in range(number)]

    def get_run_tasks(self, session):
        tasks_num = 100
        tasks = []
        for item in range(0, self.task_num, tasks_num):
            self.curr_tasks = self.get_tasks(tasks_num)
            for task in self.curr_tasks:
                tasks.append(check_offline(float(task.check_offline_time/1000)))
                tasks.append(check_cms_status(float(task.check_offline_time/1000)))
                tasks.append(check_ccca(session, task.ccca_domain))
        return tasks


async def main():
    print(f"Begin do tasks {time.strftime('%X')}")
    session = aiohttp.ClientSession()
    aac = AdminAlertConsumer(1000)
    tasks = aac.get_run_tasks(session)
    await asyncio.gather(*tasks)
    await session.close()
    print(f"After do tasks {time.strftime('%X')}")


def do_main():
    # asyncio.run(main(), debug=True)
    asyncio.run(main())
    # print('Another async start...')
    # asyncio.run(main())


if __name__ == '__main__':
    # asyncio.run(main())
    do_main()
