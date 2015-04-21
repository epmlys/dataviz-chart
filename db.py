"""Data loader and helpers."""

import csv
import sqlite3

FILE_NAME = 'uploads/history.csv'

connection = sqlite3.connect(':memory:')
cursor = connection.cursor()


def load_data_from_csv(file_name):
    cursor.execute(
        'CREATE TABLE build_history (created_at TEXT, status TEXT, duration REAL);')

    db_values = []
    with open(file_name, 'rb') as fh:
        reader = csv.DictReader(fh)
        for line in reader:
            datetime = line['created_at'].split()
            datetime = '{} {}'.format(datetime[0], datetime[1])  # eliminate UTC
            db_values.append((datetime, line['summary_status'], line['duration']))

    cursor.executemany(
        '''INSERT INTO build_history (created_at, status, duration)
           VALUES (?, ?, ?);''',
        db_values)
    connection.commit()


def get_statuses_by_day():
    res = cursor.execute(
        '''SELECT date(created_at), count(status) FROM build_history WHERE
           status="passed" GROUP BY date(created_at);''')
    statuses_by_day = dict(res.fetchall())
    res = cursor.execute(
        '''SELECT date(created_at), count(status) FROM build_history WHERE
           status="failed" GROUP BY date(created_at);''')
    failed_by_day = dict(res.fetchall())

    # add passed/failed for each day
    for key, value in statuses_by_day.items():
        statuses_by_day[key] = {'passed': value,
                                'failed': failed_by_day.get(key, 0)}
    return statuses_by_day


def get_duration_by_time():
    res = cursor.execute(
        '''SELECT time(created_at), duration FROM build_history GROUP BY time(created_at);''')
    return dict(res.fetchall())


load_data_from_csv(FILE_NAME)
build_history = get_statuses_by_day()
time_duration = get_duration_by_time()
