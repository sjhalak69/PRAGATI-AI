import sqlite3
from engine import get_audited_data

def setup_database():
    # This creates a file named 'mplad_scheme.db' in your project folder
    conn = sqlite3.connect("mplad_scheme.db")
    cursor = conn.cursor()
    
    # Create the schema table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        Project_ID TEXT PRIMARY KEY,
        Asset_Type TEXT,
        Sanctioned_Amount INTEGER,
        Spent_Amount INTEGER,
        Days_Delayed INTEGER,
        Status TEXT
    )
    """)
    
    # Populate it with your simulated AI-audited data
    df = get_audited_data()
    
    # Insert data rows into the SQL table
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO projects (Project_ID, Asset_Type, Sanctioned_Amount, Spent_Amount, Days_Delayed, Status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (row['Project_ID'], row['Asset_Type'], int(row['Sanctioned_Amount']), int(row['Spent_Amount']), int(row['Days_Delayed']), row['Status']))
        
    conn.commit()
    conn.close()
    print("✅ Local SQLite Database 'mplad_scheme.db' initialized successfully!")

if __name__ == "__main__":
    setup_database()
