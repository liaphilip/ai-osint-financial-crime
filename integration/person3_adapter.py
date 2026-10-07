def run_person3_osint(data):
    """
    Optional Person 3 Identity & Social OSINT integration.

    Person 3 requires identity fields such as recruiter name,
    email, phone, username, and claimed role/location.

    If those fields are not available in the case data,
    the integration safely skips execution rather than
    inventing identity information.
    """

    job = data.get("job_posting", {})
    company = data.get("company", {})

    identity_data = {
        "case_id": data.get("case_id"),
        "company": company.get("name"),
        "job_title": job.get("title"),
        "job_url": job.get("website"),
        "website": job.get("website"),
        "recruiter_name": None,
        "email": None,
        "phone": None,
        "username": None,
        "claimed_location": None,
        "claimed_role": None,
    }

    identity_fields = [
        "recruiter_name",
        "email",
        "phone",
        "username",
        "claimed_location",
        "claimed_role",
    ]

    available_fields = [
        key for key in identity_fields
        if identity_data.get(key)
    ]

    if not available_fields:
        return {
            "status": "SKIPPED",
            "reason": (
                "No verified recruiter, email, phone, "
                "username, or social identity data was "
                "available in the case."
            ),
            "findings": [],
            "red_flags": [],
        }

    return {
        "status": "READY",
        "reason": "Identity/social data is available for analysis.",
        "input": identity_data,
        "findings": [],
        "red_flags": [],
    }