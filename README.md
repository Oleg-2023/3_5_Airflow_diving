# 3_5_Airflow_diving
- Вынести параметры для вызова API в airflow variables.
  
__variables:__  
{  
    "API_ACCESS_KEY": "0f9490384184e1654447b78adc6589e9",  
    "BASE_CURRENCY": "RUB",  
    "CURRENCY_SOURCE": "BTC",  
    "RESOURCE_API_URL": "http://api.exchangerate.host",  
    "conn_name": "conn1"  
}  

- Вынести подключение к БД в airflow connections.  
__connections:__  
{  
  "conn1": {  
    "conn_type": "postgres",  
    "description": "",  
    "login": "postgres",  
    "password": "password",  
    "host": "localhost",  
    "port": 5430,  
    "schema": "test",  
    "extra": "{}"  
  }  
}  

В модуль __functions.py__ добавлено чтение соответствующих переменных:  
conn_id = Variable.get("conn_name")  
API_URL = Variable.get("RESOURCE_API_URL")
SOURCE = Variable.get("CURRENCY_SOURCE")  
CURRENCY = Variable.get("BASE_CURRENCY")  
ACCESS_KEY = Variable.get("API_ACCESS_KEY")  
