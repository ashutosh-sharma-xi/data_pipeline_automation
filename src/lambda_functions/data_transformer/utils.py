import logging
import boto3
from botocore.exceptions import ClientError
import sys
import psycopg2  # Replace with your database library
import json 


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_db_secret():
    secret_name = "db-secret-store"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret


def db_connection(secrets ):
    hostname = secrets["host"] 
    username = secrets["username"]
    password = secrets["password"]
    database = secrets["dbInstanceIdentifier"]
    port = 5432  

    # Connect to RDS database
    try:
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        cursor = conn.cursor()
        return conn , cursor

    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Error in connection to rds: {str(e)}"}
