#!/usr/bin/env python3
"""
Check SQLite database structure
"""
import sqlite3

def check_database_structure():
    """Check what tables and structure exist in the SQLite database"""
    
    db_path = "backend/kairocal_local.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 Found {len(tables)} tables in database:")
        for table in tables:
            print(f"   - {table[0]}")
            
        # Check each table structure
        for table in tables:
            table_name = table[0]
            print(f"\n📊 Structure of table '{table_name}':")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   {col[1]} ({col[2]})")
                
        # If there's an events-like table, show some sample data
        for table in tables:
            table_name = table[0]
            if 'event' in table_name.lower():
                print(f"\n📄 Sample data from '{table_name}' (first 3 rows):")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"   {row}")
                    
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database_structure()
