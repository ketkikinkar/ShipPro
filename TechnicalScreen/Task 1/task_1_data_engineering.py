"""
Task 1: Data Engineering Solution for Elasticsearch JSON Log Processing
======================================================================

Core functionality:
1. Extract timestamps from createdDateTime
2. Generate features: day_of_year, day_of_week, hour_of_day
3. Support both batch processing and real-time inference
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Iterator, Optional, Union
import pandas as pd
from functools import lru_cache


class TimestampExtractor:
    """Extract timestamps from Elasticsearch JSON logs."""
    
    def parse_created_datetime(self, timestamp_ms: Union[int, str]) -> datetime:
        """Parse createdDateTime timestamp to datetime object."""
        try:
            if isinstance(timestamp_ms, str):
                timestamp_ms = int(timestamp_ms)
            timestamp_s = timestamp_ms / 1000
            return datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        except (ValueError, TypeError, OSError):
            return None
    
    def extract_timestamp_from_record(self, record: Dict) -> Optional[datetime]:
        """Extract timestamp from a single Elasticsearch record."""
        try:
            if '_source' in record and 'createdDateTime' in record['_source']:
                timestamp_ms = record['_source']['createdDateTime']
                return self.parse_created_datetime(timestamp_ms)
            return None
        except Exception:
            return None
    
    def load_json_file(self, file_path: str) -> List[Dict]:
        """Load JSON file into memory."""
        with open(file_path, 'r') as f:
            return json.load(f)


class FeatureGenerator:
    """Generate model-ready features from timestamps."""
    
    @lru_cache(maxsize=10000)
    def _get_day_of_year(self, year: int, month: int, day: int) -> int:
        """Get day of year (cached for performance)."""
        return datetime(year, month, day).timetuple().tm_yday
    
    @lru_cache(maxsize=10000)
    def _get_day_of_week(self, year: int, month: int, day: int) -> int:
        """Get day of week (0=Monday, 6=Sunday)."""
        return datetime(year, month, day).weekday()
    
    def generate_features_single(self, timestamp: datetime) -> Dict[str, int]:
        """Generate features for a single timestamp (real-time inference)."""
        if timestamp is None:
            return {'day_of_year': None, 'day_of_week': None, 'hour_of_day': None}
        
        try:
            year, month, day = timestamp.year, timestamp.month, timestamp.day
            hour = timestamp.hour
            
            return {
                'day_of_year': self._get_day_of_year(year, month, day),
                'day_of_week': self._get_day_of_week(year, month, day),
                'hour_of_day': hour
            }
        except Exception:
            return {'day_of_year': None, 'day_of_week': None, 'hour_of_day': None}
    
    def generate_features_vectorized(self, timestamps: List[datetime]) -> pd.DataFrame:
        """Vectorized feature generation (batch processing)."""
        try:
            ts_series = pd.Series(timestamps)
            return pd.DataFrame({
                'day_of_year': ts_series.dt.dayofyear,
                'day_of_week': ts_series.dt.dayofweek,
                'hour_of_day': ts_series.dt.hour
            })
        except Exception:
            # Fallback to single record processing
            features = [self.generate_features_single(ts) for ts in timestamps]
            return pd.DataFrame(features)


class DataProcessor:
    """Main data processor combining timestamp extraction and feature generation."""
    
    def __init__(self):
        self.timestamp_extractor = TimestampExtractor()
        self.feature_generator = FeatureGenerator()
    
    def process_for_training(self, file_path: str) -> pd.DataFrame:
        """Process data for model training (batch processing)."""
        # Load and extract timestamps
        records = self.timestamp_extractor.load_json_file(file_path)
        timestamps_data = []
        
        for record in records:
            timestamp = self.timestamp_extractor.extract_timestamp_from_record(record)
            if timestamp:
                record_id = record.get('_id', 'unknown')
                timestamps_data.append((record_id, timestamp))
        
        # Separate IDs and timestamps
        record_ids, timestamps = zip(*timestamps_data) if timestamps_data else ([], [])
        
        # Generate features
        features_df = self.feature_generator.generate_features_vectorized(timestamps)
        features_df['record_id'] = record_ids
        features_df['timestamp'] = timestamps
        
        return features_df
    
    def process_for_inference(self, file_path: str) -> Iterator[Dict]:
        """Process data for real-time inference."""
        records = self.timestamp_extractor.load_json_file(file_path)
        
        for record in records:
            timestamp = self.timestamp_extractor.extract_timestamp_from_record(record)
            
            if timestamp:
                features = self.feature_generator.generate_features_single(timestamp)
                yield {
                    'record_id': record.get('_id', 'unknown'),
                    'timestamp': timestamp,
                    **features
                }


def main():
    """Example usage for Task 1."""
    processor = DataProcessor()
    
    # Batch processing for training
    print("=== Batch Processing (Training) ===")
    training_df = processor.process_for_training('sample_sessions.json')
    print(f"Processed {len(training_df)} records")
    print(training_df.head())
    
    # Real-time inference
    print("\n=== Real-time Inference ===")
    for i, record in enumerate(processor.process_for_inference('sample_sessions.json')):
        print(f"Record {i+1}: {record}")
        if i >= 2:  # Show first 3 records
            break


if __name__ == "__main__":
    main() 