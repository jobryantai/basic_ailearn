import psycopg2
from pathlib import Path
from pdfminer.high_level import extract_text

# ==========================
# DATABASE CONNECTION SETUP
# ==========================
DB_PARAMS = {
    "host": "127.0.0.1",
    "dbname": "postgres",
    "user": "postgres",
    "password": "YourPostgresPassword"
}

# ==========================
# UTILITY FUNCTIONS
# ==========================
def get_conn():
    """Return a new connection (stateless)."""
    return psycopg2.connect(**DB_PARAMS)

def chunk_text(text, max_len=500):
    """Split text into chunks of roughly max_len words."""
    words = text.split()
    for i in range(0, len(words), max_len):
        yield " ".join(words[i:i+max_len])

# ==========================
# DATABASE INSERT FUNCTIONS
# ==========================
def insert_book(cur, title, author=None, edition=None, source_file=None):
    cur.execute("""
        INSERT INTO books (title, author, edition, source_file)
        VALUES (%s, %s, %s, %s)
        RETURNING book_id;
    """, (title, author, edition, source_file))
    return cur.fetchone()[0]

def insert_chapter(cur, book_id, title, chapter_index):
    cur.execute("""
        INSERT INTO chapters (book_id, title, chapter_index)
        VALUES (%s, %s, %s)
        RETURNING chapter_id;
    """, (book_id, title, chapter_index))
    return cur.fetchone()[0]

def insert_section(cur, chapter_id, title, section_index):
    cur.execute("""
        INSERT INTO sections (chapter_id, title, section_index)
        VALUES (%s, %s, %s)
        RETURNING section_id;
    """, (chapter_id, title, section_index))
    return cur.fetchone()[0]

def insert_paragraph(cur, section_id, content, chunk_index):
    cur.execute("""
        INSERT INTO paragraphs (section_id, content, chunk_index)
        VALUES (%s, %s, %s)
        RETURNING paragraph_id;
    """, (section_id, content, chunk_index))
    return cur.fetchone()[0]

# ==========================
# PDF PROCESSING
# ==========================
def process_pdf(pdf_path):
    """Stateless PDF processing: books → chapters → sections → paragraphs"""
    text = extract_text(pdf_path)
    chapters = [c.strip() for c in text.split("Chapter") if c.strip()]

    conn = get_conn()
    cur = conn.cursor()

    # Insert book
    book_id = insert_book(cur, title=Path(pdf_path).stem, source_file=str(pdf_path))

    for chap_idx, chap_text in enumerate(chapters, start=1):
        chapter_id = insert_chapter(cur, book_id, title=f"Chapter {chap_idx}", chapter_index=chap_idx)
        sections = [s.strip() for s in chap_text.split("Section") if s.strip()]

        for sec_idx, sec_text in enumerate(sections, start=1):
            section_id = insert_section(cur, chapter_id, title=f"Section {sec_idx}", section_index=sec_idx)

            # Insert paragraphs
            for chunk_idx, paragraph in enumerate(chunk_text(sec_text), start=1):
                insert_paragraph(cur, section_id, paragraph, chunk_idx)

    conn.commit()
    cur.close()
    conn.close()
    print(f"Processed PDF: {pdf_path}, Book ID: {book_id}")

# ==========================
# RUN PIPELINE
# ==========================
if __name__ == "__main__":
    # Relative folder path from current working directory
    pdf_folder = Path.cwd() / "pdf"  # looks for a 'pdf' subfolder in the current directory
    pdf_folder.mkdir(exist_ok=True)  # ensure folder exists

    pdf_files = [f for f in pdf_folder.glob("*.pdf")]

    for pdf_file in pdf_files:
        try:
            process_pdf(pdf_file)
        except Exception as e:
            print(f"Skipped {pdf_file} due to error: {e}")
