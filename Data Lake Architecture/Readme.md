# End-to-End Data Pipeline with Google Sheets, Airflow, AWS S3, Glue, Athena, and Power BI

## 📌 Objective
This project demonstrates how to build a **scalable, automated data pipeline** that extracts data from **Google Sheets**, processes it using **AWS services**, and delivers curated insights for visualization in **Power BI**.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Google Sheet Data] --> B{Service Account & API Access}
    B --> C[Airflow DAG 1: Data Ingestion & Transformation]
    C --> D[Python Operator: Fetch Data from Google Sheet]
    D --> E[Upload Raw Data to S3://bucket/bronze/raw]
    E --> F[Glue Operator: Trigger Glue Job]
    F --> G[AWS Glue Job: Transform Data & SCD Type 2 Handling]
    G --> H[Create Parquet File in S3://bucket/silver/processed]
    H --> I[AWS Glue Crawler & Catalog]
    I --> J[Athena Operator: Trigger SQL Query for Analysis]
    J --> K[Save Query Result to S3://bucket/gold/curated]
    K --> L[Power BI: Visualization]

