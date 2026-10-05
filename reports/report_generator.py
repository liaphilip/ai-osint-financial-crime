import json
from datetime import datetime
from pathlib import Path


def generate_report(data, observations, risk, graph):

    company = data["company"]["name"]

    report = []

    report.append("=" * 70)
    report.append("AI-ASSISTED OSINT INVESTIGATION REPORT")
    report.append("=" * 70)

    report.append(f"\nCompany: {company}")
    report.append(f"Domain: {data['company']['domain']}")
    report.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report.append("\n\n1. INVESTIGATION SUMMARY")
    report.append("-" * 40)

    report.append(
        "The investigation correlates publicly available OSINT "
        "findings related to the organization and associated job posting."
    )

    report.append("\n\n2. OSINT OBSERVATIONS")
    report.append("-" * 40)

    if observations:
        for observation in observations:
            report.append(f"- {observation}")
    else:
        report.append("- No major inconsistencies detected.")

    report.append("\n\n3. RISK ASSESSMENT")
    report.append("-" * 40)

    report.append(
        f"Risk Score: {risk['risk_score']}/100"
    )

    report.append(
        f"Risk Level: {risk['risk_level']}"
    )

    report.append("\n\n4. RED FLAGS")
    report.append("-" * 40)

    if risk["red_flags"]:

        for flag in risk["red_flags"]:
            report.append(f"- {flag}")

    else:
        report.append("- No red flags detected.")

    report.append("\n\n5. INVESTIGATION GRAPH")
    report.append("-" * 40)

    report.append(
        f"Nodes identified: {graph.number_of_nodes()}"
    )

    report.append(
        f"Relationships identified: {graph.number_of_edges()}"
    )

    report.append("\n\n6. CONCLUSION")
    report.append("-" * 40)

    report.append(
        "The identified indicators should be treated as leads "
        "for further investigation rather than definitive evidence "
        "of fraud or criminal activity."
    )

    output = "\n".join(report)

    Path("output").mkdir(exist_ok=True)

    with open(
        "output/investigation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(output)

    print("\nReport generated:")
    print("output/investigation_report.txt")

    return output