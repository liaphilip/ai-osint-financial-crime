import json

from ai.ai_analyzer import analyze_findings
from ai.risk_scoring import calculate_risk


def main():

    print("=" * 50)
    print("AI-ASSISTED OSINT FINANCIAL CRIME INVESTIGATION")
    print("=" * 50)

    # Load OSINT data
    with open("data/sample_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Analyze findings
    findings, observations = analyze_findings(data)

    # Calculate risk
    risk = calculate_risk(findings)

    print("\nCOMPANY")
    print("-------")
    print(data["company"]["name"])

    print("\nAI OBSERVATIONS")
    print("----------------")

    for observation in observations:
        print("-", observation)

    print("\nRISK ASSESSMENT")
    print("---------------")
    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])

    print("\nRED FLAGS")
    print("---------")

    for flag in risk["red_flags"]:
        print("-", flag)

    print("\nNOTE:")
    print(
        "This score is a heuristic investigative indicator "
        "and is not proof of fraud."
    )


if __name__ == "__main__":
    main()