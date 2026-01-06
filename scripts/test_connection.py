#!/usr/bin/env python3
"""
Simple Snowflake connection test script.
Run this to verify your Snowflake credentials before running the full pipeline.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test connection to Snowflake."""
    print("=" * 60)
    print("Snowflake Connection Test")
    print("=" * 60)

    # Check if required environment variables are set
    required_vars = [
        'SNOWFLAKE_ACCOUNT',
        'SNOWFLAKE_USER',
        'SNOWFLAKE_PASSWORD',
        'SNOWFLAKE_ROLE',
        'SNOWFLAKE_WAREHOUSE'
    ]

    print("\n1. Checking environment variables...")
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
            print(f"   ❌ {var}: Not configured")
        else:
            # Mask password
            display_value = '*' * 8 if var == 'SNOWFLAKE_PASSWORD' else value
            print(f"   ✓ {var}: {display_value}")

    if missing_vars:
        print(f"\n⚠️  Please configure these variables in your .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nRefer to README.md for instructions on finding your Snowflake account identifier.")
        return False

    print("\n2. Testing Snowflake connection...")
    try:
        import snowflake.connector

        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            role=os.getenv('SNOWFLAKE_ROLE'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
        )

        print("   ✓ Successfully connected to Snowflake!")

        # Get some basic info
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION(), CURRENT_ACCOUNT(), CURRENT_REGION()")
        version, account, region = cursor.fetchone()

        print(f"\n3. Connection Details:")
        print(f"   - Snowflake Version: {version}")
        print(f"   - Account: {account}")
        print(f"   - Region: {region}")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("✓ Connection test successful!")
        print("=" * 60)
        print("\nYou can now run: python scripts/data_ingestion.py")
        return True

    except snowflake.connector.errors.HttpError as e:
        print(f"   ❌ HTTP Error: {e}")
        print("\n⚠️  Common causes:")
        print("   - Incorrect account identifier format")
        print("   - Check your SNOWFLAKE_ACCOUNT in .env")
        print("   - Refer to README.md Step 3 for correct format")
        return False

    except snowflake.connector.errors.DatabaseError as e:
        print(f"   ❌ Database Error: {e}")
        print("\n⚠️  Common causes:")
        print("   - Incorrect username or password")
        print("   - User doesn't have access to the warehouse")
        print("   - Role doesn't exist or user doesn't have it")
        return False

    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
