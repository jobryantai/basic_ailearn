import psycopg2
import json
from pathlib import Path

# ==========================
# DATABASE CONFIG
# ==========================
DB_PARAMS = {
    "host": "127.0.0.1",
    "dbname": "postgres",      # your current database
    "user": "postgres",        # owner of tables
    "password": "YourPostgresPassword"
}

# Use a relative folder for output (e.g., 'output' subfolder)
output_folder = Path.cwd() / "output"
output_folder.mkdir(exist_ok=True)  # create folder if it doesn't exist
OUTPUT_JSONL = output_folder / "ollama_training.jsonl"

# ==========================
# EXPORT DATA FROM DATABASE
# ==========================
def export_training_data():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # Fetch paragraphs with context
    cur.execute("""
    SELECT b.title, c.title, s.title, p.content
    FROM paragraphs p
    JOIN sections s ON p.section_id = s.section_id
    JOIN chapters c ON s.chapter_id = c.chapter_id
    JOIN books b ON c.book_id = b.book_id
    ORDER BY b.book_id, c.chapter_index, s.section_index, p.chunk_index;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Write to JSONL
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for book_title, chapter_title, section_title, paragraph_text in rows:
            record = {
                "prompt": f"Book: {book_title} | Chapter: {chapter_title} | Section: {section_title}\nParagraph:",
                "completion": paragraph_text
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Exported {len(rows)} paragraphs to {OUTPUT_JSONL}")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    export_training_data()
