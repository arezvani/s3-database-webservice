import requests
import psycopg2
from psycopg2 import Error, pool
import config
import boto3
from botocore.exceptions import NoCredentialsError
import mimetypes
from datetime import datetime
import json

date_format = "%Y-%m-%dT%H:%M:%S.%fZ" 
s3_public_base_url = f"{config.S3_ENDPOINT}/v1/AUTH_{config.PROJECT_ID}/persons"

def init():
    try:
        # connect to db
        db_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn= 5,
            maxconn = 100,
            host = config.db_host,
            port = config.db_port,
            database = config.db_database,
            user = config.db_username,
            password = config.db_password
        )   

        # create session for s3
        session = boto3.session.Session()

        return db_pool, session

    except Error as e: ...
        # print('Can not connect to database: {}'.format(e))
    
    except Exception as e: ...
        # print('Error: {}'.format(e))

def get_data():
    r = requests.get(config.api_url)
    
    if r.ok:
        data = r.json()
        return data['results'][0]
    else:
        return None

def upload_file(session, remote_url, bucket, file_name):
    s3 = session.client(
        service_name='s3',
        aws_access_key_id=config.ACCESS_KEY_ID,
        aws_secret_access_key=config.SECRET_ACCESS_KEY,
        endpoint_url=config.S3_ENDPOINT,
    )
    
    try:
        imageResponse = requests.get(remote_url, stream=True).raw
        content_type = imageResponse.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        s3.upload_fileobj(imageResponse, bucket, file_name + extension)
        # print("Upload Successful")
        return True
    except FileNotFoundError:
        # print("The file was not found")
        return False
    except NoCredentialsError:
        # print("Credentials not available")
        return False

def db_insert(db_pool, data):
    try:
        prepared_data = {
            "uuid": data['login']['uuid'],
            "first_name": data['name']['first'],
            "last_name": data['name']['last'],
            "gender": data['gender'],
            "location": json.dumps(data['location']),
            "username": data['login']['username'],
            "password": data['login']['password'],
            "picture": f"{s3_public_base_url}/{data['login']['uuid']}/image.jpg",
            "phone": data['phone'],
            "age": data['dob']['age'],
            "register_date": datetime.strptime(data['registered']['date'], date_format),
            "email": data['email'],
        }

        db_conn = db_pool.getconn()
        if db_conn:
            cursor = db_conn.cursor()
            
            # insert to auth table
            sql = 'INSERT INTO persons_auth VALUES(%s,%s,%s,%s);'

            values = (
                prepared_data['username'],
                prepared_data['password'],
                prepared_data['email'],
                prepared_data['uuid'],
            )
            cursor.execute(sql, values)

            # insert to information table
            sql = 'INSERT INTO persons_information VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

            values = (
                prepared_data['uuid'],
                prepared_data['first_name'],
                prepared_data['last_name'],
                prepared_data['gender'],
                prepared_data['location'],
                prepared_data['picture'],
                prepared_data['phone'],
                prepared_data['age'],
                prepared_data['register_date'],
                prepared_data['email'],
            )
            cursor.execute(sql, values)

            db_conn.commit()         

    except Exception as e: ...
        # print('DB Commit: False, DB Error: {error}'.format(error=e))

    finally:
        #closing database connection.
        if db_conn:
            cursor.close()
            db_pool.putconn(db_conn)

if __name__ == "__main__":
    db_pool, session = init()
    while 1:
        data = get_data()
        if data:
            uploaded = upload_file(session=session, remote_url=data['picture']['large'], bucket='persons', file_name=f"{data['login']['uuid']}/image")
            if uploaded:
                db_insert(db_pool=db_pool, data=data)