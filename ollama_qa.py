import json
from pathlib import Path
import ollama

# ==========================
# CONFIG
# ==========================
# Use relative 'output' folder to store training JSONL
output_folder = Path.cwd() / "output"
output_folder.mkdir(exist_ok=True)  # ensure folder exists
JSONL_FILE = output_folder / "ollama_training.jsonl"

MODEL_NAME = "codellama:34b"

# ==========================
# LOAD CONTEXT
# ==========================
def load_context():
    if not JSONL_FILE.exists():
        raise FileNotFoundError(f"Training JSONL not found at {JSONL_FILE}")

    context = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            # Combine prompt + completion as context for Ollama
            text = f"{record['prompt']} {record['completion']}"
            context.append(text)

    print(f"Loaded {len(context)} context paragraphs")
    return context

# ==========================
# ASK EXAM QUESTION
# ==========================
def ask_question(question, context):
    # Combine all context into a single string
    context_text = "\n\n".join(context)

    # Create the prompt for Ollama
    full_prompt = f"Use the following biology content to answer the question:\n\n{context_text}\n\nQuestion: {question}\nAnswer:"

    # Call Ollama
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": full_prompt}]
    )

    print("\n--- QUESTION ---")
    print(question)
    print("\n--- OLLAMA ANSWER ---")
    print(response)

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    context_data = load_context()

    # Example exam questions
    questions = [
        "Explain the role of the cell membrane.",
        "What are the main steps of photosynthesis?",
        "Describe the difference between mitosis and meiosis."
    ]

    for q in questions:
        ask_question(q, context_data)
