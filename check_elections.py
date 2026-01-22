"""Check elections and candidates in database"""

import sqlite3

conn = sqlite3.connect("voting_system.db")
cursor = conn.cursor()

print("\n" + "="*80)
print("📊 ELECTIONS IN DATABASE")
print("="*80)

cursor.execute("SELECT id, title, description FROM elections")
elections = cursor.fetchall()

if not elections:
    print("❌ No elections found")
else:
    print(f"\nTotal Elections: {len(elections)}\n")
    for election in elections:
        print(f"ID: {election[0]} | {election[1]}")
        print(f"   Description: {election[2]}\n")

print("\n" + "="*80)
print("🎯 CANDIDATES IN DATABASE")
print("="*80)

cursor.execute("SELECT id, name, election_id FROM candidates")
candidates = cursor.fetchall()

if not candidates:
    print("❌ No candidates found")
else:
    print(f"\nTotal Candidates: {len(candidates)}\n")
    for candidate in candidates:
        print(f"ID: {candidate[0]} | Name: {candidate[1]} | Election ID: {candidate[2]}")

print("\n" + "="*80 + "\n")

conn.close()
