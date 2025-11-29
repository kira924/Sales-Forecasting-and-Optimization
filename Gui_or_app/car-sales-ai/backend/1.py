# test_ml_service.py
from app.services.ml_service import ml_service

# حاول توليد forecast كامل
forecast = ml_service.generate_sales_forecast(view_type="full")
print(forecast)
