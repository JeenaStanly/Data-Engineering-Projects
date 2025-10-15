import json
import boto3

# Initialize AWS clients outside the handler for reusability and performance
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users-2')

def lambda_handler(event, context):
    """
    Lambda entry point triggered by S3 file upload.
    Parses user data from the uploaded JSON file and stores it in DynamoDB.
    """
    status_code = 0
    response_body = ''

    try:
        # Extract bucket name and object key from the S3 event payload
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Retrieve the uploaded file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')

        # Parse JSON content into Python list of user dictionaries
        users = json.loads(file_content)
        print(f"Parsed Users: {users}")

        # Batch write user records to DynamoDB for efficiency
        with table.batch_writer() as batch:
            for user in users:
                batch.put_item(Item={
                    'id': user['id'],  # Unique identifier
                    'firstname': user['firstname'],
                    'lastname': user['lastname']
                })

        response_body = 'Successfully added users to DynamoDB.'
        status_code = 201

    except Exception as e:
        # Log error and return failure response
        print(f"Error processing file: {str(e)}")
        response_body = 'Failed to add users to DynamoDB.'
        status_code = 403

    # Return HTTP-style response for Lambda integrations
    return {
        'statusCode': status_code,
        'body': response_body
    }
