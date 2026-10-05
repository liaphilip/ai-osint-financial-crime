import json
import os

from openai import OpenAI


def analyze_with_llm(data, observations):
    """
    Optional LLM analysis.

    If an API key is unavailable or the API has no credits,
    the project continues using the rule-based analysis.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("\nLLM analysis unavailable - using rule-based analysis.")
        return None

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are assisting with an academic OSINT investigation.

Analyze ONLY the information provided below.

Do not claim that an organization is fraudulent or criminal.
Identify inconsistencies, suspicious indicators, and areas
that require further verification.

OSINT DATA:
{json.dumps(data, indent=2)}

RULE-BASED OBSERVATIONS:
{json.dumps(observations, indent=2)}

Provide:

1. Key findings
2. Potential inconsistencies
3. Why the indicators matter
4. Recommended verification steps
5. A short neutral conclusion

Clearly distinguish observed facts from investigative leads.
"""

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
            input=prompt
        )

        return response.output_text

    except Exception:
        print("\nLLM analysis unavailable.")
        print("Continuing with rule-based analysis.")

        return None


if __name__ == "__main__":
    print("LLM analyzer module ready.")