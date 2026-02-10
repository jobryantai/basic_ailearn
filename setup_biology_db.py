import psycopg2
from psycopg2 import sql

# ==========================
# CONFIGURATION
# ==========================
DB_NAME = "postgres"       # database where tables will live
DB_USER = "postgres"       # user with privileges
DB_PASSWORD = "YourPostgresPassword"  # replace with your password
DB_HOST = "127.0.0.1"
DB_PORT = 5432

# ==========================
# TABLE DEFINITIONS
# ==========================
TABLES = {
    "books": """
        CREATE TABLE IF NOT EXISTS books (
            book_id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            edition TEXT,
            source_file TEXT,
            metadata JSONB DEFAULT '{}'::JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "chapters": """
        CREATE TABLE IF NOT EXISTS chapters (
            chapter_id SERIAL PRIMARY KEY,
            book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "sections": """
        CREATE TABLE IF NOT EXISTS sections (
            section_id SERIAL PRIMARY KEY,
            chapter_id INT REFERENCES chapters(chapter_id) ON DELETE CASCADE,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "paragraphs": """
        CREATE TABLE IF NOT EXISTS paragraphs (
            paragraph_id SERIAL PRIMARY KEY,
            section_id INT REFERENCES sections(section_id) ON DELETE CASCADE,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "figures": """
        CREATE TABLE IF NOT EXISTS figures (
            figure_id SERIAL PRIMARY KEY,
            section_id INT REFERENCES sections(section_id) ON DELETE CASCADE,
            caption TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "tables": """
        CREATE TABLE IF NOT EXISTS tables (
            table_id SERIAL PRIMARY KEY,
            section_id INT REFERENCES sections(section_id) ON DELETE CASCADE,
            caption TEXT,
            table_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
}

# ==========================
# DATABASE SETUP
# ==========================
def setup_database():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create each table
    for name, ddl in TABLES.items():
        print(f"Creating table {name}...")
        cur.execute(ddl)

    print("All tables created successfully.")
    cur.close()
    conn.close()

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    setup_database()
