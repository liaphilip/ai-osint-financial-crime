import json
from pathlib import Path


def analyze_findings(data):
    """
    Analyze OSINT findings and identify potential inconsistencies.
    This does not determine that an organization is fraudulent.
    """

    findings = {
        "recent_domain": False,
        "email_mismatch": False,
        "address_mismatch": False,
        "unverified_recruiter": False,
        "suspicious_social": False,
        "infrastructure_mismatch": False
    }

    observations = []

    # Domain analysis
    for domain in data.get("domains", []):
        text = domain.get("finding", "").lower()

        if "recent" in text or "new" in text:
            findings["recent_domain"] = True
            observations.append(
                "The domain appears to have been registered recently."
            )

    # Email analysis
    company_domain = data.get("company", {}).get("domain", "")

    for email in data.get("emails", []):
        address = email.get("email", "")

        if "@" in address and company_domain:
            email_domain = address.split("@")[-1]

            if email_domain.lower() != company_domain.lower():
                findings["email_mismatch"] = True
                observations.append(
                    "A contact email does not match the organization's domain."
                )

    # Recruiter verification
    if data.get("people"):
        for person in data["people"]:
            if not person.get("verified", False):
                findings["unverified_recruiter"] = True
                observations.append(
                    f"Public verification of {person.get('name', 'the recruiter')} "
                    "is incomplete."
                )

    return findings, observations


def main():

    data_path = Path("data/sample_data.json")

    with open(data_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    findings, observations = analyze_findings(data)

    print("\nAI-ASSISTED OSINT ANALYSIS")
    print("=" * 35)

    if observations:
        for observation in observations:
            print("-", observation)
    else:
        print("No major inconsistencies detected.")

    return findings


if __name__ == "__main__":
    main()