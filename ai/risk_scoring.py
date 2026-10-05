def calculate_risk(findings):
    """
    Calculate an investigative risk score from OSINT findings.
    This is a heuristic score, not a probability of fraud.
    """

    score = 0
    red_flags = []

    # Recently registered domain
    if findings.get("recent_domain"):
        score += 20
        red_flags.append(
            "Domain appears to have been registered recently."
        )

    # Email mismatch
    if findings.get("email_mismatch"):
        score += 25
        red_flags.append(
            "Contact email does not match the organization's domain."
        )

    # Address inconsistency
    if findings.get("address_mismatch"):
        score += 15
        red_flags.append(
            "Organization address differs across sources."
        )

    # Recruiter identity not verified
    if findings.get("unverified_recruiter"):
        score += 15
        red_flags.append(
            "Recruiter identity could not be independently verified."
        )

    # Suspicious social account
    if findings.get("suspicious_social"):
        score += 10
        red_flags.append(
            "Associated social-media account requires further verification."
        )

    # Infrastructure inconsistency
    if findings.get("infrastructure_mismatch"):
        score += 15
        red_flags.append(
            "Technical infrastructure shows inconsistencies with the claimed organization."
        )

    score = min(score, 100)

    if score <= 25:
        level = "LOW"
    elif score <= 50:
        level = "MEDIUM"
    elif score <= 75:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return {
        "risk_score": score,
        "risk_level": level,
        "red_flags": red_flags
    }


if __name__ == "__main__":

    # Test data
    test_findings = {
        "recent_domain": True,
        "email_mismatch": True,
        "address_mismatch": False,
        "unverified_recruiter": True,
        "suspicious_social": False,
        "infrastructure_mismatch": True
    }

    result = calculate_risk(test_findings)

    print("OSINT INVESTIGATION RISK ASSESSMENT")
    print("-----------------------------------")
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])

    print("\nRed Flags:")

    for flag in result["red_flags"]:
        print("-", flag)