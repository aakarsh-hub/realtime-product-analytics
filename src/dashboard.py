"""Real-Time Product Analytics Dashboard

Main dashboard application with live metrics visualization.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import redis
import json
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Redis connection for real-time data
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def index():
    """Main dashboard page"""
    return jsonify({
        'status': 'active',
        'message': 'Real-Time Product Analytics Dashboard',
        'version': '1.0.0',
        'endpoints': [
            '/api/events',
            '/api/metrics/active_users',
            '/api/metrics/retention',
            '/api/metrics/funnel'
        ]
    })

@app.route('/api/events', methods=['POST'])
def track_event():
    """Track a new event"""
    try:
        event_data = request.json
        event_data['timestamp'] = event_data.get('timestamp', datetime.utcnow().isoformat())
        
        # Store in Redis stream
        event_id = redis_client.xadd('events:stream', event_data)
        
        # Update real-time counters
        event_type = event_data.get('event_type')
        redis_client.incr(f'counter:{event_type}:today')
        redis_client.sadd('active_users:current', event_data.get('user_id'))
        
        return jsonify({
            'success': True,
            'event_id': event_id,
            'message': 'Event tracked successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/metrics/active_users', methods=['GET'])
def get_active_users():
    """Get active users count"""
    timeframe = request.args.get('timeframe', '1h')
    
    # Get current active users
    active_count = redis_client.scard('active_users:current')
    
    # Calculate trend (mock calculation for demo)
    previous_count = active_count * 0.9  # Simulated previous period
    trend = ((active_count - previous_count) / previous_count * 100) if previous_count > 0 else 0
    
    return jsonify({
        'active_users': active_count,
        'trend': f'{trend:+.1f}%',
        'timeframe': timeframe,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/metrics/retention', methods=['GET'])
def get_retention():
    """Get retention cohort data"""
    # Sample retention data (in production, calculate from actual user data)
    cohorts = [
        {'cohort': 'Week 1', 'day_0': 100, 'day_1': 45, 'day_7': 32, 'day_30': 18},
        {'cohort': 'Week 2', 'day_0': 100, 'day_1': 48, 'day_7': 35, 'day_30': 22},
        {'cohort': 'Week 3', 'day_0': 100, 'day_1': 52, 'day_7': 38, 'day_30': 25},
        {'cohort': 'Week 4', 'day_0': 100, 'day_1': 50, 'day_7': 36, 'day_30': None}
    ]
    
    return jsonify({
        'cohorts': cohorts,
        'metric': 'retention_rate',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/metrics/funnel', methods=['GET'])
def get_funnel():
    """Get conversion funnel metrics"""
    # Sample funnel data
    funnel_stages = [
        {'stage': 'Visited Homepage', 'users': 10000, 'conversion_rate': 100},
        {'stage': 'Signed Up', 'users': 2500, 'conversion_rate': 25},
        {'stage': 'Activated Feature', 'users': 1200, 'conversion_rate': 12},
        {'stage': 'Made Purchase', 'users': 450, 'conversion_rate': 4.5}
    ]
    
    return jsonify({
        'funnel': funnel_stages,
        'overall_conversion': 4.5,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/metrics/live', methods=['GET'])
def get_live_metrics():
    """Get live dashboard metrics"""
    return jsonify({
        'active_users_now': redis_client.scard('active_users:current'),
        'events_last_minute': redis_client.get('events:last_minute') or 0,
        'total_events_today': sum([
            int(redis_client.get(key) or 0) 
            for key in redis_client.scan_iter('counter:*:today')
        ]),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Real-Time Product Analytics Dashboard")
    print("  Server starting on http://localhost:8080")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=8080, debug=True)
