import sqlite3

def inspect_db():
    conn = sqlite3.connect('data/quiz.db')
    cursor = conn.cursor()
    
    print("--- Quiz Sessions ---")
    cursor.execute("SELECT * FROM quiz_session")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- Violation Logs ---")
    cursor.execute("SELECT * FROM violation_log")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    inspect_db()
