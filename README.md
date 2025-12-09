# Car Sales Forecasting & Optimization — Full Project

A complete end-to-end system for forecasting car sales, ranking dealership priorities, and generating actionable insights using Machine Learning & Prophet models — wrapped inside a full-stack web application (React + FastAPI).

## Project Structure

```
sales_forcasting_and_optimization/
│
├── Data_preprocessing/           # Raw + cleaned datasets + preprocessing scripts
├── Data_sample/                  # Small data samples
├── Deployment/                   # Model training & saving + trained models
│
├── Gui_or_app/
│   └── car-sales-ai/
│       ├── backend/              # FastAPI backend + ML service
│       ├── src/                  # React frontend source code
│       ├── public/               # Frontend public assets
│       ├── build/                # Production build (optional)
│       ├── Dockerfile            # Frontend Docker image
│       ├── docker-compose.yml    # Full system deployment
│
├── Modeling_and_evaluation/      # Notebooks + deep analysis
├── Screenshots/                  # UI demo screenshots
│
├── .gitignore
└── README.md (this file)
```

## Tech Stack

### Frontend

- React (Vite/CRA)
- TailwindCSS
- ShadCN UI
- Charts (Recharts)

### Backend

- FastAPI
- Uvicorn
- MLflow-ready service layout

### Machine Learning

- Facebook Prophet
- XGBoost
- Scikit-learn
- Custom preprocessing pipelines

## Features

- Monthly & yearly sales forecasting (Prophet)
- Dealership priority ranking engine
- Seasonality & Trend decomposition visualizations
- Real-time API
- Authentication system
- Fully dockerized deployment

## Installation

1. **Backend**
   ```
   cd Gui_or_app/car-sales-ai/car-sales-ai/backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend**
   ```
   cd Gui_or_app/car-sales-ai/car-sales-ai
   npm install
   npm start
   ```

## Docker Deployment

```
docker-compose up --build
```

## API Documentation

Once the backend is running, you can access the Swagger UI at:

```
http://localhost:8000/docs
```

## Project Status

- ✅ ML models trained
- ✅ API working
- ✅ Frontend integrated
- ✅ deploy on huggingface

## License

Free to use for research & educational purposes.

## Contributing

Pull requests are welcome!

## Author

GitHub: kira924
