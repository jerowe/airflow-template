from airflow import DAG
from icecream_sunday_dag_def import default_args
from icecream_sundae_linear_dag_def import generate_choose_cone_op, generate_choose_toppings_op, \
    generate_choose_icecream_flavor_op, generate_make_icecream_sundae_op

icecream_sundae_gather_dag = DAG('ice_cream_sundae_gather_dag', default_args=default_args, schedule_interval=None)

choose_cone_op = generate_choose_cone_op(icecream_sundae_gather_dag, 1)
choose_icecream_flavor_op = generate_choose_icecream_flavor_op(icecream_sundae_gather_dag, 1)
choose_toppings_op = generate_choose_toppings_op(icecream_sundae_gather_dag, 1)
make_icecream_sundae_op = generate_make_icecream_sundae_op(icecream_sundae_gather_dag, 1)

make_icecream_sundae_op.set_upstream([choose_cone_op, choose_icecream_flavor_op, choose_toppings_op])
