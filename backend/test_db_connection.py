#!/usr/bin/env python3
"""
Test PostgreSQL connection with exact same parameters as the application
"""
import psycopg2
import os
from urllib.parse import urlparse

# Test the exact connection string from .env - both IPv4 and IPv6
connection_strings = [
    "postgresql://kairocal_user:Test123@127.0.0.1:5432/kairocal",  # IPv4 explicitly
    "postgresql://kairocal_user:Test123@localhost:5432/kairocal"   # Default (might use IPv6)
]

for i, DATABASE_URL in enumerate(connection_strings, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: Testing connection to: {DATABASE_URL}")
    print("="*60)

    try:
        # Parse the URL
        parsed = urlparse(DATABASE_URL)
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"Database: {parsed.path[1:]}")  # Remove leading slash
        print(f"Username: {parsed.username}")
        print(f"Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
        print("-" * 50)
        
        # Test connection
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Version: {version[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nExisting tables: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        print("✅ Connection test completed successfully!")
        break  # Exit loop on first success
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify credentials")  
        print("3. Check network connectivity")
        print("4. Review authentication method (md5 vs scram-sha-256)")
        
        if i == len(connection_strings):
            print(f"\n❌ All {len(connection_strings)} connection attempts failed!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if i == len(connection_strings):
            print(f"\n❌ All {len(connection_strings)} connection attempts failed!")
