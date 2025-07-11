"""
ShipPro Shipping Calculator
Optimized shipping calculation engine with O(1) lookups and caching
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from functools import lru_cache
import os

logger = logging.getLogger(__name__)

class ShippingCalculator:
    """
    Enterprise-grade shipping calculator with optimized performance
    
    Features:
    - O(1) zip code lookups with cached data
    - Vectorized distance calculations
    - Pre-computed service matrices
    - Memory-efficient data structures
    """
    
    def __init__(self, zip_data_path: str):
        """Initialize calculator with cached zip data"""
        self.zip_data_path = zip_data_path
        self._zip_coordinates: Optional[Dict[str, Tuple[float, float]]] = None
        self._service_matrix = self._build_service_matrix()
        self._seasonal_data = self._load_seasonal_config()
        
    @property
    def zip_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """Lazy-loaded, cached zip coordinate data"""
        if self._zip_coordinates is None:
            self._zip_coordinates = self._load_zip_data()
        return self._zip_coordinates
    
    def _load_zip_data(self) -> Dict[str, Tuple[float, float]]:
        """
        Load and cache zip code coordinates with optimized memory usage
        Time Complexity: O(n) - only runs once, then O(1) lookups
        """
        try:
            logger.info(f"Loading zip data from {self.zip_data_path}")
            
            # Optimized CSV loading with specific dtypes
            df = pd.read_csv(
                self.zip_data_path,
                usecols=['zip', 'lat', 'lng'],
                dtype={'zip': str, 'lat': 'float32', 'lng': 'float32'}
            )
            
            # Vectorized cleaning and conversion
            df['zip'] = df['zip'].str.strip('"').str.replace('.0', '', regex=False).str.zfill(5)
            
            # Convert to dictionary for O(1) lookups
            zip_dict = dict(zip(df['zip'], zip(df['lat'], df['lng'])))
            
            logger.info(f"Loaded {len(zip_dict):,} zip codes")
            return zip_dict
            
        except Exception as e:
            logger.error(f"Error loading zip data: {e}")
            raise
    
    def _build_service_matrix(self) -> Dict[str, List[Dict]]:
        """
        Pre-computed service options matrix for O(1) service lookups
        Eliminates conditional logic during calculation
        """
        return {
            'local': [  # 0-150 miles
                {'name': 'Express Overnight', 'base_days': 1, 'cost': 28.99},
                {'name': 'Two-Day Express', 'base_days': 2, 'cost': 16.99},
                {'name': 'Ground Shipping', 'base_days': 3, 'cost': 11.99}
            ],
            'regional': [  # 151-500 miles
                {'name': 'Express Overnight', 'base_days': 1, 'cost': 32.99},
                {'name': 'Two-Day Express', 'base_days': 2, 'cost': 19.99},
                {'name': 'Ground Shipping', 'base_days': 4, 'cost': 14.99}
            ],
            'national': [  # 501-1500 miles
                {'name': 'Express Overnight', 'base_days': 2, 'cost': 39.99},
                {'name': 'Two-Day Express', 'base_days': 3, 'cost': 24.99},
                {'name': 'Standard Ground', 'base_days': 5, 'cost': 16.99}
            ],
            'continental': [  # 1500+ miles
                {'name': 'Priority Express', 'base_days': 2, 'cost': 45.99},
                {'name': 'Cross-Country Express', 'base_days': 4, 'cost': 29.99},
                {'name': 'Economy Ground', 'base_days': 7, 'cost': 18.99}
            ]
        }
    
    def _load_seasonal_config(self) -> Dict:
        """Load seasonal adjustment configuration"""
        return {
            'peak_seasons': {
                'thanksgiving': (11, 22, 29),
                'christmas': (12, 15, 25),
                'black_friday': (11, 24, 27),
                'valentines': (2, 10, 14),
                'mothers_day': (5, 8, 12)
            },
            'weather_zones': {
                'northeast': {'lat_min': 41, 'lng_min': -100, 'winter_delay': 1},
                'midwest': {'lat_max': 41, 'lng_max': -100, 'winter_delay': 1},
                'south': {'lat_max': 37, 'lng_min': -100, 'winter_delay': 0},
                'west': {'default': True, 'winter_delay': 0}
            }
        }
    
    @lru_cache(maxsize=1000)
    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """
        Cached haversine distance calculation
        Time Complexity: O(1) for cached results, O(1) for calculation
        """
        lat1, lon1 = np.radians(coord1)
        lat2, lon2 = np.radians(coord2)
        
        # Vectorized haversine formula
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        
        return 3959 * 2 * np.arcsin(np.sqrt(a))  # Earth radius in miles
    
    def get_coordinates(self, zip_code: str) -> Optional[Tuple[float, float]]:
        """
        O(1) zip code coordinate lookup
        """
        clean_zip = str(zip_code).strip().zfill(5)
        return self.zip_coordinates.get(clean_zip)
    
    def _get_distance_category(self, distance: float) -> str:
        """O(1) distance category lookup"""
        if distance <= 150:
            return 'local'
        elif distance <= 500:
            return 'regional'
        elif distance <= 1500:
            return 'national'
        else:
            return 'continental'
    
    def _get_weather_zone(self, lat: float, lng: float) -> str:
        """Optimized weather zone determination"""
        if lat > 41 and lng > -100:
            return 'northeast'
        elif lat > 37 and lng < -100:
            return 'midwest'
        elif lat < 37 and lng > -100:
            return 'south'
        return 'west'
    
    def _is_peak_season(self, date: datetime) -> Tuple[bool, str]:
        """O(1) peak season check"""
        month, day = date.month, date.day
        
        for season, (s_month, start_day, end_day) in self._seasonal_data['peak_seasons'].items():
            if month == s_month and start_day <= day <= end_day:
                return True, season
        return False, ''
    
    def _calculate_business_days(self, start_date: datetime, days: int) -> datetime:
        """Optimized business day calculation"""
        # Calculate weekdays more efficiently
        current_date = start_date
        business_days_added = 0
        
        while business_days_added < days:
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                business_days_added += 1
                
        return current_date
    
    def _apply_adjustments(self, base_days: int, distance: float, is_peak: bool, 
                          peak_type: str, origin_zone: str, dest_zone: str, 
                          ship_date: datetime) -> int:
        """
        Optimized delivery time adjustments
        Reduced conditional complexity
        """
        adjusted_days = base_days
        
        # Peak season adjustments (O(1) lookup)
        if is_peak:
            peak_adjustments = {'christmas': 2, 'thanksgiving': 2, 'black_friday': 1, 'valentines': 1}
            adjusted_days += peak_adjustments.get(peak_type, 1)
        
        # Winter weather adjustments
        if ship_date.month in (12, 1, 2, 3):
            if origin_zone in ('midwest', 'northeast') or dest_zone in ('midwest', 'northeast'):
                adjusted_days += 1
        
        # Distance and timing adjustments
        if distance > 2000:
            adjusted_days += 1
        if ship_date.weekday() == 4:  # Friday shipments
            adjusted_days += 1
            
        return max(adjusted_days, 1)
    
    def calculate_shipping_estimate(self, origin_zip: str, dest_zip: str) -> Dict:
        """
        Main calculation method with optimized performance
        Time Complexity: O(1) for most operations, O(k) for k shipping services
        """
        try:
            # O(1) coordinate lookups
            origin_coords = self.get_coordinates(origin_zip)
            dest_coords = self.get_coordinates(dest_zip)
            
            if not origin_coords or not dest_coords:
                return {"error": "Invalid zip code(s). Please enter valid 5-digit US zip codes."}
            
            # O(1) cached distance calculation
            distance = self.calculate_distance(origin_coords, dest_coords)
            
            # O(1) service matrix lookup
            distance_category = self._get_distance_category(distance)
            services = self._service_matrix[distance_category]
            
            # Pre-calculate common values
            today = datetime.now()
            is_peak, peak_type = self._is_peak_season(today)
            origin_zone = self._get_weather_zone(*origin_coords)
            dest_zone = self._get_weather_zone(*dest_coords)
            
            # Process services efficiently
            estimates = []
            for service in services:
                adjusted_days = self._apply_adjustments(
                    service['base_days'], distance, is_peak, peak_type,
                    origin_zone, dest_zone, today
                )
                
                delivery_date = self._calculate_business_days(today, adjusted_days)
                
                estimates.append({
                    'service_name': service['name'],
                    'delivery_date': delivery_date.strftime('%B %d, %Y'),
                    'delivery_days': adjusted_days,
                    'cost': service['cost']
                })
            
            return {
                'distance_miles': round(distance, 1),
                'estimates': estimates,
                'peak_season': is_peak,
                'peak_type': peak_type if is_peak else None
            }
            
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return {"error": "An error occurred during calculation. Please try again."}

# Global calculator instance for reuse
_calculator_instance: Optional[ShippingCalculator] = None

def get_calculator(zip_data_path: str) -> ShippingCalculator:
    """
    Singleton pattern for calculator instance
    Prevents repeated data loading
    """
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = ShippingCalculator(zip_data_path)
    return _calculator_instance 