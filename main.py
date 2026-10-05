import json

from ai.ai_analyzer import analyze_findings
from ai.risk_scoring import calculate_risk
from graph.investigation_graph import build_graph


def main():

    print("=" * 60)
    print("AI-ASSISTED OSINT FINANCIAL CRIME INVESTIGATION")
    print("=" * 60)

    # Load OSINT data
    with open("data/sample_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    company = data["company"]["name"]

    print(f"\nInvestigating: {company}")

    # -------------------------
    # AI-assisted analysis
    # -------------------------
    findings, observations = analyze_findings(data)

    print("\n[1] OSINT ANALYSIS")
    print("-" * 30)

    if observations:
        for observation in observations:
            print("•", observation)
    else:
        print("No major inconsistencies detected.")

    # -------------------------
    # Risk scoring
    # -------------------------
    risk = calculate_risk(findings)

    print("\n[2] RISK ASSESSMENT")
    print("-" * 30)
    print("Risk Score :", risk["risk_score"], "/ 100")
    print("Risk Level :", risk["risk_level"])

    # -------------------------
    # Red flags
    # -------------------------
    print("\n[3] RED FLAGS")
    print("-" * 30)

    if risk["red_flags"]:
        for flag in risk["red_flags"]:
            print("⚠", flag)
    else:
        print("No red flags detected.")

    # -------------------------
    # Investigation graph
    # -------------------------
    graph = build_graph(data)

    print("\n[4] INVESTIGATION GRAPH")
    print("-" * 30)
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    print("\nInvestigation completed.")

    print("\nNOTE:")
    print(
        "The risk score is a heuristic investigative indicator "
        "and does not establish fraud or criminal activity."
    )


if __name__ == "__main__":
    main()