from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import random
from pprint import pprint

"""
import requests
import json
dag_to_trigger = 'ice_cream_sundae'
uri = 'http://localhost:8080/api/experimental/dags/{}/dag_runs'.format(ice_cream_sundae)
conf = {'cone': 'chocolate_waffle','topping': 'strawberry sauce', 'ice_cream_flavor': 'cheesecake'}
data = { 'conf': json.dumps(conf)}
res = requests.post(uri, json=data)
res.content
res.status_code
"""

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG('ice_cream_sundae', default_args=default_args, schedule_interval=None)

sundae_choices = {
    'cones': ['cup', 'waffle'],
    'toppings': ['rainbow sprinkles', 'chocolate sprinkles', 'm&ms', 'gummy bears', 'chocolate sauce',
                 'strawberry sauce', 'caramel sauce', 'marshmallow'],
    'ice_cream_flavors': ['vanilla', 'chocolate', 'strawberry', 'salted caramel', 'cotton candy'],
}


def choose_cone(ds, **kwargs):
    kwargs['ti'].xcom_push(key='topping', value=random.choice(sundae_choices['cones']))


choose_cone_op = PythonOperator(
    task_id='choose_cone_task',
    python_callable=choose_cone,
    provide_context=True,
    dag=dag
)


def choose_icecream_flavor(ds, **kwargs):
    kwargs['ti'].xcom_push(key='ice_cream_flavor', value=random.choice(sundae_choices['ice_cream_flavors']))


choose_icecream_flavor_op = PythonOperator(
    task_id='choose_icecream_flavor_task',
    provide_context=True,
    dag=dag,
    python_callable=choose_icecream_flavor,
)


def choose_toppings(ds, **kwargs):
    kwargs['ti'].xcom_push(key='toppings', value=random.choice(sundae_choices['toppings']))


choose_toppings_op = PythonOperator(
    task_id='choose_toppings_task',
    provide_context=True,
    dag=dag,
    python_callable=choose_toppings,
)


def make_icecream_sundae(ds, **kwargs):
    # Get the task instance
    ti = kwargs['ti']
    cone = ti.xcom_pull(key='cone', task_ids='choose_cone_task')
    icecream_flavor = ti.xcom_pull(key='ice_cream_flavor', task_ids='choose_icecream_flavor_task')
    topping = ti.xcom_pull(key='choose_toppings_task', task_ids='choose_toppings_task')
    print('Our sundae is complete!')
    pprint({'cone': cone, 'icecream_flavor': icecream_flavor, 'topping': topping})


make_icecream_sundae_op = PythonOperator(
    task_id='make_icecream_sundae_task',
    provide_context=True,
    dag=dag,
    python_callable=make_icecream_sundae,
)

choose_icecream_flavor_op.set_upstream(choose_cone_op)
choose_toppings_op.set_upstream(choose_icecream_flavor_op)
make_icecream_sundae_op.set_upstream(choose_toppings_op)
