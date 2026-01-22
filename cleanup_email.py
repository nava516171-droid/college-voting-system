#!/usr/bin/env python
"""
Clean up hardcoded email addresses from database
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User

DATABASE_URL = "sqlite:///voting_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cleanup_emails():
    """Remove or anonymize hardcoded email addresses"""
    
    print("\n" + "="*70)
    print("EMAIL CLEANUP UTILITY")
    print("="*70 + "\n")
    
    db = SessionLocal()
    
    try:
        # Find records with these emails
        emails_to_remove = ["nava990699@gmail.com", "navanavaneeth1305@gmail.com"]
        
        for email in emails_to_remove:
            users = db.query(User).filter(User.email == email).all()
            
            if users:
                print(f"\n[!] Found {len(users)} record(s) with email: {email}")
                for user in users:
                    print(f"    - ID: {user.id}, Name: {user.full_name}, Email: {user.email}")
                    # Delete the user
                    db.delete(user)
                    print(f"    ✓ Deleted user ID {user.id}")
        
        # Commit changes
        db.commit()
        print("\n✓ All records cleaned up successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_emails()
    print("\n" + "="*70)
    print("CLEANUP COMPLETE")
    print("="*70 + "\n")
