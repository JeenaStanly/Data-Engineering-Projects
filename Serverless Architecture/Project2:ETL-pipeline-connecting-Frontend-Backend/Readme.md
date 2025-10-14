# 📄 Project Documentation: Serverless Web App with S3, API Gateway, Lambda, and DynamoDB

## 🧭 Overview

**Objective**: Build and deploy a fully serverless web application using AWS services. The frontend is hosted on S3, while backend logic is handled by Lambda functions triggered via API Gateway. Data is stored and retrieved from DynamoDB.

---

## 🏗️ Architecture Summary

```plaintext
[Static Website on S3] → [API Gateway] → [AWS Lambda] → [DynamoDB]
```

- **Frontend**: HTML/CSS/JS hosted on S3
- **API Gateway**: REST endpoints for GET and POST
- **Lambda**: Python functions for data access
- **DynamoDB**: NoSQL table for persistent storage

---

## 🔧 Step-by-Step Implementation

### **1. Hosting Static Website on S3**

- Created an S3 bucket (e.g., `my-web-app-bucket`)
- Enabled **Static Website Hosting** under bucket properties
- Uploaded `index.html`, `style.css`, and `app.js`
- Set bucket policy for public read access:
  ```json
  {
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-web-app-bucket/*"
  }
  ```

### **2. Configuring API Gateway**

- Created a **REST API** in API Gateway
- Defined two endpoints:
  - `GET /items` → fetch data from DynamoDB
  - `POST /items` → insert new data
- Enabled **CORS** for frontend integration
- Linked each method to its respective Lambda function

### **3. Creating Lambda Functions (Python)**

#### `get_items.py`
```python
import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Items')
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
```

#### `post_item.py`
```python
import boto3
import json

def lambda_handler(event, context):
    data = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Items')
    table.put_item(Item=data)
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Item added'})
    }
```

### **4. Setting Up DynamoDB**

- Created table `Items`
- **Partition Key**: `id` (String)
- Additional attributes: `name`, `description`, `timestamp`
- Enabled **on-demand capacity** for simplicity
- Verified CRUD operations via Lambda and API Gateway

---

## 📊 Monitoring & Security

- **IAM Roles**:
  - Lambda role with `dynamodb:PutItem`, `dynamodb:Scan`, `logs:*`
  - API Gateway execution role with `lambda:InvokeFunction`
- **CloudWatch Logs**:
  - Enabled for all Lambda functions
  - Used for debugging and performance tracking

---

## 📁 Deliverables

| Component            | Description                                 |
| -------------------- | ------------------------------------------- |
| S3 Bucket            | Hosts static frontend files                 |
| API Gateway          | Routes HTTP requests to Lambda functions    |
| Lambda Functions     | Python code for GET and POST operations     |
| DynamoDB Table       | Stores application data                     |
| Architecture Diagram | Visual flow of components                   |
| Documentation        | This file, suitable for recruiters or teams |

---

## ✨ Highlights

- Fully serverless architecture—no EC2 or manual provisioning
- Clean separation of frontend and backend logic
- Scalable and cost-efficient using AWS native services
- Demonstrates real-world integration of S3, API Gateway, Lambda, and DynamoDB

---

Would you like me to generate a matching architecture diagram or help format this into a Word document with headings and styles? I can also help you write a resume bullet or LinkedIn post summarizing this project.
