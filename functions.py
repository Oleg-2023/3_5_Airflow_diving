import requests
from datetime import datetime
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

conn_id = Variable.get("conn_name")
API_URL = Variable.get("RESOURCE_API_URL")
SOURCE = Variable.get("CURRENCY_SOURCE")
CURRENCY = Variable.get("BASE_CURRENCY")
ACCESS_KEY = Variable.get("API_ACCESS_KEY")

def get_url():
    # Запрос к Web API
    url = API_URL+ '/live?access_key={}&'\
          'source={}&currencies={}'.format(ACCESS_KEY, SOURCE, CURRENCY)
    return requests.get(url)

def add_data_psql():
    hook = PostgresHook(postgres_conn_id=conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    try:
        response = get_url()
        data = response.json()
        get_date = datetime.utcfromtimestamp(data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        rate = data["quotes"][SOURCE+CURRENCY]
        sql = f'''
                INSERT INTO quotes (get_date, base_rate, target_rate, rate)
                VALUES ('{get_date}', '{CURRENCY}', '{SOURCE}', '{rate}');
        '''
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as error:
        conn.rollback()
        raise Exception(f'Ошибка добавления данных: {error}')
