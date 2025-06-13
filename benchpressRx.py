# PURPOSE: MAIN LLM BENCHMARKING APPLICATION

# === IMPORTS ===
import database
import time
import json
import requests
from benchpressRx_supervisor import evaluate_response

# === CONFIGURATION ===
CONFIG = {
    "ollama_url": "http://localhost:11434",
    "benchmarked_model": "gemma3:1b",
    "supervisor_model": "qwen3:4b",
    "benchmark_questions": "questions.json",
    "timeout": 60  # seconds
}

# === MODEL INTERFACE ===
def get_model_response(question):
    """get response from model under test via Ollama"""
    try:
        response = requests.post(
            f"{CONFIG['ollama_url']}/api/generate",
            json={
                "model": CONFIG["benchmarked_model"],
                "prompt": question,
                "stream": False
            },
            timeout=CONFIG["timeout"]
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Model request failed: {e}")
        return ""

# === BENCHMARK RUNNER ===
def run_benchmark():
    """main benchmark execution workflow"""
    conn = database.init_db()
    
    # Load benchmark questions
    with open(CONFIG["benchmark_questions"]) as f:
        questions = json.load(f)
    
    # Process each question
    for domain, question, solution in questions:
        print(f"Processing: {domain} - {question[:50]}...")
        
        # Get model response
        print("  Getting model response...")
        response = get_model_response(question)
        
        # Evaluate with supervisor
        print("  Evaluating response...")
        evaluation = evaluate_response(question, solution, response)
        
        # Save to database
        run_data = (
            domain, question, solution, response,
            evaluation.get("instruction", ""),
            evaluation.get("commentary", ""),
            evaluation.get("pass", False),
            evaluation.get("rating", 0.0)
        )
        database.insert_run(conn, run_data)
        print("  Saved results")
    
    print("Benchmark completed successfully")

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    print("Starting benchmark...")
    start_time = time.time()
    run_benchmark()
    print(f"Total time: {time.time() - start_time:.2f} seconds")