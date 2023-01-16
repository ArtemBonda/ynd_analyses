# Документация проведенной работы

* [Визуализация на платформе Tableau](https://public.tableau.com/views/dash_visits_wv/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link)

* `zen.py`- скрипт запускающий подключение к БД и формирование датафрейма
* `dash_visits.csv` - формируемый датафрейм
* `Yandex.Дзен взаимодействие с карточками.pdf` - презентация анализа данных
* `input_pipeline.py` - скрипт подключающийся к БД Яндекса, сохраняющий на сервере выборку в файле `data_visits_raw.csv`
* `ouput_pipeline.py` - скрипт дописывающий обновленные агрегированные данные из сохраненного датафрейма
## Памятка по шагам запуска скрипта и пайплайна

1. Скопировать на сервер скрипт
```bash
scp zen.py input_pipeline.py ouput_pipeline.py test_admin@<public:ip>:
```

2. Подключится к серверу Yandex.Cloud или Docker с поднятым контейнером Linux
```bash
ssh test_admin@<public:ip>
```
Обновить python
```bash
sudo apt install python3.10-venv
```

3. Установить PostgreSQl 
```linux
sudo apt update
sudo apt upgrade
sudo apt install postgresql postgresql-contrib
sudo apt-get install python3-psycopg2
```
4. Запускаем Postgres под пользователем postgres
```ubuntu
sudo su postgres
```
5. Создание БД в которой, будут храниться агрегированные данные
```bash
createdb zen_db --encoding=utf-8
```
6. Подключение к БД 
```bash
psql -d zen_db
```
Команды для работы с Postgres
- `\?` - справочная информация
- `\dt` - просмотр таблиц в БД
- `\h` - список всех команд
- `exit` - выход из БД
Если пользователь уже задан подключаться к БД
```bash
psql -d zen_db -U app
```
7. Создание пользователя и предоставление прав доступа
```postgres
CREATE USER app WITH ENCRYPTED PASSWORD 'pass';

GRANT ALL PRIVILEGES ON DATABASE zen_db TO app;
```
8. Создание таблицы для хранения данных
```bash
CREATE TABLE dash_visits
(  record_id SERIAL PRIMARY KEY,
   item_topic VARCHAR(128),
   source_topic VARCHAR(128), 
   age_segment VARCHAR(128),
   dt TIMESTAMP,
   visits INT
);
```
ОБЯЗАТЕЛЬНО добавить ПРАВА пользователю, иначе будет ошибки при взаимодействии c таблицей
```
GRANT ALL PRIVILEGES ON TABLE dash_visits TO app;
GRANT USAGE, SELECT ON SEQUENCE dash_visits_record_id_seq TO app;
```
9. Установка зависимостей для Python
```bash
sudo apt install python3-pip
pip3 install sqlalchemy
pip3 install dash
pip3 install pandas
pip3 install freeze
```
Посмотреть на все установленные модули
```
python3 -m pip freeze --all
```
Запишу все в файл для хранения зависимостей, в файле `requirements.txt` будет храниться описание виртуального окружения
```
python3 -m pip freeze > requirements.txt
```
Необязательные шаги, для ознакомления в будущем
- Создание нового окружения
```bash
python3 -m venv new_venv_pipeline
```
- Активация окружения
```bash
source ./new_venv_pipeline/bin/activate

python3 -m pip list
```
- Установка окружения из файла requirements.txt
```bash
python3 -m pip install -r ./requirements.txt
```
10. Запустить скрипт на сервере
```bash
python3 input_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00'
```
Результатом будет файл с сырыми данными `data_visits_raw.csv`  
- Скрипт ниже делает:
```bash
python3 output_pipeline.py --start_dt='2019-09-24 18:00:00' --end_dt='2019-09-24 19:00:00'
```
Результат: заполнение БД на сервере  
- Скрипт ниже делает:
```bash
python3 zen.py
```
Результат: файл с выгруженными данными из БД для построения Дашборда

## задача на будущее
- Добавить комментарии в код
- Узнать как передать в переменные окружения данных от БД, для сокрытия информации
- Как установить для переменных `start_dt` и `end_dt` начало и конец прошедшего дня, убрать захордкоженные даты
- Сделать обработку флагов командной строки
- Переделать zen.py под пайпланы на Dash
- разобраться с файлом зависимостей requrements.txt
- Запаковать в архив, передавать на сервер архивом с последующей разархивацией на месте, и запуском скриптов
- запланировать выполнение всех скриптов в планировщике, пример:
    - запуск планировщика 
   ```bash
    crontab -e
    ```
   - записать задачу: Частота обновления данных: один раз в сутки, в полночь по UTC
   ```bash
   00 00 * * * -u -W python /home/test_admin/zen_bd.py >> /home/test_admin/logs/zen.log 2&>1
   ```

## Полезные ссылки
- [Статья по созданию виртуального окружения](https://www.andreyolegovich.ru/code/python/ve/virtualenv/freeze.php)
- [Статья SQLAlchemy + Flask](https://hamza-senhajirhazi.medium.com/how-to-handle-schema-multi-tennancy-with-python-flask-sqlalchemy-postgres-7000dda10749)
- [Документация по SQLAlchemy](https://www.sqlalchemy.org/)
- [Руководство на английском, работа с SQLAlchemy](https://overiq.com/sqlalchemy-101/intro-to-sqlalchemy/)
- [Адаптированная статьи по работе SQLAlcemy](https://pythonru.com/biblioteki/vvedenie-v-sqlalchemy)
- [Документация по библиотеке D3js](https://d3js.org/)
- [Документация по Dash](https://dash.plotly.com/)

