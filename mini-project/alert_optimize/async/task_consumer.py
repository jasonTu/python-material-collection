# coding: utf-8
import time
import redis
import requests


G_REDIS = redis.Redis(host='10.206.66.79', port=6379, db=0)


class Task:

    def __init__(self, check_offline_time=10, check_cms_time=10, ccca_domain='https://www.baidu.com'):
        self.check_offline_time = check_offline_time
        self.check_cms_time = check_cms_time
        self.ccca_domain = ccca_domain


def check_offline(ck_time):
    status = G_REDIS.hget('offline', 'jason')
    time.sleep(ck_time)


def check_cms_status(ck_time):
    status = G_REDIS.hget('cms_status', 'jason')
    time.sleep(ck_time)


class AdminAlertConsumer:

    def __init__(self, task_num=100):
        self.curr_tasks = None
        self.task_num = task_num

    def get_tasks(self, number=100):
        return [Task() for i in range(number)]

    def run(self):
        print(f"Begin do tasks {time.strftime('%X')}")
        tasks_num = 100
        for item in range(0, self.task_num, tasks_num):
            self.curr_tasks = self.get_tasks(tasks_num)
            for task in self.curr_tasks:
                check_offline(float(task.check_offline_time/1000))
                check_cms_status(float(task.check_cms_time/1000))
                resp = requests.get(task.ccca_domain)
                # print(len(resp.content))
        print(f"After do tasks {time.strftime('%X')}")


def main():
    aac = AdminAlertConsumer(1000)
    aac.run()


if __name__ == '__main__':
    main()
