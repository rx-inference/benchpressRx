# PURPOSE: SUPERVISOR LLM EVALUATION MODULE

# === IMPORTS ===
import requests
import json
import time

# === RESPONSE EVALUATION ===
def evaluate_response(question, solution, response, model_name="qwen3:4b", timeout=60):
    """evaluate model response using supervisor LLM"""
    # Format prompt
    prompt = f"""
[system]
You are an AI benchmark supervisor. Evaluate if the model's response correctly answers the question based on the provided solution.

[input]
QUESTION: {question}
EXPECTED SOLUTION: {solution}
MODEL RESPONSE: {response}

[output]
Provide JSON with:
- "pass": true/false
- "rating": 0.0-1.0 scale
- "commentary": brief explanation
"""
    
    # Call Ollama API
    try:
        api_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=timeout
        )
        api_response.raise_for_status()
        
        # Parse JSON response
        result = api_response.json()
        return json.loads(result["response"])
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Supervisor evaluation failed: {e}")
        return {
            "pass": False,
            "rating": 0.0,
            "commentary": "Evaluation error"
        }