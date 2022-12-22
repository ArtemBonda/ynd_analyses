#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
import getopt
from sqlalchemy import create_engine
import sys

start_dt = '2019-09-24 18:00:00'
end_dt = '2019-09-24 19:00:00'

db_config = {
    'user': 'app',
    'pwd': 'pass',
    'host': 'localhost',
    'port': 5432,
    'db': 'zen_db'
}

conn_str = (f"postgresql://{db_config['user']}:{db_config['pwd']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['db']}")


def get_connection():
    return create_engine(conn_str)


if __name__ == '__main__':
    data_raw = pd.read_csv('data_visits_raw.csv')

    columns_str = ['event', 'age_segment', 'item_topic', 'source_topic', 'source_type']
    columns_numeric = ['item_id', 'source_id', 'user_id']

    for column in columns_str:
        data_raw[column] = data_raw[column].astype(str)
    for column in columns_numeric:
        data_raw[column] = pd.to_numeric(data_raw[column], errors='coerce')
    data_raw['dt'] = pd.to_datetime(data_raw['dt']).dt.round('min')

    dash_visits = (data_raw.groupby(['item_topic', 'source_topic', 'age_segment', 'dt'])
                   .agg({'event': 'count'})
                   .rename(columns={'event': 'visits'})
                   .fillna(0)
                   .reset_index())

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

    tables = {'dash_visits': dash_visits}
    for table_name, table_data in tables.items():
        query = '''
                     DELETE FROM {} WHERE dt BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
                   '''.format(table_name, start_dt, end_dt)
        conn.execute(query)
        table_data.to_sql(name=table_name, con=conn, if_exists='append', index=False)
