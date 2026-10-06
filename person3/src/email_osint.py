from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError


FREE_EMAIL_PROVIDERS = {
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "proton.me",
    "protonmail.com",
    "icloud.com"
}


def investigate_email(email, website=None):
    result = {
        "entity": "email",
        "value": email,
        "syntax_valid": False,
        "email_domain": None,
        "website_domain": None,
        "domain_match": None,
        "provider_type": None,
        "red_flags": [],
        "sources": []
    }

    if not email:
        result["red_flags"].append("No email address supplied")
        return result

    try:
        validated = validate_email(
            email,
            check_deliverability=False
        )

        domain = validated.domain.lower()

        result["syntax_valid"] = True
        result["email_domain"] = domain

    except EmailNotValidError as error:
        result["red_flags"].append(
            f"Invalid email syntax: {error}"
        )
        return result

    if domain in FREE_EMAIL_PROVIDERS:
        result["provider_type"] = "free_email_provider"

        result["red_flags"].append(
            "Email uses a free email provider"
        )
    else:
        result["provider_type"] = "custom_domain"

    if website:

        parsed = urlparse(
            website if "://" in website
            else f"https://{website}"
        )

        website_domain = parsed.hostname

        if website_domain:

            website_domain = website_domain.lower()

            result["website_domain"] = website_domain

            result["domain_match"] = (
                domain == website_domain
                or domain.endswith("." + website_domain)
            )

            if not result["domain_match"]:
                result["red_flags"].append(
                    "Email domain differs from claimed company website"
                )

    result["sources"].append({
        "type": "input",
        "value": email
    })

    return result