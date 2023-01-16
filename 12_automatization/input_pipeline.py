#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from dotenv import load_dotenv, find_dotenv
import getopt
from sqlalchemy import create_engine
import pandas as pd

start_dt = '2019-09-24 18:00:00'
end_dt = '2019-09-24 19:00:00'

load_dotenv(find_dotenv())

# Конфигурация БД
user = os.getenv('USER')
pwd = os.getenv('PWD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db = os.getenv('DB')

conn_str = ("postgresql://{}:{}@{}:{}/{}"\
    .format(user, pwd, host, port, db))


def get_connection():
    return create_engine(conn_str)


if __name__ == '__main__':
    unix_opt = 's:e:'
    gnu_opt = ['start_dt=', 'end_dt=']

    full_arguments = sys.argv
    arguments_lst = full_arguments[1:]

    try:
        arguments, values = getopt.getopt(arguments_lst, unix_opt, gnu_opt)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ('-s', '--start_dt'):
            start_dt = current_value
        elif current_argument in ('-e', '--end_dt'):
            end_dt = current_value

    try:
        conn = get_connection()
        print(f'Connection to the {host} for user {user} created successfully')
    except Exception as ex:
        print('Error: ', ex)
        sys.exit(2)

    query = ''' SELECT
                        event_id,
                        age_segment,
                        event,
                        item_id,
                        item_topic,
                        item_type,
                        source_id,
                        source_topic,
                        source_type,
                        TO_TIMESTAMP(ts/1000) AT TIME ZONE 'Etc/UTC' as dt,
                        user_id
                FROM log_raw
                WHERE TO_TIMESTAMP(ts/1000) AT TIME ZONE 'Etc/UTC'  BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
           '''.format(start_dt, end_dt)

    data_raw = pd.read_sql_query(query, con=conn, index_col='event_id')

    data_raw.to_csv('data_visits_raw.csv', index=False)
