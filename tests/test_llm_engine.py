import time
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from llm_engine import extract_context

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

def run_context_tests():
    print("Running LLM context tests...")
    results = []
    
    for i, test in enumerate(TEST_CASES):
        print(f"Testing {test['id']}...")
        t0 = time.time()
        try:
            analysis = extract_context(test["text"])
            latency = time.time() - t0
            status = "Success"
            data = analysis.model_dump()
        except ValueError as e:
            latency = time.time() - t0
            status = f"Validation/Parsing Error: {str(e)}"
            data = None
            
        results.append({
            "test_case": test["id"],
            "input": test["text"],
            "latency": latency,
            "status": status,
            "data": data
        })
        
    write_report(results)
    print("Done! Report written to docs/phase4-context-test.md")

def write_report(results):
    os.makedirs("docs", exist_ok=True)
    passed = sum(1 for r in results if r["status"] == "Success")
    failed = len(results) - passed
    
    with open("docs/phase4-context-test.md", "w") as f:
        f.write("# Phase 4 LLM Engine Test Report\n\n")
        f.write(f"**Tests Passed**: {passed}/{len(results)}\n")
        f.write(f"**Tests Failed**: {failed}/{len(results)}\n\n")
        
        for r in results:
            f.write(f"### Test: {r['test_case']}\n")
            f.write(f"**Input**: `{r['input']}`\n")
            f.write(f"**Latency**: {r['latency']:.2f}s\n")
            f.write(f"**Status**: {r['status']}\n")
            if r['data']:
                f.write("**Validated Output**:\n```json\n")
                f.write(json.dumps(r['data'], indent=2))
                f.write("\n```\n")
            f.write("---\n\n")

if __name__ == "__main__":
    run_context_tests()
