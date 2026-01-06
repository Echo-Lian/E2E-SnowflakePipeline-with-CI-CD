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

## File Structure

```
E2E❄️Pipeline/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions CI/CD workflow
├── models/
│   ├── sources.yml             # dbt source definitions
│   ├── staging/
│   │   ├── schema.yml          # Staging model tests and docs
│   │   └── stg_customers.sql   # Staging customer model
│   └── marts/
│       └── customer_summary.sql # Customer analytics view
├── scripts/
│   └── data_ingestion.py       # Python data ingestion script
├── .env.example                # Environment variables template
├── .env                        # Your environment variables (DO NOT COMMIT)
├── .gitignore                  # Git ignore file
├── dbt_project.yml             # dbt project configuration
├── profiles.yml                # dbt connection profiles (DO NOT COMMIT)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- **Snowflake Account**: Active Snowflake account with credentials
- **Python**: Version 3.11 or higher
- **Git**: For version control
- **GitHub Account**: For CI/CD (optional)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd E2E-SnowflakePipeline-with-CI-CD
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Snowflake Credentials

#### Find Your Snowflake Account Identifier

Your Snowflake account identifier format depends on when your account was created:

**Modern Format** (accounts created after Nov 2020):
- Format: `<orgname>-<account_name>`
- Example: `myorg-myaccount`
- Find it in: Snowflake UI → Account dropdown (bottom left)

**Legacy Format** (older accounts):
- Format: `<account_locator>.<region>.<cloud>`
- Example: `xy12345.us-east-1.aws` or `xy12345.us-east-2.azure`
- Find it: Snowflake UI → Account → Account Locator

To find your account identifier:
1. Log into Snowflake web UI
2. Look at the URL: `https://<account_identifier>.snowflakecomputing.com`
3. Copy everything before `.snowflakecomputing.com`

#### Configure .env File

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Update `.env` with your Snowflake credentials:

```bash
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your-account-identifier  # e.g., orgname-accountname or xy12345.us-east-1.aws
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=your_role                   # e.g., ACCOUNTADMIN, SYSADMIN
SNOWFLAKE_DATABASE=DEMO_DB                 # Database name (will be created)
SNOWFLAKE_WAREHOUSE=your_warehouse         # Warehouse name
SNOWFLAKE_SCHEMA=DEV                       # Schema for dev environment
```

**Note**: The `profiles.yml` file is already configured to use environment variables from `.env`.

### Step 3.5: Test Your Connection (Optional but Recommended)

Before running the full pipeline, test your Snowflake connection:

```bash
python scripts/test_connection.py
```

This will verify:
- All required environment variables are set
- Your Snowflake credentials are correct
- You can successfully connect to Snowflake
- Display your account and region information

If the test fails, it will provide specific guidance on what to fix.

### Step 4: Run Data Ingestion

The data ingestion script will:
- Connect to your Snowflake account
- Create database `DEMO_DB` and schema `RAW_DATA`
- Create a `CUSTOMERS` table
- Load 100 sample customer records

```bash
# Make sure your virtual environment is activated
# Run the ingestion script using the correct Python version
./venv/bin/python3.14 scripts/data_ingestion.py

# Or if python3.14 is not available, use:
python scripts/data_ingestion.py
```

Expected output:
```
INFO - Starting data ingestion process
INFO - Successfully connected to Snowflake
INFO - Tables created successfully
INFO - Successfully loaded 100 rows into customers
INFO - Data ingestion completed successfully
```

### Step 5: Run dbt Transformations

dbt will create staging and analytics models based on the raw data:

```bash
# Test connection to Snowflake
dbt debug

# Run all models
dbt run

# Run tests
dbt test

# Generate and serve documentation (optional)
dbt docs generate
dbt docs serve
```

Expected output:
```
Running with dbt=1.11.2
Registered adapter: snowflake=1.11.0
Found 2 models, 0 tests, 0 sources, 0 exposures, 0 metrics, ...

Completed successfully
```

