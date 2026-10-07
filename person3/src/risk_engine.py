def calculate_risk(identity_findings, red_flags):

    score = 0
    reasons = []
    evidence = []

    # ==========================================
    # IDENTITY FINDINGS
    # ==========================================

    for finding in identity_findings:

        entity = finding.get("entity")
        status = finding.get("status")
        confidence = finding.get("confidence")
        finding_text = finding.get("finding")

        # --------------------------------------
        # HIGH-RISK CONFLICT
        # --------------------------------------

        if status == "CONFLICT":

            if confidence == "high":
                points = 30

            elif confidence == "medium":
                points = 20

            else:
                points = 10

            score += points

            reasons.append(finding_text)

            evidence.append({
                "entity": entity,
                "points": points,
                "reason": finding_text
            })

        # --------------------------------------
        # REQUIRES REVIEW
        # --------------------------------------

        elif status == "REQUIRES_REVIEW":

            points = 10

            score += points

            reasons.append(finding_text)

            evidence.append({
                "entity": entity,
                "points": points,
                "reason": finding_text
            })

        # --------------------------------------
        # SUPPORTED
        # --------------------------------------

        elif status == "SUPPORTED":

            evidence.append({
                "entity": entity,
                "points": 0,
                "reason": finding_text
            })

        # --------------------------------------
        # CANDIDATE
        # --------------------------------------

        elif status == "CANDIDATE":

            # A public profile is NOT automatically
            # considered suspicious.

            evidence.append({
                "entity": entity,
                "points": 0,
                "reason": finding_text
            })

    # ==========================================
    # RED FLAGS
    # ==========================================

    for flag in red_flags:

        if not flag:
            continue

        # Avoid double counting some findings
        # already represented above.

        already_recorded = any(
            flag == reason
            for reason in reasons
        )

        if already_recorded:
            continue

        points = 5

        score += points

        reasons.append(flag)

        evidence.append({
            "entity": "red_flag",
            "points": points,
            "reason": flag
        })

    # ==========================================
    # CAP SCORE
    # ==========================================

    score = min(score, 100)

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if score >= 70:

        risk_level = "HIGH"

    elif score >= 40:

        risk_level = "MEDIUM"

    elif score >= 15:

        risk_level = "LOW"

    else:

        risk_level = "MINIMAL"

    # ==========================================
    # RECOMMENDATION
    # ==========================================

    if risk_level == "HIGH":

        recommendation = (
            "Perform manual verification before trusting "
            "the recruiter or job opportunity."
        )

    elif risk_level == "MEDIUM":

        recommendation = (
            "Additional identity and organization "
            "verification is recommended."
        )

    elif risk_level == "LOW":

        recommendation = (
            "Some indicators require review, but the "
            "available evidence is limited."
        )

    else:

        recommendation = (
            "No significant automated identity indicators "
            "were detected."
        )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
        "evidence": evidence,
        "recommendation": recommendation
    }