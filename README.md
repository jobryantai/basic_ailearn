# PDF Processing & Ollama Pipeline

This repository contains a pipeline for processing PDFs, storing structured book data in PostgreSQL, exporting training data to JSONL, and testing questions using the Ollama Python SDK. It is fully portable and uses relative paths for all input/output.

---

## 📁 Folder Structure

project-root/
│
├─ pdf/ # Place your PDF files here
├─ output/ # Auto-generated output (JSONL, logs)
├─ process_pdfs.py # PDF → DB processing
├─ export_jsonl.py # DB → JSONL export
├─ test_model.py # Test Ollama model using JSONL
├─ ask_questions.py # Ask exam-style questions using Ollama
└─ README.md


> Note: `output/` is ignored in `.gitignore` to prevent large files from being pushed.

---

## 🛠️ Prerequisites

1. **Python 3.9+**  
2. **PostgreSQL** with the database and tables:
    - `books`
    - `chapters`
    - `sections`
    - `paragraphs`  

3. **Python packages**:

```bash
pip install psycopg2-binary pdfminer.six ollama
Ollama Local Model (example: codellama:34b) installed.

1️⃣ Process PDFs
Script: process_pdfs.py

Reads PDFs from pdf/ folder.

Splits text into books → chapters → sections → paragraphs.

Inserts all data into PostgreSQL.

Uses relative paths and avoids hardcoding.

Run:

python process_pdfs.py
2️⃣ Export JSONL for Ollama Training
Script: export_jsonl.py

Extracts structured paragraphs from PostgreSQL.

Writes a JSONL file in output/ollama_training.jsonl.

Each record has a prompt (book/chapter/section) and completion (paragraph content).

Run:

python export_jsonl.py
3️⃣ Test Ollama Model Responses
Script: test_model.py

Loads the JSONL training file from output/.

Sends prompts to Ollama model (codellama:34b) to test responses.

Compares output with expected paragraph completion.

Run:

python test_model.py
4️⃣ Ask Exam-Style Questions
Script: ask_questions.py

Loads JSONL as context.

Combines prompt + completion into context for Ollama.

Sends example exam questions to the model.

Prints Ollama answers to console.

Run:

python ask_questions.py
⚡ Notes
All scripts use relative paths (pdf/ and output/) to ensure portability.

output/ folder is auto-created if it doesn’t exist.

Use .gitignore to exclude output/ files and avoid pushing large datasets.

Modify DB_PARAMS in scripts to match your PostgreSQL setup.

Example exam questions are included in ask_questions.py and can be customized.

🔗 GitHub Setup
Initialize Git:

git init
git add .
git commit -m "Initial commit of PDF-Ollama pipeline"
Create a repository on GitHub, then push:

git remote add origin https://github.com/<USERNAME>/<REPO>.git
git branch -M main
git push -u origin main
✅ Summary of Scripts
Script	Purpose
process_pdfs.py	Parse PDFs → PostgreSQL
export_jsonl.py	Export paragraphs from DB → JSONL
test_model.py	Test Ollama model with JSONL prompts
ask_questions.py	Ask exam-style questions using Ollama
📌 Author / Maintainer
