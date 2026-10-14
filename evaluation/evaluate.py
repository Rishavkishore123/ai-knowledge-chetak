
import json
from pathlib import Path

import httpx


API_URL = "http://127.0.0.1:8000/ask"
QUESTIONS_FILE = Path(__file__).with_name("questions.json")


def main():
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    passed = 0

    with httpx.Client(timeout=60) as client:
        for item in questions:
            response = client.post(
                API_URL,
                json={"question": item["question"]},
            )
            response.raise_for_status()
            result = response.json()

            answer = result["answer"].lower()
            sources = result["sources"]

            if item["answerable"]:
                expected = item["expected"]
                terms = expected if isinstance(expected, list) else [expected]
                success = (
                    all(term.lower() in answer for term in terms)
                    and bool(sources)
                    and all(source.get("excerpt") for source in sources)
                )
            else:
                success = (
                    result["found_evidence"] is False
                    and not sources
                    and (
                        "not contain enough information" in answer
                        or "unavailable" in answer
                    )
                )

            passed += int(success)
            print(
                f"{'PASS' if success else 'FAIL'}: "
                f"{item['question']}\n"
                f"  Answer: {result['answer']}"
            )

    print(f"\nEvaluation: {passed}/{len(questions)} passed")


if __name__ == "__main__":
    main()
