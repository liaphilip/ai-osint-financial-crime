def normalize(value):
    """Normalize text for comparison."""
    if value is None:
        return ""

    return str(value).strip().lower()


def compare_identity(
    input_data,
    email_result,
    phone_result,
    sherlock_result
):
    """
    Compare identity-related evidence collected from
    email, phone and username investigations.

    Important:
    A public profile match is treated as candidate evidence,
    not automatic proof of identity.
    """

    findings = []

    # -------------------------------------------------
    # BASIC INPUT INFORMATION
    # -------------------------------------------------

    recruiter_name = normalize(
        input_data.get("recruiter_name")
    )

    company = normalize(
        input_data.get("company")
    )

    claimed_location = normalize(
        input_data.get("claimed_location")
    )

    claimed_role = normalize(
        input_data.get("claimed_role")
    )

    # -------------------------------------------------
    # EMAIL DOMAIN MATCH
    # -------------------------------------------------

    email_domain_match = email_result.get(
        "domain_match"
    )

    if email_domain_match is True:

        findings.append({
            "entity": "email",
            "status": "SUPPORTED",
            "finding": (
                "Email domain matches the claimed "
                "company website domain."
            ),
            "confidence": "medium"
        })

    elif email_domain_match is False:

        findings.append({
            "entity": "email",
            "status": "CONFLICT",
            "finding": (
                "Email domain differs from the claimed "
                "company website domain."
            ),
            "confidence": "medium"
        })

    # -------------------------------------------------
    # FREE EMAIL PROVIDER
    # -------------------------------------------------

    if email_result.get(
        "provider_type"
    ) == "free_email_provider":

        findings.append({
            "entity": "email",
            "status": "REQUIRES_REVIEW",
            "finding": (
                "The contact uses a free email provider "
                "instead of a company-domain email."
            ),
            "confidence": "low"
        })

    # -------------------------------------------------
    # EMAIL SYNTAX
    # -------------------------------------------------

    if email_result.get("syntax_valid"):

        findings.append({
            "entity": "email",
            "status": "VALID",
            "finding": (
                "Email address has valid syntax."
            ),
            "confidence": "low"
        })

    else:

        findings.append({
            "entity": "email",
            "status": "INVALID",
            "finding": (
                "Email address failed syntax validation."
            ),
            "confidence": "medium"
        })

    # -------------------------------------------------
    # PHONE VALIDATION
    # -------------------------------------------------

    if phone_result.get("valid"):

        findings.append({
            "entity": "phone",
            "status": "SUPPORTED",
            "finding": (
                "Phone number is recognized as a "
                "valid number."
            ),
            "confidence": "low"
        })

    elif phone_result.get("possible"):

        findings.append({
            "entity": "phone",
            "status": "REQUIRES_REVIEW",
            "finding": (
                "Phone number is structurally possible "
                "but could not be fully validated."
            ),
            "confidence": "low"
        })

    else:

        findings.append({
            "entity": "phone",
            "status": "CONFLICT",
            "finding": (
                "Phone number appears invalid or "
                "could not be parsed."
            ),
            "confidence": "medium"
        })

    # -------------------------------------------------
    # SHERLOCK RESULTS
    # -------------------------------------------------

    profiles = sherlock_result.get(
        "profiles",
        []
    )

    if profiles:

        findings.append({
            "entity": "username",
            "status": "FOUND",
            "finding": (
                f"Sherlock discovered "
                f"{len(profiles)} candidate public "
                f"profile(s) for the username."
            ),
            "confidence": "low"
        })

        # Each Sherlock result is preserved as
        # candidate evidence.

        for index, profile in enumerate(
            profiles,
            start=1
        ):

            findings.append({
                "entity": "social_profile",
                "status": "CANDIDATE",
                "finding": (
                    f"Candidate public profile #{index}: "
                    f"{profile.get('raw_result', '')}"
                ),
                "confidence": "low"
            })

    else:

        findings.append({
            "entity": "username",
            "status": "UNKNOWN",
            "finding": (
                "No candidate public profiles "
                "were discovered by Sherlock."
            ),
            "confidence": "none"
        })

    # -------------------------------------------------
    # IDENTITY INPUT SUMMARY
    # -------------------------------------------------

    if recruiter_name:

        findings.append({
            "entity": "person",
            "status": "INPUT",
            "finding": (
                f"Investigation subject name: "
                f"{input_data.get('recruiter_name')}"
            ),
            "confidence": "none"
        })

    if company:

        findings.append({
            "entity": "company",
            "status": "INPUT",
            "finding": (
                f"Claimed company: "
                f"{input_data.get('company')}"
            ),
            "confidence": "none"
        })

    if claimed_location:

        findings.append({
            "entity": "location",
            "status": "INPUT",
            "finding": (
                f"Claimed location: "
                f"{input_data.get('claimed_location')}"
            ),
            "confidence": "none"
        })

    if claimed_role:

        findings.append({
            "entity": "role",
            "status": "INPUT",
            "finding": (
                f"Claimed role: "
                f"{input_data.get('claimed_role')}"
            ),
            "confidence": "none"
        })

    return findings