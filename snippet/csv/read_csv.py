import csv
import pymysql


def main():
    conn = pymysql.connect(
        host='', port=3306,
        user='admin', passwd='', db='analysis', charset='utf8'
    )
    cursor = conn.cursor()
    alldata = {}
    with open('internet_security.csv') as fp:
        csv_reader = csv.reader(fp, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                if not row[1].startswith('10.') and not row[1].startswith('192.') and not row[1].startswith('172.'):
                    print(row[1])
                    continue
