import sqlite3
import chromadb
import os
from datetime import datetime

# SQLite setup
DB_PATH = "memory.db"

def init_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            role TEXT,
            preferred_tone TEXT,
            notes TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER,
            timestamp TEXT,
            text TEXT,
            platform TEXT,
            direction TEXT,
            FOREIGN KEY (contact_id) REFERENCES contacts (id)
        )
    ''')
    conn.commit()
    conn.close()

# ChromaDB setup
CHROMA_PATH = "./chroma_store"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="semantic_memory")

def save_interaction(user, text, platform):
    # Ensure contact exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO contacts (name) VALUES (?)", (user,))
    cursor.execute("SELECT id FROM contacts WHERE name = ?", (user,))
    contact_id = cursor.fetchone()[0]
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO interactions (contact_id, timestamp, text, platform, direction) VALUES (?, ?, ?, ?, ?)",
                   (contact_id, timestamp, text, platform, "incoming"))  # Assume incoming for now
    conn.commit()
    conn.close()

    # Add to ChromaDB
    collection.add(
        documents=[text],
        metadatas=[{"user": user, "platform": platform, "timestamp": timestamp}],
        ids=[f"{user}_{timestamp}"]
    )

def get_profile(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, role, preferred_tone, notes FROM contacts WHERE name = ?", (user,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "role": row[1], "preferred_tone": row[2], "notes": row[3]}
    return None

def search_semantic_memory(query):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results

# Initialize on import
init_sqlite()