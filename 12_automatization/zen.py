#!/usr/bin/python
# -*- python: utf-8 -*-

import pandas as pd
import sys
from sqlalchemy import create_engine

db_config = {
    'user': 'praktikum_student',
    'pwd': 'Sdf4$2;d-d30pp',
    'host': 'rc1b-wcoijxj3yxfsf3fs.mdb.yandexcloud.net',
    'port': 6432,
    'db': 'data-analyst-zen-project-db'
}

conn_str = (f"postgresql://{db_config['user']}:{db_config['pwd']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['db']}")


def get_connection():
    return create_engine(conn_str)


if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f'Connection to the {db_config["host"]} for user {db_config["user"]} created successfully')
    except Exception as ex:
        print('Error: ', ex)
        sys.exit(2)

    query = '''
            SELECT * FROM dash_visits
            '''

    output = pd.io.sql.read_sql(query, con=engine)

    # сохраняем файл
    output.to_csv('dash_visits.csv', index=False)
    df = pd.read_csv('dash_visits.csv')
    print(df.head())
