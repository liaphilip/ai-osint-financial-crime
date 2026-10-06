from urllib.parse import quote_plus


def generate_search_queries(input_data):
    """
    Generate Google/Bing OSINT investigation queries.
    """

    company = input_data.get("company", "")
    recruiter_name = input_data.get("recruiter_name", "")
    email = input_data.get("email", "")
    username = input_data.get("username", "")
    phone = input_data.get("phone", "")
    website = input_data.get("website", "")

    queries = []

    # ==========================================
    # PERSON + COMPANY
    # ==========================================

    if recruiter_name and company:

        queries.append({
            "query_type": "person_company",
            "query": f'"{recruiter_name}" "{company}"'
        })

    # ==========================================
    # EMAIL
    # ==========================================

    if email:

        queries.append({
            "query_type": "email",
            "query": f'"{email}"'
        })

        queries.append({
            "query_type": "email_scam",
            "query": f'"{email}" scam'
        })

    # ==========================================
    # USERNAME
    # ==========================================

    if username:

        queries.append({
            "query_type": "username",
            "query": f'"{username}"'
        })

        if company:

            queries.append({
                "query_type": "username_company",
                "query": f'"{username}" "{company}"'
            })

    # ==========================================
    # RECRUITER NAME
    # ==========================================

    if recruiter_name:

        queries.append({
            "query_type": "name",
            "query": f'"{recruiter_name}"'
        })

        queries.append({
            "query_type": "name_scam",
            "query": f'"{recruiter_name}" scam'
        })

    # ==========================================
    # PHONE
    # ==========================================

    if phone:

        queries.append({
            "query_type": "phone",
            "query": f'"{phone}"'
        })

    # ==========================================
    # COMPANY SCAM
    # ==========================================

    if company:

        queries.append({
            "query_type": "company_scam",
            "query": f'"{company}" scam'
        })

        queries.append({
            "query_type": "company_reviews",
            "query": f'"{company}" reviews'
        })

    # ==========================================
    # WEBSITE
    # ==========================================

    if website:

        queries.append({
            "query_type": "website",
            "query": f'"{website}"'
        })

    return queries


def create_search_urls(queries):
    """
    Create Google and Bing URLs for generated queries.
    """

    results = []

    for item in queries:

        query = item["query"]

        encoded = quote_plus(query)

        results.append({
            "query_type": item["query_type"],
            "query": query,
            "google_url":
                f"https://www.google.com/search?q={encoded}",
            "bing_url":
                f"https://www.bing.com/search?q={encoded}"
        })

    return results


def investigate_search_osint(input_data):
    """
    Generate search-engine OSINT investigation data.
    """

    queries = generate_search_queries(
        input_data
    )

    search_results = create_search_urls(
        queries
    )

    return {
        "entity": "search_engine_osint",
        "tool": "Google/Bing",
        "query_count": len(search_results),
        "queries": search_results,
        "red_flags": [],
        "sources": [
            {
                "type": "search_engine",
                "name": "Google"
            },
            {
                "type": "search_engine",
                "name": "Bing"
            }
        ]
    }