# DEPI-Team-project

**AI-Powered Predictive Maintenance System**

A Streamlit-based web application that uses machine learning (XGBoost) to predict Remaining Useful Life (RUL) of industrial assets and manage maintenance schedules.

## Tech Stack

- **Frontend:** Streamlit (Python)
- **ML Model:** XGBoost regressor for RUL prediction
- **Database:** SQLite
- **Libraries:** pandas, scikit-learn, xgboost, plotly

## Project Structure

```
AI_Predictive_Maintenance/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── generate_report.py              # Auto-generate technical report
├── reset_users.py                  # Reset user accounts
├── test_db.py                      # Database test script
│
├── ai/                             # Machine Learning module
│   ├── model/
│   │   ├── xgboost_rul_model.pkl   # Trained XGBoost model
│   │   ├── standard_scaler.pkl     # Feature scaler
│   │   └── feature_names.pkl       # Feature name mapping
│   ├── predict.py                  # RUL prediction logic
│   ├── preprocessing.py            # Data preprocessing
│   ├── feature_engineering.py      # Feature engineering
│   └── explain.py                  # Model explainability
│
├── app/                            # Streamlit UI layer
│   ├── home.py                     # Home/dashboard page
│   ├── pages/
│   │   ├── Prediction.py           # RUL prediction page
│   │   ├── Maintenance.py          # Maintenance scheduling
│   │   ├── Maintenance_Records.py  # Maintenance history records
│   │   ├── History.py              # Historical data views
│   │   └── Reports.py              # Analytics & reports
│   ├── utils/
│   │   ├── sidebar.py              # Sidebar navigation
│   │   ├── styles.py               # Custom CSS styles
│   │   └── path_setup.py           # Path configuration
│   └── survey-filler/              # Chrome extension (survey helper)
│       ├── manifest.json
│       └── content.js
│
├── application/                    # Business logic layer
│   ├── auth/
│   │   ├── service.py              # Authentication service
│   │   ├── password.py             # Password hashing
│   │   └── validator.py            # Input validation
│   ├── prediction/
│   │   ├── service.py              # Prediction business logic
│   │   └── validator.py            # Prediction validation
│   └── reports/
│       ├── reports.py              # Report generation
│       ├── charts.py               # Chart configurations
│       ├── export.py               # Export functionality
│       └── theme.py                # Report theming
│
├── database/                       # Database layer
│   ├── database.py                 # DB connection & setup
│   ├── models.py                   # SQLAlchemy models
│   ├── queries.py                  # Database queries
│   └── maintenance.db              # SQLite database file
│
└── data/                           # Data assets
```

## Key Features

- **RUL Prediction** - Predict remaining useful life of equipment using XGBoost
- **Maintenance Scheduling** - Plan and track preventive maintenance
- **Maintenance Records** - Log and review maintenance history
- **Interactive Reports** - Visualize trends with Plotly charts
- **User Authentication** - Secure login with password hashing

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The app will open in your browser at `http://localhost:8501`.

## License

DEPI Team Project
