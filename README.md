# 🏠 Avito Real Estate Data Pipeline

A full end-to-end data engineering pipeline for scraping, cleaning, transforming, and analyzing real estate listings from **Avito**. Built with Python, Docker, and a modular layered architecture (Staging → Data Warehouse → BI).

---

## 📁 Project Structure

```
.
├── clean/                    # Data cleaning logic
│   └── clean_data.py         # Cleaning & transformation scripts
│
├── data/                     # Raw & cleaned data files
│   ├── avito_appartements.csv  # Raw scraped listings
│   └── avito_clean.csv         # Cleaned output
│
├── data_werhouse/            # Data warehouse layer
│   ├── bi.py                 # BI/reporting queries
│   ├── db.py                 # Database connection & helpers
│   ├── ml_schema.py          # ML-ready schema definitions
│   └── Untitled-1.ipynb      # Exploratory analysis notebook
│
├── extract/                  # Data extraction / scraping modules
│
├── load_db/                  # SQL scripts for loading data
│   ├── bi_sql.sql            # SQL for BI layer tables
│   └── ml_sql.sql            # SQL for ML layer tables
│
├── staging/                  # Staging layer
│   ├── save_data_db.py       # Save raw data to staging DB
│   └── save_data.py          # Save data to flat files
│
├── main.py                   # Pipeline entry point
├── Dockerfile                # Container definition
├── docker-compose.yml        # Multi-service orchestration
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (not committed)
```

---

## 🔄 Pipeline Architecture

```
[Avito Website]
      │
      ▼
 [extract/]          ← Web scraping
      │
      ▼
 [staging/]          ← Raw data persistence (CSV + DB)
      │
      ▼
 [clean/]            ← Cleaning & normalization
      │
      ▼
 [data_werhouse/]    ← Structured warehouse (BI + ML schemas)
      │
      ▼
 [BI / ML Layer]     ← Reporting, dashboards, model-ready data
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=avito_db
DB_USER=your_user
DB_PASSWORD=your_password
```

### 3. Start with Docker

```bash
docker-compose up --build
```

### 4. Or run locally

```bash
pip install -r requirements.txt
python main.py
```

---

## 🚀 Usage

Run the full pipeline end-to-end:

```bash
python main.py
```

Run individual steps:

```bash
# Scrape raw data
python extract/scraper.py

# Clean and normalize
python clean/clean_data.py

# Load into staging DB
python staging/save_data_db.py

# Load BI / ML schemas
psql -f load_db/bi_sql.sql
psql -f load_db/ml_sql.sql
```

---

## 📊 Data

| File | Description |
|------|-------------|
| `data/avito_appartements.csv` | Raw scraped apartment listings |
| `data/avito_clean.csv` | Cleaned and normalized listings |

### Key fields (after cleaning)

- `title` — Listing title
- `price` — Price in MAD
- `surface` — Area in m²
- `city` / `neighborhood` — Location
- `rooms` — Number of rooms
- `url` — Source URL
- `scraped_at` — Timestamp

---

## 🗄️ Database Schemas

Two SQL schemas are provided under `load_db/`:

- **`bi_sql.sql`** — Optimized for reporting and dashboards (aggregations, fact/dimension tables)
- **`ml_sql.sql`** — Optimized for machine learning (flat, feature-rich table)

---

## 🐳 Docker

The project ships with a `Dockerfile` and `docker-compose.yml` for containerized execution.

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop
docker-compose down
```

---

## 📦 Dependencies

Install all dependencies via:

```bash
pip install -r requirements.txt
```

Key libraries used:

- `requests` / `BeautifulSoup4` — Web scraping
- `pandas` — Data manipulation
- `psycopg2` / `sqlalchemy` — Database connectivity
- `python-dotenv` — Environment variable management

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)
