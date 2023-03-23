import os
import psycopg2
import boto3

conn = psycopg2.connect(
        host="some_ip_or_host",
        port=5432,
        database="the_database_name",
        user="the_user",
        password="the_password"
        )

# setup client of S3 Bucket and AWS private key's. In this example, these must be setup as eviroment variables
s3 = boto3.client('s3',
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

device_id = input("Enter the device ID: ")

# Search for device_id in a device table. Change query as you need
cur = conn.cursor()
cur.execute(f"SELECT * FROM device WHERE name = '{device_id}'")
device = cur.fetchone()
cur.close()

if device:
        s3.put_object(Body=str(device), Bucket='the_bucket_name', Key=f'/{device_id}.txt')
        print(f"Device {device_id} uploaded to S3 successfully.")
else:
        print(f"Device {device_id} not found in the database.")
