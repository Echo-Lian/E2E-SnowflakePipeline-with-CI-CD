#!/usr/bin/env python3
"""
Data ingestion script for Snowflake pipeline.
This script loads sample data into Snowflake and demonstrates the ingestion process.
"""

import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_connection():
    """Create Snowflake connection using environment variables."""
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            role=os.getenv('SNOWFLAKE_ROLE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA', 'DEV')
        )
        logger.info("Successfully connected to Snowflake")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {str(e)}")
        raise


def create_sample_data():
    """Generate sample data for demonstration."""
    import datetime
    import random

    customers = []
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']
    regions = ['North America', 'Europe', 'Asia', 'Australia']

    for i in range(100):
        customer = {
            'customer_id': i + 1,
            'customer_name': f'Customer_{i+1}',
            'email': f'customer{i+1}@example.com',
            'region': random.choice(regions),
            'signup_date': datetime.date.today() - pd.Timedelta(days=random.randint(0, 365))
        }
        customers.append(customer)

    return pd.DataFrame(customers)


def create_tables(conn):
    """Create necessary tables in Snowflake."""
    with conn.cursor() as cursor:
        # Create database and schema if not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS DEMO_DB")
        cursor.execute("USE DATABASE DEMO_DB")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS RAW_DATA")

        # Create customers table
        cursor.execute("""
            CREATE OR REPLACE TABLE RAW_DATA.CUSTOMERS (
                CUSTOMER_ID INTEGER,
                CUSTOMER_NAME VARCHAR(100),
                EMAIL VARCHAR(100),
                REGION VARCHAR(50),
                SIGNUP_DATE DATE
            )
        """)

        logger.info("Tables created successfully")


def load_data(conn, df, table_name):
    """Load data into Snowflake table."""
    try:
        # Write the data to the table
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table_name.upper(),
            schema='RAW_DATA',
            database='DEMO_DB',
            auto_create_table=False,
            overwrite=True
        )

        if success:
            logger.info(f"Successfully loaded {nrows} rows into {table_name}")
        else:
            logger.error(f"Failed to load data into {table_name}")

        return success

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def main():
    """Main function to orchestrate data ingestion."""
    logger.info("Starting data ingestion process")

    # Create sample data
    df_customers = create_sample_data()

    try:
        # Create Snowflake connection
        conn = create_connection()

        # Create tables
        create_tables(conn)

        # Load data
        load_data(conn, df_customers, 'customers')

        logger.info("Data ingestion completed successfully")

    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()
