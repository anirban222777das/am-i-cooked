import json
import time
import psutil
from pydantic import BaseModel, ValidationError
from typing import List
from mlx_lm import load, generate

class ContextExtraction(BaseModel):
    category: str
    urgency: int
    preparation: int
    consequences: int
    recoverability: int
    time_remaining: str
    key_factors: List[str]
    explicit_facts: List[str]
    uncertainties: List[str]

TEST_CASES = [
    {
        "id": "1_basic",
        "text": "I have an exam tomorrow and haven't studied anything."
    },
    {
        "id": "2_nuance",
        "text": "I have an exam tomorrow. I've studied about 80% of the material, but I haven't reviewed the final chapter."
    },
    {
        "id": "3_slang",
        "text": "bro exam tmrw 💀 haven't touched the book"
    },
    {
        "id": "4_sarcasm",
        "text": "Yeah I'm totally prepared for tomorrow's exam. Haven't opened the book once."
    },
    {
        "id": "5_multiple",
        "text": "My interview is tomorrow. I've prepared for the technical questions, but I haven't researched the company and I haven't practiced speaking answers."
    },
    {
        "id": "6_ambiguous",
        "text": "Things aren't looking good 💀"
    },
    {
        "id": "7_contradiction",
        "text": "I've studied everything for tomorrow's exam, but I haven't studied anything."
    },
    {
        "id": "8_different_category",
        "text": "I spent almost my entire salary three days after getting paid."
    },
    {
        "id": "9_short",
        "text": "bro 💀"
    },
    {
        "id": "10_grounding",
        "text": "I spent my salary in three days."
    }
]

SYSTEM_PROMPT = """You are an objective context extraction engine. Your job is to read the user's text and extract the context into a strictly validated JSON structure.
You must NOT invent facts. Only use explicit information provided by the user. If something is unknown, leave it blank or add it to uncertainties.

Schema requirements:
- category: one of [academic, career, financial, relationship, coding, deadline, personal, other]
- urgency: integer 0-10 (how soon it matters)
- preparation: integer 0-10 (how prepared they are)
- consequences: integer 0-10 (how bad it is based ONLY on provided facts)
- recoverability: integer 0-10 (how recoverable it is)
- time_remaining: string (e.g. 'tomorrow', 'unknown')
- key_factors: list of concise strings representing the most critical factors
- explicit_facts: list of undeniable facts directly stated by the user
- uncertainties: list of things that are unclear or contradictory

Output ONLY valid JSON. No markdown, no explanations, no chain of thought."""

def measure_memory():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 * 1024)
    return mem

def run_tests():
    results = []
    
    print("Loading model...")
    t0 = time.time()
    model, tokenizer = load("models/qwen3-4b")
    load_time = time.time() - t0
    print(f"Model loaded in {load_time:.2f}s. Memory usage: {measure_memory():.2f} MB")
    
    for i, test in enumerate(TEST_CASES):
        print(f"\nRunning test {test['id']}...")
        
        prompt = f"{SYSTEM_PROMPT}\n\nUser Text: {test['text']}\nJSON Output:\n"
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        t1 = time.time()
        output = generate(model, tokenizer, prompt=formatted_prompt, max_tokens=300)
        latency = time.time() - t1
        
        print(f"Latency: {latency:.2f}s")
        
        # Clean output
        clean_out = output.strip()
        if clean_out.startswith("```json"):
            clean_out = clean_out[7:-3]
        elif clean_out.startswith("```"):
            clean_out = clean_out[3:-3]
            
        try:
            data = json.loads(clean_out)
            validated = ContextExtraction(**data)
            status = "Success"
        except (json.JSONDecodeError, ValidationError) as e:
            validated = None
            status = f"Validation Error: {str(e)}"
            
        results.append({
            "test_case": test["id"],
            "input": test["text"],
            "latency": latency,
            "raw_output": output,
            "status": status,
            "validated_data": validated.model_dump() if validated else None
        })
        
    return load_time, results

def write_report(load_time, results):
    import os
    os.makedirs("docs", exist_ok=True)
    
    passed = sum(1 for r in results if r["status"] == "Success")
    failed = len(results) - passed
    
    with open("docs/qwen3-context-test.md", "w") as f:
        f.write("# Qwen3 4B Context Extraction Test Report\n\n")
        f.write(f"**Model Load Time**: {load_time:.2f}s\n")
        f.write(f"**Tests Passed**: {passed}/{len(results)}\n")
        f.write(f"**Tests Failed**: {failed}/{len(results)}\n\n")
        
        f.write("## Test Results\n\n")
        for r in results:
            f.write(f"### Test: {r['test_case']}\n")
            f.write(f"**Input**: `{r['input']}`\n")
            f.write(f"**Latency**: {r['latency']:.2f}s\n")
            f.write(f"**Status**: {r['status']}\n")
            f.write("**Raw Output**:\n```json\n")
            f.write(r['raw_output'])
            f.write("\n```\n")
            if r['validated_data']:
                f.write("**Validated Output**:\n```json\n")
                f.write(json.dumps(r['validated_data'], indent=2))
                f.write("\n```\n")
            f.write("---\n\n")

if __name__ == "__main__":
    load_time, results = run_tests()
    write_report(load_time, results)
    print("Report written to docs/qwen3-context-test.md")
