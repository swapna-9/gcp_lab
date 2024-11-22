from airflow import DAG
from scipy import stats
from airflow.operators.python import PythonOperator
from datetime import datetime
import numpy as np
from airflow import configuration as conf
from google.cloud import storage
import io
import os
import pandas as pd
from google.cloud import storage
import logging

from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator
from datetime import timedelta,datetime
from airflow.utils.dates import days_ago
from airflow.utils.email import send_email_smtp
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime
from train_and_save_model import main # Import the training function
 
# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2024, 11, 21),
    'retries': 1,
}
 
# Define the DAG
with DAG(
    default_args=default_args,
    description='A DAG to run training.py and send email notifications',
    schedule_interval=None,  # Run manually or on trigger
) as dag:
 
    # Task 1: Execute the training job
    run_training = PythonOperator(
        task_id='run_training',
        python_callable=main
    )
 
    # Task 2: Send an email notification
    send_email = EmailOperator(
        task_id='send_email',
        to='anirudhak881@gmail.com',  # Replace with your email
        subject='Training Job Completed',
        html_content='<p>The training job has been successfully completed!</p>'
        conn_id='gmail_smtp'
    )
 
    # Define task dependencies
    run_training >> send_email
