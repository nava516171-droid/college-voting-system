"""Update user password using bcrypt"""

import sqlite3
from bcrypt import hashpw, gensalt

DATABASE = "voting_system.db"
EMAIL = "prgadarsh@gmail.com"
NEW_PASSWORD = "nag123"

def update_password():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Hash the new password using bcrypt
    hashed_password = hashpw(NEW_PASSWORD.encode(), gensalt()).decode()
    
    # Update the user
    cursor.execute("""
        UPDATE users 
        SET hashed_password = ? 
        WHERE email = ?
    """, (hashed_password, EMAIL))
    
    conn.commit()
    
    # Verify the update
    cursor.execute("SELECT id, full_name, email FROM users WHERE email = ?", (EMAIL,))
    user = cursor.fetchone()
    
    if user:
        print("\n" + "="*70)
        print("✅ PASSWORD UPDATED SUCCESSFULLY")
        print("="*70)
        print(f"User ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"New Password: {NEW_PASSWORD}")
        print("="*70 + "\n")
    else:
        print(f"\n❌ User with email '{EMAIL}' not found\n")
    
    conn.close()

if __name__ == "__main__":
    update_password()
