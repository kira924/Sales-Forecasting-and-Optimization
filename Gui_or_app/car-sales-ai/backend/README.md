# 🚗 Car Sales AI Platform - Backend API

FastAPI backend for AI-powered sales forecasting and inventory ranking system.

---

## Quick Start

### **Prerequisites**
- Python 3.11+
- pip
- Virtual environment (recommended)

### **Installation**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Edit .env with your configuration
nano .env  # or use your favorite editor

# 6. Save your trained models (IMPORTANT!)
python save_models.py

# 7. Run the server
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── forecast.py      # Sales forecast endpoints
│   │   └── ranking.py       # Priority ranking endpoints
│   ├── services/
│   │   ├── ml_service.py    # ML model service
│   │   └── auth_service.py  # Authentication service
│   └── utils/
│       └── helpers.py       # Helper functions
├── models/                  # Trained ML models (*.pkl)
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── Dockerfile              # Docker configuration
```

---

## 📊 API Endpoints

### **Authentication**

```bash
# Sign Up
POST /api/auth/signup
Body: {
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "company_name": "ABC Dealership"}

# Sign In
POST /api/auth/signin
Body: {
  "email": "john@example.com",
  "password": "password123"}
Response: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"}

# Get Current User
GET /api/auth/me
Headers: Authorization: Bearer <token>
```

### **Sales Forecasting**

```bash
# Generate Forecast
POST /api/forecast/sales
Headers: Authorization: Bearer <token>
Body: {
  "view_type": "full"  # or "quick" 
}

Response: {
  "total_forecast": 18500000000,
  "total_2024": 17500000000,
  "growth_rate": 5.7,
  "monthly_forecast": [
    {
      "month": "Jan 2025",
      "forecast": 1501577,
      "lower_bound": 1325000,
      "upper_bound": 1678000
    },
    ...
  ]
}

# Health Check
GET /api/forecast/health
```

### **Priority Ranking**

```bash
# Generate Ranking
POST /api/ranking/priority
Headers: Authorization: Bearer <token>
Body: {
  "cars": [
    {
      "make": "Mercedes",
      "model": "C-Class",
      "year": 2023,
      "quantity": 1
    },
    {
      "make": "Toyota",
      "model": "Camry",
      "year": 2023,
      "quantity": 2
    }
  ],
  "target_month": "November",
  "target_year": 2025,
  "region": "East",
  "profit_margin": 0.15
}

Response: {
  "rankings": [
    {
      "make": "Mercedes",
      "model": "C-Class",
      "year": 2023,
      "age": 2,
      "quantity": 1,
      "profit": 2008.45,
      "confidence": 67.5,
      "risk": "LOW"
    },
    ...
  ]
}

# Health Check
GET /api/ranking/health
```

---

## 🔧 Configuration

### **Environment Variables (.env)**

```bash
# Application
APP_NAME=Car Sales AI Platform
DEBUG=True
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# CORS (Add your frontend URL)
CORS_ORIGINS=["http://localhost:3000"]

# JWT Secret (Generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Model Paths
PROFIT_MODEL_PATH=models/priority_ranking_model.pkl
FEATURE_SCALER_PATH=models/full_preprocessor.pkl
PROPHET_MODEL_PATH=models/prophet_sales_model.pkl
```

---

## Saving Your Trained Models

**IMPORTANT:** You must save your trained models before running the backend.

```python
# save_models.py
import joblib
from your_training_script import xgb_model, feature_scaler, prophet_model

# Save models
joblib.dump(xgb_model, 'models/priority_ranking_model.pkl')
joblib.dump(feature_scaler, 'models/full_preprocessor.pkl')
joblib.dump(prophet_model, 'models/prophet_sales_model.pkl')  # Optional

print(" Models saved successfully!")
```

Then run:
```bash
python save_models.py
```

---

## Docker Deployment

```bash
# Build image
docker build -t car-sales-backend .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  --name car-sales-backend \
  car-sales-backend

# Or use docker-compose (from root directory)
docker-compose up -d
```

---

## Testing

```bash
# Run with test data
curl -X POST http://localhost:8000/api/forecast/sales \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"view_type": "full"}'

# Check health
curl http://localhost:8000/health
```

---

## Logging

Logs are saved to:
- **File:** `logs/app.log`
- **Console:** Standard output

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## Security

### **Production Checklist:**
- [ ] Generate strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use HTTPS
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up proper authentication
- [ ] Enable logging
- [ ] Add monitoring

---

##  Production Deployment

### **Option 1: Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **Option 2: Traditional Server**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (production server)
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### **Option 3: Cloud Platforms**

**AWS (Elastic Beanstalk):**
```bash
eb init
eb create car-sales-api
eb deploy
```

**Google Cloud (Cloud Run):**
```bash
gcloud run deploy car-sales-api \
  --source . \
  --platform managed \
  --region us-central1
```

**Heroku:**
```bash
heroku create car-sales-api
git push heroku main
```

---

## Troubleshooting

**Issue: Models not loading**
```bash
# Check if model files exist
ls -la models/

# Re-save models
python save_models.py
```

**Issue: CORS errors**
```bash
# Add your frontend URL to CORS_ORIGINS in .env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

**Issue: Prophet installation fails**
```bash
# Install Prophet dependencies first
pip install pystan
pip install prophet
```

---

##  Support

For issues or questions:
- Open an issue on GitHub
- Contact: kirakel924@gmail.com

