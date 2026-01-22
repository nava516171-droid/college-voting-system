import sqlite3

try:
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("✓ Database: voting_system.db")
    print("✓ Tables Found:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} records")
    
    # Check candidates specifically
    cursor.execute("SELECT id, candidate_name FROM candidate LIMIT 3")
    candidates = cursor.fetchall()
    print("\n✓ Sample Candidates:")
    for cand in candidates:
        print(f"  - {cand[1]} (ID: {cand[0]})")
    
    conn.close()
    print("\n✓ Database Status: HEALTHY")
    
except Exception as e:
    print(f"✗ Database Error: {str(e)}")
