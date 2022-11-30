
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from rekdat_script.hello_world import hello_world

with DAG(
    dag_id="test_dags",
    schedule_interval="@hourly",
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag:

    def print_context(ds, **kwargs):
        print(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = PythonOperator(
        task_id='print_the_context',
        python_callable=hello_world,
    )

    run_this