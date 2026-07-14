# AI-Powered Predictive Maintenance System

A full-stack application for aircraft turbofan engine health monitoring, Remaining Useful Life (RUL) prediction, maintenance scheduling, and AI-assisted querying using Retrieval-Augmented Generation (RAG).

Built as the team project for the **Digital Egypt Pioneers Initiative (DEPI)** — Microsoft Machine Learning track.

## Key Features

- **RUL Prediction** — XGBoost regression model with SHAP explainability
- **MLflow Experiment Tracking** — Log params, metrics, model artifacts, and visualizations for training runs
- **AI Assistant (RAG)** — Chat with your maintenance knowledge base via Groq-hosted LLM + FAISS
- **Dashboard & Reports** — KPIs, health distribution, prediction trends, engineer activity, critical engine alerts
- **Maintenance Management** — Log, track, and search maintenance records per engine
- **Role-Based Access** — Admin and Engineer roles with per-user activity tracking
- **PDF & Excel Export** — Downloadable prediction reports and full system analytics

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (multi-page app) |
| Backend / ML | Python 3.11, XGBoost, scikit-learn, SHAP |
| Experiment Tracking | MLflow (training logs, inference monitoring) |
| RAG | sentence-transformers, FAISS, OpenAI client (Groq API) |
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
│   ├── train.py                   # MLflow training experiments
│   ├── explain.py                 # SHAP explainability (Explainability class)
│   ├── preprocessing.py           # Feature scaling & validation
│   ├── rag.py                     # RAG engine (FAISS + Groq)
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
├── notebooks/
│   ├── MLflow_Integration_Demo.ipynb  # MLflow demo notebook
│   ├── depi_RAG.ipynb                 # RAG notebook
│   └── depi_rag.py                    # RAG script
├── mlruns/                            # MLflow experiment tracking data
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
mlflow>=2.0
```

### External Services (for RAG)

- [Groq API](https://console.groq.com/) — Free tier, provides fast inference via `llama-3.3-70b-versatile`
- Embeddings run locally via `sentence-transformers/all-MiniLM-L6-v2` (no external service needed)

## Setup

```bash
# Clone the repository
git clone https://github.com/myler71/DEPI-project-RAG.git
cd DEPI-project-RAG

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
4. Groq generates a response using role-specific system prompts:
   - **Maintenance Engineer** — technical, evidence-based
   - **Field Monitoring Worker** — plain-language with traffic-light status
   - **General User** — high-level summary with optional depth

## Changelog

### v3.0 — MLflow Integration

**New:**
- **Training experiments with MLflow** — `ai/train.py` runs 6 XGBoost experiments with different hyperparameters (baseline, deeper, more trees, lower LR, subsample, custom). Each run logs params, metrics (RMSE, MAE, R2, MAPE), model artifacts, and 5 plots (RUL distribution, prediction vs actual, feature importance, residuals, health distribution).
- **Batch inference monitoring** — `application/prediction/service.py` now logs batch prediction metrics to a separate MLflow experiment ("Predictive Maintenance - Inference") tracking avg/min/max/std/median RUL and engine health counts.
- **MLflow Demo Notebook** — `notebooks/MLflow_Integration_Demo.ipynb` shows MLflow basics for the project's models.

**How to use:**
```bash
# Run training experiments
python ai/train.py

# Run with custom params
python ai/train.py -n 200 -d 8 -lr 0.1

# Open MLflow UI
mlflow ui
```

Then open http://localhost:5000 to compare experiments.

### v2.0 — Groq Migration & Bug Fixes

**Upgrades:**
- **RAG backend migrated from LM Studio to Groq** — No longer requires a local LLM server. Uses Groq's free-tier API with `llama-3.3-70b-versatile` for fast, cloud-hosted inference. Embeddings remain local via sentence-transformers.
- **Dashboard + Chat split UI** for the AI Assistant — Settings panel on the left (engine config, role selector, knowledge base path), chat interface on the right with welcome screen and suggestion prompts.
- **Role-based system prompts** — Maintenance Engineer (technical/evidence-based), Field Monitoring Worker (plain-language with traffic-light indicators), General User (high-level summaries).
- **Prediction input validation** — All sensor inputs now have min/max bounds matching the training data distribution, preventing garbage predictions from out-of-range values.
- **Realistic default sensor values** — Inputs default to training-data means instead of `100.0`, giving meaningful predictions on first use.

**Bug Fixes:**
- Fixed `sqlite3.Row` / pandas `DataFrame` column-name mismatch — `pd.read_sql_query` was returning integer column indices instead of named columns, causing empty tables in Maintenance Records, Reports, and History pages.
- Added `get_pandas_connection()` for all pandas queries to avoid conflicts with the dict-based row factory.
- Fixed prediction always returning ~31 RUL — caused by all sensor inputs defaulting to `100.0`, which is hundreds of standard deviations outside the training range.
- Fixed SHAP explanation crash with thinking models — bumped `max_tokens` from `400` to `4096` to accommodate Gemma-4's internal reasoning tokens (now handled by Groq's inference).

**Observations:**
- Groq eliminates the need for local GPU inference — anyone with an API key can run the RAG assistant on any machine.
- The local FAISS index + sentence-transformers embeddings ensure search quality stays the same; only the text generation layer moved to the cloud.
- Input bounds on the prediction page prevent users from accidentally breaking the model with nonsensical values — a common issue with XGBoost models trained on normalized sensor data.

## License

This project was developed for educational purposes under the Digital Egypt Pioneers Initiative (DEPI).
