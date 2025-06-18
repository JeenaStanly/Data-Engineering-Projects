import json
import pymysql
import boto3

# Database connection details
DB_HOST = "your-mysql-host"
DB_USER = "your-username"
DB_PASSWORD = "your-password"
DB_NAME = "your-database"

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Get bucket and file details from event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Fetch file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    
    # Process file (assuming CSV format)
    rows = file_content.split("\n")
    
    # Connect to MySQL
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS your_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            column1 VARCHAR(255),
            column2 VARCHAR(255)
        )
    """)
    
    # Insert data into MySQL
    for row in rows:
        values = row.split(",")  # Adjust parsing based on file format
        cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (values[0], values[1]))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return {"statusCode": 200, "body": json.dumps("Data inserted successfully")}
