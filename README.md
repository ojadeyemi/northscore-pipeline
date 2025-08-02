# NorthScore Pipeline

Central ETL pipeline for NorthScore that automates the ingestion, transformation, and loading of U SPORTS and CCAA data from Canadian university and college sports — includes GitHub Actions workflows for scheduled script execution.

## ⚙️ Requirements
- Python 3.12+
- PostgreSQL (or compatible)
- Optional: Redis / Prefect (if using orchestration)

## 📦 Setup

1. **Clone the repository:**

```bash
git clone https://github.com/ojadeyemi/northscore-pipeline.git
cd northscore-pipeline
```

2. **Set Environment Variables:**

```bash
export PYTHONPATH=./
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

- `PYTHONPATH=./`: Ensures Python can locate modules within the project. This is needed when running scripts directly instead of through a package.
- `DATABASE_URL`: Connection string for the PostgreSQL database.

3. **Install Dependencies:**

```bash
poetry install
```

## ⚡ Usage

```bash
poetry run python scripts/fetch_all_data.py
poetry run python scripts/update_all_db.py
```
