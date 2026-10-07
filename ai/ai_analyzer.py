def analyze_findings(data):
    """
    Analyze real OSINT findings.

    This produces investigative indicators only.
    It does not establish fraud or criminal activity.
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

    # Government verification
    verification = data.get("government_verification", {})

    if verification:
        observations.append(
            "Official government verification information "
            "was identified in the case evidence."
        )

    # Infrastructure observations
    infrastructure = data.get("infrastructure", [])

    for record in infrastructure:

        if record.get("registration_note"):
            findings["recent_domain"] = True
            observations.append(
                f"Domain {record.get('domain', 'unknown')} "
                "has a registration-related indicator requiring verification."
            )

        for flag in record.get("red_flags", []):
            findings["infrastructure_mismatch"] = True
            observations.append(
                f"Infrastructure finding: {flag}"
            )

    # Explicit case red flags
    for flag in data.get("red_flags", []):
        observations.append(
            f"Case finding: {flag}"
        )

    # Email analysis
    company_domain = (
        data.get("company", {}).get("domain", "")
    )

    for email in data.get("emails", []):

        if isinstance(email, dict):
            address = email.get("email", "")
        else:
            address = str(email)

        if "@" in address and company_domain:

            email_domain = address.split("@")[-1]

            if email_domain.lower() != company_domain.lower():

                findings["email_mismatch"] = True

                observations.append(
                    "A contact email does not match "
                    "the organization's domain."
                )

    # People verification
    for person in data.get("people", []):

        if isinstance(person, dict):

            if not person.get("verified", True):

                findings["unverified_recruiter"] = True

                observations.append(
                    f"Public verification of "
                    f"{person.get('name', 'the associated person')} "
                    "is incomplete."
                )

    if not observations:
        observations.append(
            "No additional rule-based inconsistencies "
            "were detected from the available structured data."
        )

    return findings, observations