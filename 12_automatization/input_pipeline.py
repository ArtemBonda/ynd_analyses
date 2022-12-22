#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
from sqlalchemy import create_engine
import pandas as pd

start_dt = '2019-09-24 18:00:00'
end_dt = '2019-09-24 19:00:00'

db_config = {'user': 'praktikum_student',
             'pwd': 'Sdf4$2;d-d30pp',
             'host': 'rc1b-wcoijxj3yxfsf3fs.mdb.yandexcloud.net',
             'port': 6432,
             'db': 'data-analyst-zen-project-db'}

conn_str = (f"postgresql://{db_config['user']}:{db_config['pwd']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['db']}")


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
        print(f'Connection to the {db_config["host"]} for user {db_config["user"]} created successfully')
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
