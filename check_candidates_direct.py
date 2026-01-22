"""Check candidates in database"""

import sqlite3

def check_candidates():
    conn = sqlite3.connect("voting_system.db")
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("📋 CANDIDATES IN DATABASE")
    print("="*80)
    
    try:
        cursor.execute("""
            SELECT id, name, election_id, symbol_number, description
            FROM candidates
            ORDER BY id
        """)
        
        candidates = cursor.fetchall()
        
        if not candidates:
            print("\n❌ No candidates found in database")
            print("\nExpected candidates:")
            print("  - DINESH RANGAPPA")
            print("  - RAMESH")
            print("  - NIRMALA HIREMANI")
        else:
            print(f"\nTotal Candidates: {len(candidates)}\n")
            for candidate in candidates:
                cid, name, elec_id, symbol, desc = candidate
                print(f"ID: {cid}")
                print(f"Name: {name}")
                print(f"Election ID: {elec_id}")
                print(f"Symbol Number: {symbol}")
                print(f"Description: {desc}")
                print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    check_candidates()
