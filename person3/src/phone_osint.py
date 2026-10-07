import phonenumbers

from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat
)


def investigate_phone(phone, default_region=None):

    result = {
        "entity": "phone",
        "value": phone,
        "valid": False,
        "possible": False,
        "country_code": None,
        "international_format": None,
        "national_format": None,
        "red_flags": [],
        "sources": []
    }

    # Check whether phone number was supplied
    if not phone:

        result["red_flags"].append(
            "No phone number supplied"
        )

        return result

    try:

        # Parse phone number
        number = phonenumbers.parse(
            phone,
            default_region
        )

        # Validate number
        result["valid"] = (
            phonenumbers.is_valid_number(number)
        )

        result["possible"] = (
            phonenumbers.is_possible_number(number)
        )

        # Country code
        result["country_code"] = (
            number.country_code
        )

        # International format
        result["international_format"] = (
            phonenumbers.format_number(
                number,
                PhoneNumberFormat.INTERNATIONAL
            )
        )

        # National format
        result["national_format"] = (
            phonenumbers.format_number(
                number,
                PhoneNumberFormat.NATIONAL
            )
        )

        # Add warnings
        if not result["possible"]:

            result["red_flags"].append(
                "Phone number appears structurally invalid"
            )

        elif not result["valid"]:

            result["red_flags"].append(
                "Phone number is not recognized as valid"
            )

    except NumberParseException as error:

        result["red_flags"].append(
            f"Could not parse phone number: {error}"
        )

    # Record source
    result["sources"].append({
        "type": "input",
        "value": phone
    })

    return result