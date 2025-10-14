## 📄 1. Serverless Architecture Documentation

### **Project Title**  
**Serverless Data Processing Pipeline with AWS Lambda, S3, and DynamoDB**

### **Objective**  
Design and implement a fully serverless pipeline that ingests data via S3, processes it using AWS Lambda, and stores transformed results in DynamoDB for querying and downstream use.

### **Architecture Overview**

```plaintext
[S3 Bucket] → (Trigger) → [AWS Lambda] → [DynamoDB Table]
```

- **S3 Bucket**: Stores incoming `.csv` or `.json` files.
- **Lambda Function**: Triggered on file upload. Parses and transforms data using Python.
- **DynamoDB**: Stores processed records with partition/sort keys for efficient querying.

### **Workflow Steps**

1. **Data Ingestion**  
   - Files uploaded to `s3://your-bucket-name/input/`  
   - S3 event triggers Lambda execution

2. **Data Processing**  
   - Lambda reads file from S3  
   - Parses content using Python (e.g., `csv`, `json`, `boto3`)  
   - Applies transformations (e.g., filtering, enrichment, normalization)

3. **Data Storage**  
   - Transformed records written to DynamoDB  
   - Uses `PutItem` or `BatchWriteItem` for efficiency

4. **Monitoring & Logging**  
   - CloudWatch logs for Lambda execution  
   - Optional: CloudWatch alarms for failures or throttling

---

## 🧠 2. Lambda Function Documentation

### **Function Name**  
`process_s3_file_to_dynamodb`

### **Trigger**  
- **Event Source**: S3  
- **Event Type**: `ObjectCreated:*`  
- **Bucket**: `your-bucket-name`

### **Runtime & Language**  
- Python 3.9  
- AWS Lambda

### **IAM Role Permissions**  
- `s3:GetObject`  
- `dynamodb:PutItem`  
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

### **Code Summary**
- Use the code in the python file
---

## 🗃️ 3. DynamoDB Table Schema

### **Table Name**  
`ProcessedData`

### **Primary Key Structure**  
- **Partition Key**: `record_id` (String)  
- **Sort Key** *(optional)*: `timestamp` (String or Number)

### **Attributes**  
| Attribute     | Type   | Description                       |
| ------------- | ------ | --------------------------------- |
| `record_id`   | String | Unique identifier for each record |
| `timestamp`   | String | Time of processing or ingestion   |
| `data_field1` | String | Transformed field from input      |
| `data_field2` | Number | Calculated or normalized value    |

### **Indexes (Optional)**  
- **GSI**: `status-index` on `status` attribute for querying by processing status