### Step 6: Verify the Results

Log into your Snowflake account and run:

```sql
-- Check the raw data
SELECT * FROM DEMO_DB.RAW_DATA.CUSTOMERS LIMIT 10;

-- Check the staging model (ephemeral, won't appear as table)
-- View the marts model
SELECT * FROM DEMO_DB.DEV.CUSTOMER_SUMMARY;
```

The `CUSTOMER_SUMMARY` view shows:
- Customer count by region
- Average days since signup
- Customer density category (High/Medium/Low)

## Detailed Component Guide

### Data Ingestion Script

Located in `scripts/data_ingestion.py`, this script:
- Generates sample customer data (ID, name, email, region, signup date)
- Connects to Snowflake using credentials from `.env`
- Creates necessary database and schema structures
- Loads data using Snowflake's `write_pandas` function
- Includes error handling and logging

### dbt Models

#### Source Definition (`models/sources.yml`)
```yaml
sources:
  - name: raw_data
    database: DEMO_DB
    schema: RAW_DATA
    tables:
      - name: customers
```

#### Staging Model (`models/staging/stg_customers.sql`)
- Materialized as ephemeral (not persisted)
- Casts data types explicitly
- Adds `loaded_at` timestamp

#### Marts Model (`models/marts/customer_summary.sql`)
- Materialized as view
- Aggregates customers by region
- Calculates metrics and categorizes regions

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automatically:
1. **On Pull Request**: Runs dbt tests
2. **On Merge to Main**: Deploys to production

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution**: Ensure virtual environment is activated and packages are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "404 Not Found: post <account>.snowflakecomputing.com"

**Cause**: Incorrect account identifier format in `.env`

**Solutions**:
1. Verify your account identifier format (see Step 3 above)
2. Common fixes:
   - Try format: `orgname-accountname`
   - Try format: `account_locator.region.cloud`
   - Example: `xy12345.us-east-1.aws`

3. Test connection manually:
```python
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD')
)
print("Connection successful!")
conn.close()
```

### Issue: "Database 'DEMO_DB' does not exist"

**Solution**: The ingestion script creates the database. Run it first:
```bash
python scripts/data_ingestion.py
```

### Issue: "Insufficient privileges to operate on database 'DEMO_DB'"

**Solution**: Your Snowflake role needs these privileges:
```sql
-- Grant necessary privileges (run as ACCOUNTADMIN)
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <your_role>;
GRANT USAGE ON WAREHOUSE <your_warehouse> TO ROLE <your_role>;
```

### Issue: dbt can't connect

**Solution**:
1. Verify `profiles.yml` uses environment variables
2. Test with `dbt debug`
3. Check that `.env` file is in the project root
4. Ensure dbt is using the correct profile:
```bash
dbt debug --profiles-dir .
```

## CI/CD Setup (GitHub Actions)

### Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
SNOWFLAKE_ACCOUNT=your-account-identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_DATABASE=DEMO_DB
SNOWFLAKE_WAREHOUSE=your_warehouse
```

### Workflow Features

The CI/CD pipeline automatically:
- Installs dependencies
- Runs dbt tests on PRs
- Deploys to dev environment on main branch
- Can be extended for production deployments

## Next Steps

1. **Add More Data Sources**: Extend `data_ingestion.py` to load from CSV, APIs, or databases
2. **Create More Models**: Add transformations in `models/staging/` and `models/marts/`
3. **Add Data Tests**: Define tests in `schema.yml` files
4. **Set Up Production**: Configure prod target in `profiles.yml`
5. **Schedule Runs**: Use GitHub Actions schedule or Snowflake tasks

## Resources

- [Snowflake Documentation](https://docs.snowflake.com)
- [dbt Documentation](https://docs.getdbt.com)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Snowflake Account Identifiers](https://docs.snowflake.com/en/user-guide/admin-account-identifier.html)

## License

This project is licensed under the MIT License.
