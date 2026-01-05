# End-to-End Snowflake Pipeline with CI/CD

This project demonstrates a complete data pipeline that ingests data into Snowflake, manages transformations using dbt (Data Build Tool), and implements automated CI/CD practices.

## Tech Stack

- **Snowflake**: Cloud data warehouse for data storage and processing
- **dbt**: Data transformation tool for SQL-based transformations
- **GitHub Actions**: CI/CD automation platform
- **Python**: Scripting for data ingestion
- **SQL**: Data querying and transformations

## Architecture

```
Raw Data → Snowflake → dbt Transformations → Analytics Views
     ↑              ↓
  Ingestion    Data Quality Tests
     ↑              ↓
GitHub Actions → CI/CD Pipeline
```

## Key Features

- **Automated Data Ingestion**: Python scripts to load data into Snowflake
- **dbt Transformations**: SQL-based data modeling with staging and marts layers
- **Data Quality Tests**: Automated validation rules for data integrity
- **CI/CD Pipeline**: GitHub Actions workflow with PR testing and automated deployment
- **Environment Management**: Separate dev and prod environments

## File structure

```
master/
├── .github/workflows/           # CI/CD workflows
├── models/                      # dbt models
│   ├── staging/                 # Raw data staging models
│   └── marts/                   # Business-ready views
├── scripts/                     # Data ingestion scripts
│   └── data_ingestion.py        # Python ingestion script
├── .env.example                 # Environment variables template
├── dbt_project.yml             # dbt configuration
├── profiles.yml                # dbt connection profiles
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

- Snowflake account with appropriate permissions
- Python 3.9+
- GitHub repository (for CI/CD)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd snowflake-pipeline
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Snowflake credentials
   ```

5. Set up dbt profile:
   ```bash
   cp profiles.yml ~/.dbt/profiles.yml
   # Edit with your Snowflake credentials
   ```

### Data Ingestion

Run the data ingestion script:
```bash
python scripts/data_ingestion.py
```

### dbt Transformations

Run dbt commands:
```bash
# Install dependencies
dbt deps

# Run tests
dbt test

# Run transformations
dbt run
```

### CI/CD Setup

1. Add Snowflake secrets to GitHub repository:
   - `SNOWFLAKE_ACCOUNT`
   - `SNOWFLAKE_USER`
   - `SNOWFLAKE_PASSWORD`
   - `SNOWFLAKE_ROLE`
   - `SNOWFLAKE_DATABASE`
   - `SNOWFLAKE_WAREHOUSE`

2. The CI/CD pipeline will:
   - Run tests on every push and PR
   - Deploy to production on successful main branch merge
   - Validate dbt model syntax

## Data Quality & Testing

This project includes:
- **Schema Tests**: Not null, unique, accepted values
- **Data Validation**: Business logic checks
- **CI Testing**: Automated validation on code changes

## License

This project is licensed under the MIT License.
