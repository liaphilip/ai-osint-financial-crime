from integration.person3_adapter import run_person3_osint
from ai.ai_analyzer import analyze_findings
from ai.risk_scoring import calculate_risk
from ai.llm_analyzer import analyze_with_llm
from graph.investigation_graph import (
    build_graph,
    visualize_graph
)
from integration.data_loader import load_investigation_cases
from reports.report_generator import generate_report


def main():

    print("=" * 60)
    print("AI-ASSISTED OSINT FINANCIAL CRIME INVESTIGATION")
    print("=" * 60)

    cases = load_investigation_cases()

    if not cases:
        print("No investigation cases found.")
        return

    print(f"\nCases loaded: {len(cases)}")

    for data in cases:

        case_id = data.get("case_id", "unknown")

        company = data.get(
            "company",
            {}
        ).get(
            "name",
            "Unknown"
        )

        print("\n" + "=" * 60)
        print(f"CASE: {case_id}")
        print(f"Investigating: {company}")
        print("=" * 60)

        # -------------------------
        # AI-assisted analysis
        # -------------------------

        findings, observations = analyze_findings(data)

                # -------------------------
        # Person 3 Identity/Social OSINT
        # -------------------------

        person3_result = run_person3_osint(data)

        print("\n[1.2] IDENTITY & SOCIAL OSINT")
        print("-" * 30)

        print("Status:", person3_result["status"])
        print("Reason:", person3_result["reason"])

        print("\n[1] OSINT ANALYSIS")
        print("-" * 30)

        for observation in observations:
            print("•", observation)

        # Optional LLM.
        # If unavailable, rule-based analysis continues.
        llm_analysis = analyze_with_llm(
            data,
            observations
        )

        if llm_analysis:

            print("\n[1.5] LLM-ASSISTED ANALYSIS")
            print("-" * 30)
            print(llm_analysis)

        # -------------------------
        # Risk scoring
        # -------------------------

        risk = calculate_risk(findings)

        print("\n[2] RISK ASSESSMENT")
        print("-" * 30)

        print(
            "Risk Score:",
            risk["risk_score"],
            "/ 100"
        )

        print(
            "Risk Level:",
            risk["risk_level"]
        )

        # -------------------------
        # Red flags
        # -------------------------

        print("\n[3] RED FLAGS")
        print("-" * 30)

        if risk["red_flags"]:

            for flag in risk["red_flags"]:
                print("⚠", flag)

        else:
            print("No rule-based red flags detected.")

        # -------------------------
        # Investigation graph
        # -------------------------

        graph = build_graph(data)

        print("\n[4] INVESTIGATION GRAPH")
        print("-" * 30)

        print(
            "Nodes:",
            graph.number_of_nodes()
        )

        print(
            "Edges:",
            graph.number_of_edges()
        )

        graph_path = (
            f"output/{case_id}_investigation_graph.png"
        )

        visualize_graph(
            graph,
            graph_path
        )

        print(
            "Graph saved:",
            graph_path
        )

        # -------------------------
        # Report
        # -------------------------

        generate_report(
            data,
            observations,
            risk,
            graph
        )

    print("\n" + "=" * 60)
    print("ALL INVESTIGATIONS COMPLETED")
    print("=" * 60)

    print(
        "\nNOTE:\n"
        "Risk scores are heuristic investigative indicators "
        "and do not establish fraud or criminal activity."
    )


if __name__ == "__main__":
    main()