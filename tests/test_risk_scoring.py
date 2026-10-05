from ai.risk_scoring import calculate_risk


def test_low_risk():

    findings = {
        "recent_domain": False,
        "email_mismatch": False,
        "address_mismatch": False,
        "unverified_recruiter": False,
        "suspicious_social": False,
        "infrastructure_mismatch": False
    }

    result = calculate_risk(findings)

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"


def test_high_risk():

    findings = {
        "recent_domain": True,
        "email_mismatch": True,
        "address_mismatch": True,
        "unverified_recruiter": True,
        "suspicious_social": False,
        "infrastructure_mismatch": True
    }

    result = calculate_risk(findings)

    assert result["risk_score"] == 90
    assert result["risk_level"] == "CRITICAL"


def test_score_limit():

    findings = {
        "recent_domain": True,
        "email_mismatch": True,
        "address_mismatch": True,
        "unverified_recruiter": True,
        "suspicious_social": True,
        "infrastructure_mismatch": True
    }

    result = calculate_risk(findings)

    assert result["risk_score"] <= 100