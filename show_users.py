"""Simple script to display all users from the database"""

import sqlite3

def view_users():
    conn = sqlite3.connect("voting_system.db")
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("📊 REGISTERED USERS IN DATABASE")
    print("="*80)
    
    try:
        cursor.execute("""
            SELECT id, full_name, email, roll_number, is_active, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("❌ No users found\n")
        else:
            print(f"\nTotal Users: {len(users)}\n")
            for user in users:
                user_id, name, email, roll, active, created = user
                status = "✅" if active else "❌"
                print(f"{user_id}. {name:20} | {email:30} | {roll:10} | {status} Active | Created: {created[:10]}")
        
        print("\n" + "="*80 + "\n")
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    view_users()
