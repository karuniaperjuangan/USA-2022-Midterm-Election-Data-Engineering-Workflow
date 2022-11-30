from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from rekdat_script.w01_extract_json_data import extract_json_data
from rekdat_script.w02a_scrape_popularity import scrape_candidates_popularity
from rekdat_script.w02b_scrape_twitter import scrape_twitter
from rekdat_script.w03_sentiment_analysis import sentiment_analysis_tweet
from rekdat_script.w04_merge_all_data import merge_data
from rekdat_script.w05_xgboost_training import train_xgboost_model


with DAG(
    dag_id="rekdat1_update_election_count",
    schedule_interval="0 */6 * * *", # every 6 hours
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag:


    run_this = PythonOperator(
        task_id='extract_json_data',
        python_callable=extract_json_data,
    )

    run_this
    
with DAG(
    dag_id="rekdat2_scraping_google_popularity",
    #daily
    schedule_interval="0 0 * * *",
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag2:
    task_scraping_google_popularity = PythonOperator(
        task_id='scraping_google_popularity_task',
        python_callable=scrape_candidates_popularity,
    )
    
    task_scraping_google_popularity
    
with DAG(
    dag_id="rekdat3_sentiment_analysis_tweet",
    #daily
    schedule_interval="0 0 * * *",
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag3:
    task_scrape_tweet = PythonOperator(
        task_id='scrape_tweet_task',
        python_callable=sentiment_analysis_tweet,
    )    
    task_sentiment_analysis_tweet = PythonOperator(
        task_id='sentiment_analysis_tweet_task',
        python_callable=scrape_twitter,
    )
    
    task_scrape_tweet >> task_sentiment_analysis_tweet
    
with DAG(
    dag_id="rekdat4_merge_all_data",
    schedule_interval="0 8 * * *", #jam 8 pagi
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag4:
    task_merge_all_data = PythonOperator(
        task_id='merge_all_data_task',
        python_callable=merge_data,
    )
    
    task_merge_all_data
    
with DAG(
    dag_id="rekdat5_xgboost_training",
    schedule_interval="0 12 * * *", #jam 12 siang
    start_date=datetime(2022, 11, 30),
    catchup=False,
) as dag5:
    task_xgboost_training = PythonOperator(
        task_id='xgboost_training_task',
        python_callable=train_xgboost_model,
    )
    
    task_xgboost_training