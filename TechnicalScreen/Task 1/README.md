# Task 1: Data Engineering Solution

A focused solution for processing Elasticsearch JSON logs and generating model-ready features.

## Core Features

- **Timestamp Extraction**: Parse `createdDateTime` from Elasticsearch JSON logs
- **Feature Generation**: Create `day_of_year`, `day_of_week`, `hour_of_day` features
- **Batch Processing**: Optimized for model training with large datasets
- **Real-time Inference**: Optimized for low-latency single-record processing

## Installation

```bash
pip install -r requirements.txt

## Usage

### Quick Start

```python
from task_1_data_engineering import DataProcessor

# Initialize processor
processor = DataProcessor()

# Batch processing for training
training_df = processor.process_for_training('sample_sessions.json')
print(f"Processed {len(training_df)} records")

# Real-time inference
for record in processor.process_for_inference('sample_sessions.json'):
    print(record)
    break  # Process one record
```

### Run Demo

```bash
python task_1_data_engineering.py

## Output Format

### Batch Processing
```python
DataFrame with columns:
- day_of_year: Day of year (1-366)
- day_of_week: Day of week (0=Monday, 6=Sunday)  
- hour_of_day: Hour of day (0-23)
- record_id: Unique record identifier
- timestamp: Parsed datetime object
```

### Real-time Inference
```python
Dictionary with keys:
- record_id: Unique record identifier
- timestamp: Parsed datetime object
- day_of_year: Day of year (1-366)
- day_of_week: Day of week (0-6)
- hour_of_day: Hour of day (0-23)
```

## Input Format

Expected JSON structure:
```json
[
  {
    "_id": "record_id",
    "_source": {
      "createdDateTime": 1731880381293
    }
  }
]
``` 