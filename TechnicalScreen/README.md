# TechnicalScreen - Technical Assessment Project

A comprehensive technical assessment covering data engineering, system design, and MLOps deployment for a delivery date prediction system.

## Project Overview

This project demonstrates end-to-end technical capabilities across three key areas:
1. **Data Engineering** - Processing Elasticsearch logs and feature engineering
2. **System Design** - Real-time data pipeline architecture on AWS
3. **MLOps & Deployment** - Production deployment and monitoring strategies

## Project Structure

```
TechnicalScreen/
├── README.md                           # This file - Project overview and index
├── sample_sessions.json                # Sample Elasticsearch clickstream data
├── Task 1/                             # Data Engineering Solution
│   ├── README.md                       # Task 1 documentation
│   ├── task_1_data_engineering.py      # Main data processing implementation
│   └── requirements.txt                # Python dependencies
├── Task 2/                             # System Design Solution
│   └── task_2_system_design.md         # Real-time pipeline architecture
└── Task 3/                             # MLOps & Deployment Solution
    └── task_3_mlops_deployment.md      # Production deployment strategy
```

## Task Descriptions

### Task 1: Data Engineering Solution
**Goal**: Process Elasticsearch JSON logs and generate model-ready features for delivery date prediction.

**Key Features**:
- Timestamp extraction from `createdDateTime` field
- Feature generation: `day_of_year`, `day_of_week`, `hour_of_day`
- Optimized for both batch training and real-time inference
- Handles large datasets efficiently

**Technologies**: Python, Pandas, JSON processing

**Files**:
- [`Task 1/task_1_data_engineering.py`](Task%201/task_1_data_engineering.py) - Main implementation
- [`Task 1/README.md`](Task%201/README.md) - Detailed documentation
- [`Task 1/requirements.txt`](Task%201/requirements.txt) - Dependencies

### Task 2: System Design - Real-Time Data Pipeline
**Goal**: Design a robust, low-latency AWS-based data pipeline for real-time clickstream processing.

**Key Features**:
- Sub-100ms end-to-end latency
- Real-time clickstream ingestion from Elasticsearch
- Feature enrichment and ML model integration
- Comprehensive monitoring and failure handling

**Technologies**: AWS Kinesis, Lambda, DynamoDB, SageMaker, CloudWatch

**Files**:
- [`Task 2/task_2_system_design.md`](Task%202/task_2_system_design.md) - Complete architecture design

### Task 3: MLOps & Deployment
**Goal**: Convert a delivery date prediction model from Jupyter notebook to production-ready deployment.

**Key Features**:
- Production API conversion with FastAPI
- Model monitoring and drift detection
- Automated rollback and versioning capabilities
- CI/CD pipeline implementation

**Technologies**: FastAPI, Docker, Kubernetes, Prometheus, Grafana, MLflow

**Files**:
- [`Task 3/task_3_mlops_deployment.md`](Task%203/task_3_mlops_deployment.md) - Complete MLOps strategy

## Sample Data

The project includes `sample_sessions.json` containing real Elasticsearch clickstream data with:
- Session tracking information
- Product details and SKUs
- Shipping and delivery information
- Timestamp data for feature engineering

## Quick Start

### Prerequisites
- Python 3.8+
- AWS CLI (for Task 2 concepts)
- Docker (for Task 3 concepts)

### Running Task 1 (Data Engineering)
```bash
cd Task\ 1/
pip install -r requirements.txt
python task_1_data_engineering.py
```

### Viewing Task 2 (System Design)
Open [`Task 2/task_2_system_design.md`](Task%202/task_2_system_design.md) to see the complete AWS architecture design with Mermaid diagrams.

### Viewing Task 3 (MLOps)
Open [`Task 3/task_3_mlops_deployment.md`](Task%203/task_3_mlops_deployment.md) to see the complete production deployment strategy.

## Key Concepts Covered

### Data Engineering
- JSON log processing
- Feature engineering for time-based data
- Batch vs real-time processing optimization
- Data validation and error handling

### System Design
- Real-time streaming architecture
- AWS managed services integration
- Low-latency optimization strategies
- Monitoring and observability patterns

### MLOps
- Model versioning and registry
- Production API design
- Monitoring and drift detection
- Automated deployment and rollback
- Infrastructure as Code

## Business Context

This project addresses a real-world scenario where an e-commerce platform needs to:
1. Process clickstream data to understand user behavior
2. Build real-time features for delivery date prediction
3. Deploy and maintain ML models in production

The solution demonstrates scalable, maintainable, and production-ready approaches to each challenge.

## Contributing

This is a technical assessment project. For questions or clarifications about the implementation, please refer to the individual task documentation files.

---

**Note**: This project demonstrates theoretical and practical approaches to modern data engineering, system design, and MLOps challenges. The implementations are designed to be educational and showcase best practices in each domain. 