# coding: utf-8

import time
import json
import pika
import pymysql
import multiprocessing


def init_alert_db():
    G_CONN = pymysql.connect(
        host='10.206.67.81', port=3306, user='root',
        passwd='Trend#1..', db='alert_opt'
    )
    cursor = G_CONN.cursor()
    try:
        for i in range(50000):
            sql = 'insert into alert(`update_time`) values(0)'
            cursor.execute(sql)
        G_CONN.commit()
    except Exception as e:
        print(e)
        G_CONN.rollback()
    cursor.close()


def get_tasks(tnum):
    G_CONN = pymysql.connect(
        host='10.206.67.81', port=3306, user='root',
        passwd='Trend#1..', db='alert_opt'
    )
    cursor = G_CONN.cursor()
    sql_f = 'select * from alert where update_time < {} order by id asc limit {}'
    update_sql_f = 'update alert set update_time={} where id in ({})'
    while True:
        ts_now = int(time.time())
        sql = sql_f.format(ts_now, tnum)
        try:
            cursor.execute(sql)
            datas = cursor.fetchall()
            # print(datas)
            # G_CONN.commit()
            if datas[-1][0] == 50000:
                all_done = int(time.time())
                with open('/tmp/alert_mark.txt', 'a') as fp:
                    fp.write('Explore done for all records: {}\n'.format(all_done))
            ids = [str(item[0]) for item in datas]
            update_sql = update_sql_f.format(ts_now+300, ','.join(ids))
            # print(update_sql)
            cursor.execute(update_sql)
            G_CONN.commit()
        except Exception as e:
            print(e)
            G_CONN.rollback()
            time.sleep(10)
    cursor.close()


def main(pnum):
    p_list = []
    for i in range(5):
        p = multiprocessing.Process(target=get_tasks, args=(10,))
        p_list.append(p)
    for item in p_list:
        item.start()


def generate_task_mq():
    cred = pika.PlainCredentials('json', '111111')
    conn = pika.BlockingConnection(
        pika.ConnectionParameters('10.206.67.81', 5672, 'vhost_json', cred)
    )
    channel = conn.channel()
    channel.queue_declare(queue='balance')

    G_CONN = pymysql.connect(
        host='10.206.67.81', port=3306, user='root',
        passwd='Trend#1..', db='alert_opt'
    )
    cursor = G_CONN.cursor()
    sql_f = 'select * from alert where update_time < {} order by id asc'
    ts_now = int(time.time())
    sql = sql_f.format(ts_now)
    cursor.execute(sql)
    data = cursor.fetchall()
    for item in data:
        channel.basic_publish(
            exchange='', routing_key='balance', body=json.dumps(item)
        )
    G_CONN.commit()
    cursor.close()
    G_CONN.close()
    conn.close()


def get_tasks_mq():
    cred = pika.PlainCredentials('json', '111111')
    conn = pika.BlockingConnection(
        pika.ConnectionParameters('10.206.67.81', 5672, 'vhost_json', cred)
    )
    channel = conn.channel()
    channel.queue_declare(queue='balance')

    def on_message(channel, method_frame, header_frame, body):
        data = json.loads(body)
        if data[0] == 50000:
            print(data)
            all_done = int(time.time())
            with open('/tmp/alert_mark.txt', 'a') as fp:
                fp.write('Explore done for all records: {}\n'.format(all_done))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    channel.basic_consume('balance', on_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    conn.close()


def main_mq(pnum):
    generate_task_mq()
    # get_tasks_mq()
    p_list = []
    for i in range(5):
        p = multiprocessing.Process(target=get_tasks_mq)
        p_list.append(p)
    for item in p_list:
        item.start()


if __name__ == '__main__':
    # init_alert_db()
    print(int(time.time()))
    # get_tasks(10)
    main(5)
    # main_mq(5)
