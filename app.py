"""
ShipPro Shipping Calculator 
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

from config import config
from models.shipping import get_calculator

def create_app(config_name: str = None) -> Flask:
    """Simple application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize calculator
    calculator = get_calculator(app.config['ZIP_DATA_PATH'])
    
    @app.route('/')
    def index():
        """Main shipping calculator page"""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Simple health check"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    @app.route('/api/calculate', methods=['POST'])
    def calculate_shipping():
        """Calculate shipping estimates"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            origin = data.get('origin', '').strip()
            destination = data.get('destination', '').strip()
            
            # Simple validation
            if not origin or not destination:
                return jsonify({'error': 'Please enter both origin and destination zip codes'}), 400
            
            if len(origin) != 5 or len(destination) != 5 or not origin.isdigit() or not destination.isdigit():
                return jsonify({'error': 'Please enter valid 5-digit zip codes'}), 400
            
            # Calculate shipping
            result = calculator.calculate_shipping_estimate(origin, destination)
            
            if 'error' in result:
                return jsonify(result), 400
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': 'Calculation error occurred'}), 500
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', True)
    ) 