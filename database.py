# PURPOSE: DATABASE INITIALIZATION AND MANAGEMENT

# --- SQLITE SETUP ---
import sqlite3
import os

def init_db():
    """initialize database connection and create schema"""
    db_path = 'benchpressRx.db'
    schema_exists = os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if not schema_exists:
        cursor.execute('''
            CREATE TABLE benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_domain TEXT NOT NULL,
                test_question TEXT NOT NULL,
                test_solution TEXT NOT NULL,
                unit_response TEXT,
                supervisor_instruction TEXT,
                supervisor_commentary TEXT,
                supervisor_pass BOOLEAN,
                supervisor_rating REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    
    return conn

# --- DATABASE UTILITIES ---
def insert_run(conn, run_data):
    """insert benchmark run into database"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO benchmark_runs (
            test_domain, test_question, test_solution,
            unit_response, supervisor_instruction,
            supervisor_commentary, supervisor_pass, supervisor_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', run_data)
    conn.commit()
    return cursor.lastrowid

def get_runs(conn, domain=None):
    """retrieve benchmark runs from database"""
    query = 'SELECT * FROM benchmark_runs'
    params = ()
    
    if domain:
        query += ' WHERE test_domain = ?'
        params = (domain,)
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()