import argparse
import json
from pathlib import Path

from src.email_osint import investigate_email
from src.phone_osint import investigate_phone
from src.sherlock_osint import run_sherlock
from src.search_osint import investigate_search_osint
from src.identity_matcher import compare_identity
from src.evidence_builder import build_evidence_table
from src.report_generator import save_json, save_csv
from src.risk_engine import calculate_risk


def load_input(filepath):
    """
    Load investigation input from JSON.
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Person 3 - Identity & Social OSINT"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to investigation JSON file"
    )

    args = parser.parse_args()

    input_data = load_input(
        args.input
    )

    print()
    print("=" * 60)
    print(" PERSON 3 - IDENTITY & SOCIAL OSINT")
    print("=" * 60)

    print()

    print(
        f"Case      : "
        f"{input_data.get('case_id')}"
    )

    print(
        f"Company   : "
        f"{input_data.get('company')}"
    )

    print(
        f"Recruiter : "
        f"{input_data.get('recruiter_name')}"
    )

    print(
        f"Username  : "
        f"{input_data.get('username')}"
    )

    # Email investigation

    print()
    print("-" * 60)
    print("EMAIL INVESTIGATION")
    print("-" * 60)

    email_result = investigate_email(
        input_data.get("email"),
        input_data.get("website")
    )

    print(
        f"Email           : "
        f"{input_data.get('email')}"
    )

    print(
        f"Email domain    : "
        f"{email_result.get('email_domain')}"
    )

    print(
        f"Syntax valid    : "
        f"{email_result.get('syntax_valid')}"
    )

    print(
        f"Provider type   : "
        f"{email_result.get('provider_type')}"
    )

    print(
        f"Domain match    : "
        f"{email_result.get('domain_match')}"
    )

    if email_result.get("red_flags"):

        print()
        print("Email flags:")

        for flag in email_result.get(
            "red_flags",
            []
        ):

            print(
                f"  - {flag}"
            )

    # Phone investigation

    print()
    print("-" * 60)
    print("PHONE INVESTIGATION")
    print("-" * 60)

    phone_result = investigate_phone(
        input_data.get("phone")
    )

    print(
        f"Phone           : "
        f"{input_data.get('phone')}"
    )

    print(
        f"Valid           : "
        f"{phone_result.get('valid')}"
    )

    print(
        f"Possible        : "
        f"{phone_result.get('possible')}"
    )

    print(
        f"Country code    : "
        f"{phone_result.get('country_code')}"
    )

    print(
        f"International   : "
        f"{phone_result.get('international_format')}"
    )

    if phone_result.get("red_flags"):

        print()
        print("Phone flags:")

        for flag in phone_result.get(
            "red_flags",
            []
        ):

            print(
                f"  - {flag}"
            )

    # Sherlock investigation

    print()
    print("-" * 60)
    print("SHERLOCK USERNAME INVESTIGATION")
    print("-" * 60)

    sherlock_result = run_sherlock(
        input_data.get("username")
    )

    profiles = sherlock_result.get(
        "profiles",
        []
    )

    print(
        f"Username        : "
        f"{input_data.get('username')}"
    )

    print(
        f"Sherlock        : "
        f"{sherlock_result.get('tool')}"
    )

    print(
        f"Profiles found  : "
        f"{len(profiles)}"
    )

    if profiles:

        print()
        print("Candidate profiles:")

        for profile in profiles:

            print(
                f"  {profile.get('site')} "
                f"- "
                f"{profile.get('url')}"
            )

    else:

        print(
            "No candidate profiles discovered."
        )

    if sherlock_result.get("red_flags"):

        print()
        print("Sherlock flags:")

        for flag in sherlock_result.get(
            "red_flags",
            []
        ):

            print(
                f"  - {flag}"
            )

    # Google and Bing search OSINT

    print()
    print("-" * 60)
    print("GOOGLE/BING SEARCH OSINT")
    print("-" * 60)

    search_osint_result = investigate_search_osint(
        input_data
    )

    print(
        f"Search queries generated : "
        f"{search_osint_result.get('query_count')}"
    )

    search_queries = search_osint_result.get(
        "queries",
        []
    )

    for item in search_queries:

        print()

        print(
            f"Query type : "
            f"{item.get('query_type')}"
        )

        print(
            f"Query      : "
            f"{item.get('query')}"
        )

        print(
            f"Google     : "
            f"{item.get('google_url')}"
        )

        print(
            f"Bing       : "
            f"{item.get('bing_url')}"
        )

    # Identity matching

    print()
    print("-" * 60)
    print("IDENTITY MATCHING")
    print("-" * 60)

    identity_findings = compare_identity(
        input_data,
        email_result,
        phone_result,
        sherlock_result
    )

    print(
        f"Identity findings: "
        f"{len(identity_findings)}"
    )

    for finding in identity_findings:

        print()

        print(
            f"Entity      : "
            f"{finding.get('entity')}"
        )

        print(
            f"Status      : "
            f"{finding.get('status')}"
        )

        print(
            f"Finding     : "
            f"{finding.get('finding')}"
        )

        print(
            f"Confidence  : "
            f"{finding.get('confidence')}"
        )

        if finding.get("source"):

            print(
                f"Source      : "
                f"{finding.get('source')}"
            )

    # Evidence table

    evidence_table = build_evidence_table(
        input_data,
        email_result,
        phone_result,
        sherlock_result,
        search_osint_result,
        identity_findings
    )

    print()
    print("-" * 60)
    print("INVESTIGATION EVIDENCE TABLE")
    print("-" * 60)

    for evidence in evidence_table:

        print()

        print(
            f"Entity        : "
            f"{evidence.get('entity')}"
        )

        print(
            f"Information   : "
            f"{evidence.get('found_information')}"
        )

        print(
            f"Source        : "
            f"{evidence.get('source')}"
        )

        print(
            f"Relationship  : "
            f"{evidence.get('relationship')}"
        )

        print(
            f"Suspicious    : "
            f"{evidence.get('suspicious')}"
        )

        print(
            f"Confidence    : "
            f"{evidence.get('confidence')}"
        )

    # Red flag collection

    red_flags = []

    red_flags.extend(
        email_result.get(
            "red_flags",
            []
        )
    )

    red_flags.extend(
        phone_result.get(
            "red_flags",
            []
        )
    )

    red_flags.extend(
        sherlock_result.get(
            "red_flags",
            []
        )
    )

    red_flags.extend(
        search_osint_result.get(
            "red_flags",
            []
        )
    )

    print()
    print("-" * 60)
    print("INVESTIGATION FLAGS")
    print("-" * 60)

    if red_flags:

        for flag in red_flags:

            print(
                f"  - {flag}"
            )

    else:

        print(
            "No automatic investigation flags."
        )

    # Risk analysis

    print()
    print("-" * 60)
    print("RISK ANALYSIS")
    print("-" * 60)

    risk_analysis = calculate_risk(
        identity_findings,
        red_flags
    )

    print(
        f"Risk score     : "
        f"{risk_analysis.get('risk_score')}/100"
    )

    print(
        f"Risk level     : "
        f"{risk_analysis.get('risk_level')}"
    )

    reasons = risk_analysis.get(
        "reasons",
        []
    )

    if reasons:

        print()
        print("Risk reasons:")

        for reason in reasons:

            print(
                f"  - {reason}"
            )

    else:

        print(
            "No risk reasons generated."
        )

    print()

    print(
        f"Recommendation : "
        f"{risk_analysis.get('recommendation')}"
    )

    # Final report

    report = {

        "case_id":
            input_data.get("case_id"),

        "investigation_type":
            "identity_and_social_osint",

        "subject": {

            "company":
                input_data.get("company"),

            "job_title":
                input_data.get("job_title"),

            "job_url":
                input_data.get("job_url"),

            "website":
                input_data.get("website"),

            "recruiter_name":
                input_data.get("recruiter_name"),

            "claimed_location":
                input_data.get("claimed_location"),

            "claimed_role":
                input_data.get("claimed_role")
        },

        "email":
            email_result,

        "phone":
            phone_result,

        "username_osint":
            sherlock_result,

        "search_osint":
            search_osint_result,

        "identity_findings":
            identity_findings,

        "evidence_table":
            evidence_table,

        "red_flags":
            red_flags,

        "risk_analysis":
            risk_analysis,

        "disclaimer": (
            "OSINT findings are candidate evidence "
            "for investigation and are not automatic "
            "proof of identity or fraud."
        )
    }

    # Output directory

    output_directory = Path(
        "output"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    case_id = input_data.get(
        "case_id",
        "investigation"
    )

    json_file = (
        output_directory /
        f"{case_id}.json"
    )

    csv_file = (
        output_directory /
        f"{case_id}.csv"
    )

    # Save JSON

    save_json(
        report,
        json_file
    )

    # Save CSV

    save_csv(
        report,
        csv_file
    )

    # Final summary

    print()
    print("=" * 60)
    print("INVESTIGATION COMPLETE")
    print("=" * 60)

    print()

    print(
        f"JSON report : "
        f"{json_file}"
    )

    print(
        f"CSV report  : "
        f"{csv_file}"
    )

    print()

    print(
        f"Risk score  : "
        f"{risk_analysis.get('risk_score')}/100"
    )

    print(
        f"Risk level  : "
        f"{risk_analysis.get('risk_level')}"
    )

    print()

    print(
        "OSINT results are indicators for investigation, "
        "not automatic proof of fraud."
    )

    print()


if __name__ == "__main__":
    main()