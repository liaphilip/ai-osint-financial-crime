def calculate_risk(findings, observations=None):
    """
    Calculate an investigative risk score from OSINT findings
    and case-level observations.

    This is a heuristic investigative indicator, not a
    probability of fraud and not proof of criminal activity.
    """

    score = 0
    red_flags = []

    # -------------------------------------------------
    # TECHNICAL / IDENTITY INDICATORS
    # -------------------------------------------------

    if findings.get("recent_domain"):
        score += 20
        red_flags.append(
            "Domain appears to have been registered recently."
        )

    if findings.get("email_mismatch"):
        score += 25
        red_flags.append(
            "Contact email does not match the organization's domain."
        )

    if findings.get("address_mismatch"):
        score += 15
        red_flags.append(
            "Organization address differs across sources."
        )

    if findings.get("unverified_recruiter"):
        score += 15
        red_flags.append(
            "Recruiter identity could not be independently verified."
        )

    if findings.get("suspicious_social"):
        score += 10
        red_flags.append(
            "Associated social-media account requires further verification."
        )

    if findings.get("infrastructure_mismatch"):
        score += 15
        red_flags.append(
            "Technical infrastructure shows inconsistencies with the claimed organization."
        )

    # -------------------------------------------------
    # CASE-LEVEL OSINT EVIDENCE
    # -------------------------------------------------

    observations = observations or []

    observation_text = " ".join(
        str(item).lower()
        for item in observations
    )

    # Government impersonation / false association
    if (
        "government impersonation" in observation_text
        or "false association" in observation_text
    ):
        score += 15
        red_flags.append(
            "Case evidence indicates possible government impersonation or false association."
        )

    # Unauthorized recruitment
    if (
        "unauthorized recruitment" in observation_text
        or "recruitment conducted without government endorsement"
        in observation_text
        or "recruitment advertisement not authorized"
        in observation_text
    ):
        score += 15
        red_flags.append(
            "Case evidence indicates unauthorized recruitment activity."
        )

    # Payment / recruitment fee
    if (
        "make payment" in observation_text
        or "recruitment fee" in observation_text
        or "payment requested" in observation_text
    ):
        score += 15
        red_flags.append(
            "Applicants were reportedly asked to make a recruitment-related payment."
        )

    # Fake / unauthorized website
    if (
        "fake website" in observation_text
        or "unauthorized recruitment website" in observation_text
    ):
        score += 10
        red_flags.append(
            "Case evidence identifies the recruitment website as unauthorized or fake."
        )

    # Official government warning / enforcement
    if (
        "government enforcement" in observation_text
        or "official government verification" in observation_text
        or "government action" in observation_text
    ):
        score += 10
        red_flags.append(
            "Official government evidence or enforcement action is associated with the case."
        )

    # -------------------------------------------------
    # LIMIT SCORE
    # -------------------------------------------------

    score = min(score, 100)

    # -------------------------------------------------
    # RISK LEVEL
    # -------------------------------------------------

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

    test_findings = {
        "recent_domain": True,
        "email_mismatch": True,
        "address_mismatch": False,
        "unverified_recruiter": True,
        "suspicious_social": False,
        "infrastructure_mismatch": True
    }

    test_observations = [
        "Unauthorized recruitment website",
        "False association with a government organization",
        "Applicants were asked to make payment"
    ]

    result = calculate_risk(
        test_findings,
        test_observations
    )

    print("OSINT INVESTIGATION RISK ASSESSMENT")
    print("-----------------------------------")
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])

    print("\nRed Flags:")

    for flag in result["red_flags"]:
        print("-", flag)