import json
from pathlib import Path
import ollama  # Python SDK

# ==========================
# CONFIG
# ==========================
# Use relative 'output' folder to store training JSONL
output_folder = Path.cwd() / "output"
output_folder.mkdir(exist_ok=True)  # ensure folder exists
JSONL_FILE = output_folder / "ollama_training.jsonl"

MODEL_NAME = "codellama:34b"  # your local model

# ==========================
# LOAD TRAINING DATA
# ==========================
def load_training_data():
    if not JSONL_FILE.exists():
        raise FileNotFoundError(f"Training JSONL not found at {JSONL_FILE}")

    training_data = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            training_data.append(record)

    print(f"Loaded {len(training_data)} paragraphs from JSONL")
    return training_data

# ==========================
# RUN TEST QUERIES
# ==========================
def test_model(training_data, num_tests=5):
    print("\n--- Running test queries ---")
    for i, record in enumerate(training_data[:num_tests]):
        prompt = record["prompt"]
        completion = record["completion"]

        # Ollama chat returns plain string directly
        resp_text = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        print(f"\nPrompt:\n{prompt}\n")
        print(f"Ollama Response:\n{resp_text}\n")
        print(f"Expected Completion (preview 200 chars):\n{completion[:200]}...")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    data = load_training_data()
    test_model(data)
