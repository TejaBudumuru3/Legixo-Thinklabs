import json
import requests
import time
import os

PATH = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(PATH, 'test_cases.json')
def run_eval():
    with open(FILE, 'r') as f:
        test_cases = json.load(f)

    url = "http://127.0.0.1:8000/ask"

    print(f"loaded {len(test_cases)} test cases to test")

    for case in test_cases:
        print(f"Running Test ID: {case['id']}")
        try:
            response = requests.post(url=url, json={
                "question": case['question']
            })
            response.raise_for_status()

            data = response.json()
            case['actual_answer'] = data['answer']
            case['actual_citations'] = data['citations']
            case['trace'] = data['trace']

        except Exception as e:
            print(f"Error calling API for ID {case['id']}: {e}")
            case["error"] = str(e)

    output_file = os.path.join(PATH, "test_results.json")
    with open(output_file, "w") as f:
        json.dump(test_cases, f, indent=2)

    print(f"\nDone! All results successfully saved to {output_file}")


if __name__ == "__main__":
    run_eval()