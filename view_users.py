"""
Script to view all registered users in the database
"""

import sqlite3
from datetime import datetime
from tabulate import tabulate

DATABASE_URL = "voting_system.db"

def view_all_users():
    """Display all registered users"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query all users
        cursor.execute("""
            SELECT 
                id,
                full_name,
                email,
                roll_number,
                role,
                is_active,
                created_at,
                updated_at
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("\n❌ No users found in the database\n")
            return
        
        # Prepare data for table
        table_data = []
        for user in users:
            table_data.append([
                user['id'],
                user['full_name'],
                user['email'],
                user['roll_number'],
                user['role'],
                '✅ Yes' if user['is_active'] else '❌ No',
                user['created_at'][:19],
                user['updated_at'][:19]
            ])
        
        # Display table
        headers = ["ID", "Name", "Email", "Roll Number", "Role", "Active", "Created", "Updated"]
        print("\n" + "="*150)
        print(f"📊 REGISTERED USERS ({len(users)} total)")
        print("="*150)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("="*150 + "\n")
        
        # Show OTP status for each user
        print("\n📧 OTP VERIFICATION STATUS:")
        print("="*80)
        for user in users:
            cursor.execute("""
                SELECT COUNT(*) as total_otps,
                       SUM(CASE WHEN is_verified = 1 THEN 1 ELSE 0 END) as verified_otps
                FROM otps
                WHERE user_id = ?
            """, (user['id'],))
            otp_stats = cursor.fetchone()
            
            status = "✅ Verified" if otp_stats['verified_otps'] and otp_stats['verified_otps'] > 0 else "⏳ Pending"
            print(f"  {user['full_name']:30} | OTPs: {otp_stats['total_otps']:3} | Verified: {otp_stats['verified_otps'] or 0:3} | Status: {status}")
        
        print("="*80 + "\n")
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"\n❌ Database error: {e}")
        print(f"Make sure the database file exists at: {DATABASE_URL}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

def view_user_votes():
    """Display voting records"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                v.id,
                u.full_name,
                u.email,
                e.title as election,
                c.name as candidate,
                v.created_at
            FROM votes v
            JOIN users u ON v.user_id = u.id
            JOIN elections e ON v.election_id = e.id
            JOIN candidates c ON v.candidate_id = c.id
            ORDER BY v.created_at DESC
        """)
        
        votes = cursor.fetchall()
        
        if not votes:
            print("\n❌ No votes found in the database\n")
            return
        
        # Prepare data
        table_data = []
        for vote in votes:
            table_data.append([
                vote['id'],
                vote['full_name'],
                vote['email'],
                vote['election'],
                vote['candidate'],
                vote['created_at'][:19]
            ])
        
        headers = ["Vote ID", "Voter Name", "Email", "Election", "Candidate", "Timestamp"]
        print("\n" + "="*130)
        print(f"🗳️  VOTING RECORDS ({len(votes)} total votes)")
        print("="*130)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("="*130 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

def view_user_details(email):
    """View details of a specific user"""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"\n❌ User with email '{email}' not found\n")
            return
        
        print("\n" + "="*60)
        print(f"👤 USER DETAILS")
        print("="*60)
        print(f"ID:              {user['id']}")
        print(f"Name:            {user['full_name']}")
        print(f"Email:           {user['email']}")
        print(f"Roll Number:     {user['roll_number']}")
        print(f"Role:            {user['role']}")
        print(f"Active:          {'Yes' if user['is_active'] else 'No'}")
        print(f"Created:         {user['created_at']}")
        print(f"Updated:         {user['updated_at']}")
        
        # Get OTP history
        cursor.execute("""
            SELECT * FROM otps WHERE user_id = ? ORDER BY created_at DESC
        """, (user['id'],))
        otps = cursor.fetchall()
        
        print(f"\nOTP History: {len(otps)} requests")
        if otps:
            for otp in otps:
                status = "✅ Verified" if otp['is_verified'] else "⏳ Pending"
                print(f"  - {otp['created_at'][:19]} | Code: {otp['otp_code']} | {status}")
        
        # Get voting history
        cursor.execute("""
            SELECT v.*, e.title, c.name 
            FROM votes v
            JOIN elections e ON v.election_id = e.id
            JOIN candidates c ON v.candidate_id = c.id
            WHERE v.user_id = ?
        """, (user['id'],))
        votes = cursor.fetchall()
        
        print(f"\nVoting History: {len(votes)} votes")
        if votes:
            for vote in votes:
                print(f"  - {vote['created_at'][:19]} | {vote['title']} → {vote['name']}")
        
        print("="*60 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    print("\n🔐 College Voting System - Database Viewer")
    print("="*80)
    
    while True:
        print("\nOptions:")
        print("  1. View all users")
        print("  2. View voting records")
        print("  3. View specific user details")
        print("  4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_user_votes()
        elif choice == "3":
            email = input("Enter user email: ").strip()
            view_user_details(email)
        elif choice == "4":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid option. Please try again.")
