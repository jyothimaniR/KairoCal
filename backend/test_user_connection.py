#!/usr/bin/env python3
"""
Test PostgreSQL connection with test user
"""
import psycopg2

# Test with the new test user
DATABASE_URL = "postgresql://kairocal_test:Test123@127.0.0.1:5432/kairocal"

print(f"Testing connection to: {DATABASE_URL}")
print("-" * 50)

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful with kairocal_test user!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_user, version();")
    result = cursor.fetchone()
    print(f"Connected as: {result[0]}")
    print(f"PostgreSQL Version: {result[1]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
