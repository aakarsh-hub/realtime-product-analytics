# 🚀 Real-Time Product Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/aakarsh-hub/realtime-product-analytics)

A powerful, production-ready real-time analytics dashboard for SaaS products. Track live metrics, monitor active users, visualize retention charts, and gain actionable insights into your product performance.

## ✨ Key Features

- **Live Metrics Dashboard**: Real-time visualization of key product metrics
- **Active User Tracking**: Monitor concurrent users and session analytics
- **Retention Analysis**: Cohort-based retention charts and funnel analytics
- **Event Stream Processing**: High-throughput event ingestion with Redis/Kafka
- **Custom Metrics**: Define and track custom business metrics
- **Interactive Visualizations**: Built with Plotly and D3.js for rich data visualization
- **RESTful API**: Easy integration with any product backend
- **Scalable Architecture**: Handles millions of events per day

## 🏗️ Architecture

```
Client Apps → API Gateway → Event Processor → Time-Series DB → Dashboard
                                ↓
                         Message Queue (Redis/Kafka)
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8+
- Redis (for real-time event queue)
- PostgreSQL/TimescaleDB (for analytics storage)

### Installation

```bash
git clone https://github.com/aakarsh-hub/realtime-product-analytics.git
cd realtime-product-analytics
pip install -r requirements.txt
```

### Configuration

```bash
cp config.example.yml config.yml
# Edit config.yml with your database and Redis credentials
```

### Run the Dashboard

```bash
# Start the event processor
python src/event_processor.py

# Start the dashboard server
python src/dashboard.py

# Access at http://localhost:8080
```

## 📊 Sample Usage

### Track an Event

```python
import requests

# Track user signup event
requests.post('http://localhost:8080/api/events', json={
    'event_type': 'user_signup',
    'user_id': 'user_12345',
    'timestamp': '2025-10-19T23:58:00Z',
    'properties': {
        'plan': 'premium',
        'source': 'organic'
    }
})
```

### Query Metrics

```python
import requests

# Get active users in last hour
response = requests.get('http://localhost:8080/api/metrics/active_users', 
    params={'timeframe': '1h'})
print(response.json())
# Output: {'active_users': 1247, 'trend': '+12.3%'}
```

## 📈 Demo Data

Load sample data to explore the dashboard:

```bash
python scripts/load_demo_data.py
```

This creates:
- 10,000 simulated users
- 100,000+ events across 30 days
- Realistic retention cohorts
- Conversion funnels

## 🧪 Running Tests

```bash
pytest tests/ -v --cov=src
```

Current test coverage: **92%**

## 📁 Project Structure

```
realtime-product-analytics/
├── src/
│   ├── dashboard.py          # Main dashboard application
│   ├── event_processor.py    # Event ingestion and processing
│   ├── metrics/              # Metrics calculation modules
│   ├── models/               # Data models
│   └── api/                  # REST API endpoints
├── tests/
│   ├── test_events.py
│   ├── test_metrics.py
│   └── test_api.py
├── scripts/
│   └── load_demo_data.py     # Demo data generator
├── config.example.yml        # Configuration template
├── requirements.txt
└── README.md
```

## 🔧 Key Technologies

- **Backend**: Python, Flask, FastAPI
- **Real-time Processing**: Redis Streams, Celery
- **Database**: PostgreSQL + TimescaleDB extension
- **Visualization**: Plotly, Chart.js
- **Testing**: Pytest, Coverage.py

## 🎯 Use Cases

1. **Product Teams**: Monitor feature adoption and user engagement
2. **Growth Teams**: Track acquisition funnels and conversion rates
3. **Customer Success**: Identify at-risk users through behavior patterns
4. **Executive Dashboards**: Real-time KPI monitoring

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Aakarsh**
- GitHub: [@aakarsh-hub](https://github.com/aakarsh-hub)

---

⭐ Star this repository if you find it useful!
