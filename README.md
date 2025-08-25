# NorthScore Pipeline

Central ETL pipeline for NorthScore that automates the ingestion, transformation, and loading of U SPORTS and CCAA data from Canadian university and college sports — includes GitHub Actions workflows for scheduled script execution.

Built using the [usports](https://github.com/ojadeyemi/usports) package for data extraction.

## ⚙️ Requirements
- Python 3.12+
- PostgreSQL (or compatible)

## 📦 Setup

1. **Clone the repository:**

```bash
git clone https://github.com/ojadeyemi/northscore-pipeline.git
cd northscore-pipeline
```

2. **Set Environment Variables:**

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

- `LOG_LEVEL`: Debug level for logging
- `PYTHONPATH`: Ensures Python can locate modules within the project
- `DATABASE_URL`: Connection string for the PostgreSQL database (required for database operations)

3. **Install Dependencies:**

```bash
poetry install
```

## ⚡ Usage

**Fetch data locally (stores CSV files in data/ folder):**
```bash
poetry run python scripts/fetch_all_usports_data.py
```

**Update database (requires PostgreSQL setup):**
```bash
poetry run python scripts/update_all_usports_db.py
```

## 🔍 Code Quality

Run pylint with the project's configuration:

```bash
poetry run pylint --rcfile=.pylintrc scripts/
```
