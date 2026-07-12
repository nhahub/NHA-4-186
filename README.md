# AI-Powered Predictive Maintenance System

A full-stack application for aircraft turbofan engine health monitoring, Remaining Useful Life (RUL) prediction, maintenance scheduling, and AI-assisted querying using Retrieval-Augmented Generation (RAG).

Built as the team project for the **Digital Egypt Pioneers Initiative (DEPI)** — Microsoft Machine Learning track.

## Key Features

- **RUL Prediction** — XGBoost regression model with SHAP explainability
- **AI Assistant (RAG)** — Chat with your maintenance knowledge base via local LLM (LM Studio + FAISS)
- **Dashboard & Reports** — KPIs, health distribution, prediction trends, engineer activity, critical engine alerts
- **Maintenance Management** — Log, track, and search maintenance records per engine
- **Role-Based Access** — Admin and Engineer roles with per-user activity tracking
- **PDF & Excel Export** — Downloadable prediction reports and full system analytics

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (multi-page app) |
| Backend / ML | Python 3.11, XGBoost, scikit-learn, SHAP |
| RAG | sentence-transformers, FAISS, OpenAI client (LM Studio) |
| Database | SQLite |
| Visualization | Plotly, Matplotlib |
| Reporting | ReportLab (PDF), openpyxl (Excel) |

## Project Structure

```
├── app/
│   ├── home.py                    # Login / signup page
│   ├── pages/
│   │   ├── Prediction.py          # Manual & CSV RUL prediction with SHAP
│   │   ├── AIAssistant.py         # RAG chat with maintenance knowledge base
│   │   ├── History.py             # Prediction history per user
│   │   ├── Maintenance.py         # Maintenance dashboard & analytics
│   │   ├── Maintenance_Records.py # Log, drill-down, browse all records
│   │   └── Reports.py             # System-wide reports & export
│   └── utils/
│       ├── sidebar.py             # Navigation sidebar
│       ├── styles.py              # Global CSS & status badges
│       └── path_setup.py          # sys.path configuration
├── ai/
│   ├── predict.py                 # XGBoost prediction (Predictor class)
│   ├── explain.py                 # SHAP explainability (Explainability class)
│   ├── preprocessing.py           # Feature scaling & validation
│   ├── rag.py                     # RAG engine (FAISS + LM Studio)
│   └── model/
│       ├── xgboost_rul_model.pkl  # Trained XGBoost model
│       ├── standard_scaler.pkl    # Feature scaler
│       └── feature_names.pkl      # Ordered feature list
├── application/
│   ├── auth/
│   │   └── service.py             # Login, registration, password hashing
│   ├── prediction/
│   │   ├── service.py             # Prediction orchestration
│   │   └── validator.py           # Input validation
│   └── reports/
│       ├── reports.py             # All report SQL queries
│       ├── charts.py              # Plotly chart builders
│       ├── export.py              # PDF & Excel export
│       └── theme.py               # Chart theming
├── database/
│   ├── database.py                # SQLite connection (dict + pandas factories)
│   ├── models.py                  # Schema creation (CREATE TABLE)
│   ├── queries.py                 # CRUD operations
│   └── maintenance.db             # SQLite database
├── data/
│   └── knowledge_base.txt         # RAG knowledge base document
├── run.py                         # App entry point
└── requirements.txt               # Python dependencies
```

## Requirements

### Python

- Python 3.11+

### Python Packages

```
streamlit>=1.58
pandas>=2.3
numpy>=2.4
matplotlib>=3.10
shap>=0.51
joblib>=1.5
bcrypt>=5.0
plotly>=6.8
reportlab>=5.0
openpyxl>=3.1
scikit-learn>=1.9
xgboost>=2.0
openai>=1.0
sentence-transformers>=3.0
faiss-cpu>=1.8
```

### External Services (for RAG)

- [LM Studio](https://lmstudio.ai/) running locally on `http://127.0.0.1:1234`
- A loaded text-generation model (e.g. `google/gemma-4-e4b`)

## Setup

```bash
# Clone the repository
git clone https://github.com/myler71/DEPI-Team-project-.git
cd DEPI-Team-project-

# Install dependencies
pip install -r requirements.txt

# Initialize the database (creates tables + seeds data)
python -c "from database.models import create_tables; create_tables()"

# Run the application
python run.py
```

The app opens at **http://localhost:8501**.

### Default Login

| Username | Password | Role |
|----------|----------|------|
| test | test1234 | Admin |

## How It Works

### Prediction Pipeline

1. User inputs sensor readings (17 features) or uploads a NASA C-MAPSS test file
2. Features are scaled with the pre-trained StandardScaler
3. XGBoost model predicts Remaining Useful Life (RUL) in cycles
4. SHAP TreeExplainer generates per-feature contribution plots
5. Results are saved to the database with health status classification

### RAG Assistant

1. Knowledge base text is split into overlapping chunks (120 words, 20 overlap)
2. Chunks are embedded with `all-MiniLM-L6-v2` and indexed in FAISS
3. User queries retrieve the top-K most relevant chunks
4. LM Studio generates a response using role-specific system prompts:
   - **Maintenance Engineer** — technical, evidence-based
   - **Field Monitoring Worker** — plain-language with traffic-light status
   - **General User** — high-level summary with optional depth

## License

This project was developed for educational purposes under the Digital Egypt Pioneers Initiative (DEPI).
