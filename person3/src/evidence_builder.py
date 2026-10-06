def build_evidence_table(
    input_data,
    email_result,
    phone_result,
    sherlock_result,
    search_osint_result,
    identity_findings
):
    """
    Build a structured Person 3 investigation
    evidence table.
    """

    evidence = []

    # ==========================================
    # EMAIL
    # ==========================================

    email = input_data.get("email")

    if email:

        email_suspicious = (
            "Yes"
            if email_result.get("red_flags")
            else "No"
        )

        evidence.append({
            "entity": "Email",
            "found_information": email,
            "source": "Input",
            "relationship": "Recruiter contact",
            "suspicious": email_suspicious,
            "confidence": "Low"
        })

    # ==========================================
    # EMAIL DOMAIN
    # ==========================================

    email_domain = email_result.get(
        "email_domain"
    )

    if email_domain:

        domain_match = email_result.get(
            "domain_match"
        )

        if domain_match is False:

            suspicious = "Yes"
            confidence = "Medium"

        else:

            suspicious = "No"
            confidence = "Medium"

        evidence.append({
            "entity": "Email Domain",
            "found_information": email_domain,
            "source": "Email OSINT",
            "relationship": "Associated with recruiter email",
            "suspicious": suspicious,
            "confidence": confidence
        })

    # ==========================================
    # PHONE
    # ==========================================

    phone = input_data.get("phone")

    if phone:

        phone_suspicious = (
            "Yes"
            if phone_result.get("red_flags")
            else "No"
        )

        evidence.append({
            "entity": "Phone",
            "found_information": phone,
            "source": "Phone OSINT",
            "relationship": "Recruiter contact",
            "suspicious": phone_suspicious,
            "confidence": "Low"
        })

    # ==========================================
    # USERNAME
    # ==========================================

    username = input_data.get("username")

    if username:

        evidence.append({
            "entity": "Username",
            "found_information": username,
            "source": "Input",
            "relationship": "Claimed online identity",
            "suspicious": "Unknown",
            "confidence": "None"
        })

    # ==========================================
    # SHERLOCK PROFILES
    # ==========================================

    profiles = sherlock_result.get(
        "profiles",
        []
    )

    for profile in profiles:

        evidence.append({
            "entity": "Social Profile",
            "found_information": (
                profile.get("url")
                or profile.get("site")
            ),
            "source": "Sherlock",
            "relationship": (
                "Candidate profile associated "
                "with username"
            ),
            "suspicious": "Unknown",
            "confidence": "Low"
        })

    # ==========================================
    # COMPANY
    # ==========================================

    company = input_data.get("company")

    if company:

        evidence.append({
            "entity": "Company",
            "found_information": company,
            "source": "Input",
            "relationship": "Claimed employer",
            "suspicious": "Unknown",
            "confidence": "None"
        })

    # ==========================================
    # WEBSITE
    # ==========================================

    website = input_data.get("website")

    if website:

        evidence.append({
            "entity": "Website",
            "found_information": website,
            "source": "Input",
            "relationship": "Claimed company website",
            "suspicious": "Unknown",
            "confidence": "None"
        })

    # ==========================================
    # RECRUITER
    # ==========================================

    recruiter_name = input_data.get(
        "recruiter_name"
    )

    if recruiter_name:

        evidence.append({
            "entity": "Person",
            "found_information": recruiter_name,
            "source": "Input",
            "relationship": "Claimed recruiter",
            "suspicious": "Unknown",
            "confidence": "None"
        })

    # ==========================================
    # SEARCH QUERIES
    # ==========================================

    for query in search_osint_result.get(
        "queries",
        []
    ):

        evidence.append({
            "entity": "Search Query",
            "found_information": query.get(
                "query"
            ),
            "source": "Google/Bing",
            "relationship": (
                "Generated OSINT investigation query"
            ),
            "suspicious": "Unknown",
            "confidence": "None"
        })

    # ==========================================
    # IDENTITY FINDINGS
    # ==========================================

    for finding in identity_findings:

        status = finding.get("status")

        if status == "CONFLICT":

            suspicious = "Yes"

        elif status == "REQUIRES_REVIEW":

            suspicious = "Review"

        else:

            suspicious = "No"

        evidence.append({
            "entity": finding.get("entity"),
            "found_information": finding.get(
                "finding"
            ),
            "source": finding.get(
                "source",
                "Identity Matching"
            ),
            "relationship": (
                "Identity verification finding"
            ),
            "suspicious": suspicious,
            "confidence": finding.get(
                "confidence"
            )
        })

    return evidence