# 🍷 Wine Quality Prediction — End-to-End ML Project

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-API-green)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Containerised-blue)](https://docker.com)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)](https://github.com/features/actions)
[![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-red)](https://mlflow.org)

## 🔗 Links
- **Live Application:**  https://datascienceproject2-9cuu.onrender.com
- **GitHub Repository:** https://github.com/korede-folarin/Wine-Quality-Prediction-End-to-End-ML-Project.git 

---

##  Project Overview

A production-ready end-to-end machine learning pipeline that predicts the quality of red wine based on its physicochemical properties. Built following industry-standard MLOps practices with a modular layered architecture, automated CI/CD, and a live deployed Flask API.

---

##  Architecture

The project follows a strict layered architecture where each layer has one responsibility:

```
Entity Layer       → Typed dataclasses that hold configuration per stage
Config Layer       → Reads YAML files and returns typed config objects
Component Layer    → Individual workers that perform the actual ML tasks
Pipeline Layer     → Coordinates components in the correct order
Entry Point        → main.py triggers all stages sequentially
```

---

##  ML Pipeline Stages

| Stage | Component | Input | Output |
|-------|-----------|-------|--------|
| 1. Data Ingestion | Downloads and extracts data | GitHub URL | winequality-red.csv |
| 2. Data Validation | Checks columns against schema | CSV + schema.yaml | status.txt |
| 3. Data Transformation | Scales features, splits data | CSV | train.csv + test.csv |
| 4. Model Training | Trains ElasticNet model | train.csv | model.joblib |
| 5. Model Evaluation | Evaluates and logs metrics | test.csv + model | metrics.json + MLflow |

---

##  Dataset

- **Source:** Wine Quality Dataset (Red Wine)
- **Total rows:** 1,599
- **Features:** 11 physicochemical properties
- **Target:** Quality score (integer)
- **Train split:** 1,199 rows (75%)
- **Test split:** 400 rows (25%)

**Features include:**
fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol

---

##  Model

- **Algorithm:** ElasticNet Regression
- **Why ElasticNet:** Wine features are correlated. L2 penalty handles correlated features by shrinking weights evenly. L1 penalty removes irrelevant features by zeroing their weights. ElasticNet combines both.
- **Hyperparameters:** alpha=0.2, l1_ratio=0.1 (stored in params.yaml)
- **Saved as:** model.joblib using joblib

---

##  Project Structure

```
DATASCIENCEPROJECT2/
│
├── config/config.yaml          → WHERE: all paths and settings
├── params.yaml                 → HOW: model hyperparameters  
├── schema.yaml                 → WHAT: column names and types
├── main.py                     → ENTRY: runs all pipeline stages
├── app.py                      → FLASK: serves predictions as API
├── Dockerfile                  → DOCKER: containerises for deployment
├── requirement.txt             → PACKAGES: all dependencies
│
├── src/datascience/
│   ├── __init__.py             → Logging setup
│   ├── constant/               → File path constants
│   ├── entity/config_entity.py → Config dataclasses per stage
│   ├── utils/common.py         → Shared utility functions
│   ├── config/configuration.py → ConfigurationManager
│   ├── components/             → One worker per stage
│   └── pipeline/               → One coordinator per stage
│
└── artifacts/                  → Created at runtime
    ├── data_ingestion/         → Raw data
    ├── data_validation/        → Validation status
    ├── data_transformation/    → Train and test CSVs
    └── model_trainer/          → Trained model
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| config.yaml | WHERE — all file paths and directory locations |
| params.yaml | HOW — model hyperparameters (alpha, l1_ratio) |
| schema.yaml | WHAT — expected column names, types, target column |

Separating configuration from code means hyperparameters and paths can be changed without touching Python files.

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| scikit-learn | ML model (ElasticNet) |
| pandas | Data manipulation |
| Flask | REST API for serving predictions |
| Flask-Cors | Cross-origin request handling |
| joblib | Model serialisation |
| MLflow | Experiment tracking and metric logging |
| Docker | Containerisation |
| GitHub Actions | CI/CD automation |
| Render | Cloud deployment |
| PyYAML | Configuration file parsing |
| python-box | Dot notation config access |
| ensure | Runtime type validation |

---

##  How to Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/korede-folarin/DATASCIENCEPROJECT2.git
cd DATASCIENCEPROJECT2
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirement.txt
```

**4. Run the full pipeline:**
```bash
python main.py
```

**5. Start the Flask API:**
```bash
python app.py
```

**6. Make a prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [7.4, 0.70, 0.00, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]}'
```

---

##  CI/CD Pipeline

Every push to the main branch automatically triggers:

```
1. Install dependencies
2. Run full ML pipeline (python main.py)
3. Build Docker image
4. Push to DockerHub
5. Deploy to Render
```

Configured via `.github/workflows/main.yaml`

---

##  MLflow Experiment Tracking

The model evaluation stage logs the following to MLflow after every training run:

- **Parameters:** alpha, l1_ratio
- **Metrics:** RMSE, MAE, R2 Score
- **Artifact:** Trained model

This allows comparing different runs and reproducing the best model.

---

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home page |
| POST | /predict | Returns wine quality prediction |

**Request body:**
```json
{
  "features": [7.4, 0.70, 0.00, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]
}
```

**Response:**
```json
{
  "prediction": 5
}
```

---

##  Key Design Decisions

**Why YAML configuration files?**
Keeps settings completely outside code. Data scientists change params.yaml to tune the model. DevOps engineers change config.yaml for deployment paths. Neither touches the other's files.

**Why ElasticNet over Ridge or Lasso?**
Wine features are correlated. Ridge handles correlated features but keeps all of them. Lasso removes irrelevant ones but can randomly drop correlated features. ElasticNet uses both — L2 for correlation, L1 for irrelevance.

**Why the layered architecture?**
Each component has one responsibility. Changing the model only touches model_trainer.py. Changing the data source only touches data_ingestion.py and config.yaml. Easy to debug, test and extend.

**Why Docker?**
Solves the works on my machine problem. The container runs identically on any server — same Python version, same packages, guaranteed consistency.

---

##  Author

**Korede Folarin**
- GitHub: [@korede-folarin](https://github.com/korede-folarin)

---

*Built as a demonstration of end-to-end MLOps practices — from raw data to live deployed API.*