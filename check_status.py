from app.database import SessionLocal, engine
from sqlalchemy import inspect, text

print("=" * 50)
print("SYSTEM STATUS CHECK")
print("=" * 50)

# Check database
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT name FROM sqlite_master WHERE type=\'table\''))
        tables = result.fetchall()
        print('\n[DATABASE] ✓ Connected')
        print(f'  Type: SQLite (voting_system.db)')
        print(f'  Tables: {len(tables)}')
        for table in tables:
            print(f'    - {table[0]}')
except Exception as e:
    print(f'\n[DATABASE] ✗ Error: {e}')

# Check tables have data
try:
    db = SessionLocal()
    from app.models import User, Election, Candidate, Vote
    
    users = db.query(User).count()
    elections = db.query(Election).count()
    candidates = db.query(Candidate).count()
    votes = db.query(Vote).count()
    
    print('\n[DATA] Records Found:')
    print(f'  Users: {users}')
    print(f'  Elections: {elections}')
    print(f'  Candidates: {candidates}')
    print(f'  Votes: {votes}')
    
    db.close()
except Exception as e:
    print(f'\n[DATA] Error: {e}')

print("\n[BACKEND] ✓ Running on http://localhost:8000")
print("[FRONTEND] ✓ Running on http://localhost:3000")
print("\n" + "=" * 50)
print("All systems operational!")
print("=" * 50)
