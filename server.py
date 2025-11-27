from mcp.server.fastmcp import FastMCP
import db_manager
import sqlite3
from datetime import datetime

app = FastMCP("Clone MCP")

@app.tool()
def remember_fact(text: str, category: str):
    """Save a fact in semantic vectors with a category."""
    db_manager.collection.add(
        documents=[text],
        metadatas=[{"category": category}],
        ids=[f"fact_{datetime.now().isoformat()}"]
    )
    return "Fact saved."

@app.tool()
def retrieve_context(contact_name: str):
    """Retrieve SQL profile and semantic vectors for a contact."""
    profile = db_manager.get_profile(contact_name)
    # Get interactions
    conn = sqlite3.connect(db_manager.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT text, platform, direction, timestamp
        FROM interactions
        WHERE contact_id = (SELECT id FROM contacts WHERE name = ?)
        ORDER BY timestamp DESC
        LIMIT 10
    """, (contact_name,))
    interactions = cursor.fetchall()
    conn.close()
    # Semantic search
    semantic_results = db_manager.search_semantic_memory(f"conversations with {contact_name}")
    return {
        "profile": profile,
        "interactions": [{"text": i[0], "platform": i[1], "direction": i[2], "timestamp": i[3]} for i in interactions],
        "semantic_memory": semantic_results
    }

@app.tool()
def write_daily_note(text: str):
    """Append a note to the diary.md file."""
    with open("diary.md", "a") as f:
        f.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {text}\n")
    return "Note added to diary."

if __name__ == "__main__":
    app.run()