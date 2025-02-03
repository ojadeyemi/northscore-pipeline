# Canada Sports Usports Pipeline

A private data pipeline for automating the fetching, validation, and updating of Usports data into the database.

## ⚙️ Requirements

- Python 3.12+
- PostgreSQL (or compatible database)

## 📦 Setup

1. **Clone the repository:**

```bash
git clone https://github.com/ojadeyemi/canada-sports-usports-pipeline.git
cd canada-sports-usports-pipeline
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

## 🗓️ Cron Job Example

```bash
0 */6 * 9-12,1-4 * cd /path/to/project && poetry run python scripts/fetch_all_data.py >> logs/fetch.log 2>&1

5 */6 * 9-12,1-4 * cd /path/to/project && poetry run python scripts/update_all_db.py >> logs/update.log 2>&1
```
