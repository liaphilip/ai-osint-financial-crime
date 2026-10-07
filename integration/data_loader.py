import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PERSON2_DIR = BASE_DIR / "person2_output"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_case(case_data, infrastructure_records):
    case_id = case_data.get("case_id")

    matching_infrastructure = [
        record
        for record in infrastructure_records
        if record.get("case_id") == case_id
    ]

    domains = []
    ips = []
    subdomains = []
    sources = []

    for record in matching_infrastructure:
        domain = record.get("domain")
        if domain and domain not in domains:
            domains.append(domain)

        for ip in record.get("a_records", []):
            if ip not in ips:
                ips.append(ip)

        for subdomain in record.get("subdomains", []):
            if subdomain not in subdomains:
                subdomains.append(subdomain)

        for source in record.get("sources", []):
            if source not in sources:
                sources.append(source)

    company = dict(case_data.get("company", {}))

    # Compatibility with the original Person 4 pipeline.
    if "name" not in company:
        company["name"] = company.get("claimed_name", "Unknown")

    if "domain" not in company:
        company["domain"] = (
            case_data.get("job_posting", {}).get("website", "")
            .replace("https://", "")
            .replace("http://", "")
            .rstrip("/")
        )

    job_posting = dict(case_data.get("job_posting", {}))

    if "title" not in job_posting:
        job_posting["title"] = job_posting.get(
            "job_type",
            "Recruitment posting"
        )

    return {
        "case_id": case_id,
        "investigation_type": case_data.get("investigation_type"),
        "case_period": case_data.get("case_period"),
        "company": company,
        "job_posting": job_posting,
        "government_verification": case_data.get(
            "government_verification", {}
        ),
        "official_verification": case_data.get(
            "official_verification", {}
        ),
        "domains": domains,
        "infrastructure": matching_infrastructure,
        "emails": case_data.get("emails", []),
        "phones": case_data.get("phones", []),
        "people": case_data.get("people", []),
        "social_accounts": case_data.get("social_accounts", []),
        "ips": ips,
        "subdomains": subdomains,
        "sources": sources,
        "evidence": case_data.get("evidence_files", []),
        "red_flags": case_data.get("red_flags", []),
        "assessment": case_data.get("assessment", {}),
    }


def load_investigation_cases():
    person2_path = PERSON2_DIR / "person2_all.json"

    if person2_path.exists():
        infrastructure_records = load_json(person2_path)
        if not isinstance(infrastructure_records, list):
            infrastructure_records = []
    else:
        infrastructure_records = []

    cases = []

    for case_file in sorted(DATA_DIR.glob("case_*.json")):
        if "_notes" in case_file.name:
            continue

        case_data = load_json(case_file)

        if isinstance(case_data, dict):
            cases.append(
                normalize_case(
                    case_data,
                    infrastructure_records
                )
            )

    return cases


if __name__ == "__main__":
    for case in load_investigation_cases():
        print(
            f"{case['case_id']}: "
            f"{case['company']['name']}"
        )
        print("  Infrastructure:", len(case["infrastructure"]))
        print("  Domains:", case["domains"])
        print("  IPs:", case["ips"])
        print("  Evidence:", len(case["evidence"]))