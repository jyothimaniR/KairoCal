#!/usr/bin/env python3
"""
Test PostgreSQL connection using container IP
"""
import psycopg2

# Test with container IP
DATABASE_URL = "postgresql://kairocal_user:Test123@172.18.0.3:5432/kairocal"

print(f"Testing connection to container IP: {DATABASE_URL}")
print("-" * 50)

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_user, version();")
    result = cursor.fetchone()
    print(f"Connected as: {result[0]}")
    print(f"PostgreSQL Version: {result[1]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
