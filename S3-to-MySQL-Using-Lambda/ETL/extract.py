import json
import boto3
import pymysql
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Extract bucket and file details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"Bucket: {bucket}, Key: {key}")

    # Fetch file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8').strip()

    print(f"Data: {data}")

    rows = []
    for i, row in enumerate(data.split("\n")):
        if i == 0 or not row.strip():  # Skip header & empty rows
            continue
        values = row.split(",")
        if len(values) == 5:
            id_, name, age, email, city = values
            try:
                age = int(age.strip())  # Ensure age is a valid integer
            except ValueError:
                print(f"Skipping row due to invalid age format: {values}")
                continue
            rows.append((name.strip(), age, email.strip(), city.strip()))

    print("Parsed rows:", rows)

    # Connect to MySQL
    try:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            port=int(os.environ['DB_PORT']),
            password=os.environ['DB_PASSWORD'],
            db=os.environ['DB_NAME']
        )
        cursor = connection.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                email VARCHAR(255),
                city VARCHAR(255)
            )
        """)

        # Insert data into MySQL
        if rows:
            cursor.executemany("""
                INSERT INTO customer (name, age, email, city)
                VALUES (%s, %s, %s, %s)
            """, rows)
            connection.commit()
            print(f"Inserted {cursor.rowcount} rows into the database.")

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    
    finally:
        cursor.close()
        connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps("Data successfully Inserted")
    }
