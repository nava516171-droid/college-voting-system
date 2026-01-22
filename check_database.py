"""Script to verify admin database table"""

import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('voting_system.db')
cursor = conn.cursor()

print("\n" + "="*80)
print("DATABASE VERIFICATION - ADMIN SYSTEM")
print("="*80)

# Check if admins table exists
print("\n1. CHECKING ADMINS TABLE STRUCTURE:")
print("-" * 80)

try:
    cursor.execute("PRAGMA table_info(admins)")
    columns = cursor.fetchall()
    
    if columns:
        print("✅ ADMINS TABLE EXISTS")
        print("\nColumns:")
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            print(f"  • {col_name:20} {col_type:15} PK={pk} NOT_NULL={not_null}")
    else:
        print("❌ ADMINS TABLE NOT FOUND")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check indexes
print("\n2. CHECKING INDEXES:")
print("-" * 80)

try:
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND tbl_name='admins'")
    indexes = cursor.fetchall()
    
    if indexes:
        print("✅ INDEXES FOUND:")
        for idx_name, tbl_name in indexes:
            print(f"  • {idx_name}")
    else:
        print("⚠️  No indexes found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check admin records
print("\n3. CHECKING ADMIN RECORDS:")
print("-" * 80)

try:
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    
    if admins:
        print(f"✅ {len(admins)} ADMIN(S) FOUND:\n")
        
        # Get column names
        cursor.execute("PRAGMA table_info(admins)")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        
        # Display admins
        for idx, admin in enumerate(admins, 1):
            print(f"Admin #{idx}:")
            for col_name, value in zip(col_names, admin):
                if col_name == 'hashed_password':
                    print(f"  • {col_name}: {value[:20]}... (bcrypt hash)")
                elif col_name in ['created_at', 'updated_at']:
                    print(f"  • {col_name}: {value}")
                else:
                    print(f"  • {col_name}: {value}")
            print()
    else:
        print("⚠️  No admin records found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Summary of all tables
print("\n4. DATABASE SUMMARY - ALL TABLES:")
print("-" * 80)

try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    if tables:
        print("\nTables in voting_system.db:")
        for table_name, in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  • {table_name:20} ({count} records)")
    else:
        print("❌ No tables found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Connection details
print("\n5. DATABASE FILE INFO:")
print("-" * 80)

import os
db_path = 'voting_system.db'
if os.path.exists(db_path):
    file_size = os.path.getsize(db_path)
    mod_time = datetime.fromtimestamp(os.path.getmtime(db_path))
    print(f"✅ Database File: {db_path}")
    print(f"  • Size: {file_size:,} bytes")
    print(f"  • Last Modified: {mod_time}")
else:
    print(f"❌ Database File NOT FOUND: {db_path}")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80 + "\n")

conn.close()
