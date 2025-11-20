"""
Script to save your trained models to the backend/models directory

Run this after training your models:
    python save_models.py
"""

import joblib
import os

def save_models(
    profit_model,
    feature_scaler,
    prophet_model=None,
    prophet_scaler=None
):
    """
    Save trained models to disk
    
    Parameters:
    -----------
    profit_model : XGBoost model
        Trained profit prediction model
    feature_scaler : StandardScaler
        Feature scaler for profit model
    prophet_model : Prophet model (optional)
        Trained sales forecasting model
    prophet_scaler : StandardScaler (optional)
        Feature scaler for prophet model
    """
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save profit prediction model
    print(" Saving profit prediction model...")
    joblib.dump(profit_model, 'models/profit_model.pkl')
    print(" Saved: models/profit_model.pkl")
    
    # Save feature scaler
    print(" Saving feature scaler...")
    joblib.dump(feature_scaler, 'models/feature_scaler.pkl')
    print(" Saved: models/feature_scaler.pkl")
    
    # Save prophet model (if provided)
    if prophet_model:
        print(" Saving prophet model...")
        joblib.dump(prophet_model, 'models/prophet_model.pkl')
        print(" Saved: models/prophet_model.pkl")
    
    # Save prophet scaler (if provided)
    if prophet_scaler:
        print(" Saving prophet scaler...")
        joblib.dump(prophet_scaler, 'models/prophet_scaler.pkl')
        print(" Saved: models/prophet_scaler.pkl")
    
    print("\n All models saved successfully!")
    print(" Models directory: ./models/")
    print("\nNext step: Start the backend server with 'uvicorn app.main:app --reload'")

# Example usage:
if __name__ == "__main__":
    # Load your trained models here
    # Example:
    # from your_training_script import best_model, scaler, prophet_model
    
    # For demonstration, we'll show how to do it:
    print("  This is a template script!")
    print(" Instructions:")
    print("1. Replace these lines with your actual model loading code")
    print("2. Example:")
    print("   from your_notebook import xgb_model, feature_scaler")
    print("   save_models(xgb_model, feature_scaler)")
    print()
    print("3. Or load from existing pickle files:")
    print("   import joblib")
    print("   profit_model = joblib.load('path/to/your/model.pkl')")
    print("   scaler = joblib.load('path/to/your/scaler.pkl')")
    print("   save_models(profit_model, scaler)")
    
    # Uncomment and modify these lines once you have your models:
    # 
    # import joblib
    # 
    # # Load your trained models
    # profit_model = joblib.load('../path/to/your/xgboost_model.pkl')
    # feature_scaler = joblib.load('../path/to/your/scaler.pkl')
    # prophet_model = joblib.load('../path/to/your/prophet_model.pkl')  # Optional
    # 
    # # Save them to backend/models
    # save_models(
    #     profit_model=profit_model,
    #     feature_scaler=feature_scaler,
    #     prophet_model=prophet_model  # Optional
    # )