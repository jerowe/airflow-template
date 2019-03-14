from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import random
from pprint import pprint
from icecream_sunday_dag_def import choose_icecream_flavor, choose_cone, choose_toppings, make_icecream_sundae, default_args

icecream_sundae_linear_dag = DAG('ice_cream_sundae_linear', default_args=default_args, schedule_interval=None)


def generate_choose_cone_op(dag, task_id):
    return PythonOperator(
        task_id='choose_cone_task_{}'.format(task_id),
        python_callable=choose_cone,
        provide_context=True,
        dag=dag
    )


def generate_choose_icecream_flavor_op(dag, task_id):
    return PythonOperator(
        task_id='choose_icecream_flavor_task_{}'.format(task_id),
        provide_context=True,
        dag=dag,
        python_callable=choose_icecream_flavor,
    )


def generate_choose_toppings_op(dag, task_id):
    return PythonOperator(
        task_id='choose_toppings_task_{}'.format(task_id),
        provide_context=True,
        dag=dag,
        python_callable=choose_toppings,
    )


def generate_make_icecream_sundae_op(dag, task_id):
    return PythonOperator(
        task_id='make_icecream_sundae_task_{}'.format(task_id),
        provide_context=True,
        dag=dag,
        python_callable=make_icecream_sundae,
    )


choose_cones_op_list = [generate_choose_cone_op(icecream_sundae_linear_dag, 1),
                        generate_choose_cone_op(icecream_sundae_linear_dag, 2)]
choose_flavors_op_list = [generate_choose_icecream_flavor_op(icecream_sundae_linear_dag, 1),
                          generate_choose_icecream_flavor_op(icecream_sundae_linear_dag, 2)]
choose_toppings_op_list = [generate_choose_toppings_op(icecream_sundae_linear_dag, 1),
                           generate_choose_toppings_op(icecream_sundae_linear_dag, 2)]

for index, choose_cone_OP in enumerate(choose_cones_op_list):
    choose_cone_OP.set_downstream(choose_flavors_op_list[index])
    choose_flavors_op_list[index].set_downstream(choose_toppings_op_list[index])
