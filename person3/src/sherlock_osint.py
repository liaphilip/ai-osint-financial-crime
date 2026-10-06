import re
import subprocess
import sys


def parse_sherlock_output(output):
    """
    Convert Sherlock console output into structured
    candidate profile records.
    """

    profiles = []

    for line in output.splitlines():

        line = line.strip()

        if not line.startswith("[+]"):
            continue

        # Remove [+]
        cleaned = line[3:].strip()

        url_match = re.search(
            r"(https?://\S+)",
            cleaned
        )

        url = None

        if url_match:
            url = url_match.group(1).rstrip(".,)")

        site = cleaned

        if ":" in cleaned:
            site = cleaned.split(":", 1)[0].strip()

        profiles.append({
            "site": site,
            "url": url,
            "raw_result": cleaned
        })

    return profiles


def run_sherlock(username):

    result = {
        "entity": "username",
        "username": username,
        "tool": "Sherlock",
        "available": False,
        "profiles": [],
        "profile_count": 0,
        "red_flags": [],
        "sources": []
    }

    if not username:

        result["red_flags"].append(
            "No username supplied"
        )

        return result

    try:

        command = [
            sys.executable,
            "-m",
            "sherlock_project",
            username,
            "--print-found"
        ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180
        )

        result["available"] = True

        profiles = parse_sherlock_output(
            process.stdout
        )

        result["profiles"] = profiles

        result["profile_count"] = len(
            profiles
        )

        result["sources"].append({
            "tool": "Sherlock",
            "username": username
        })

        if process.returncode != 0:

            result["red_flags"].append(
                "Sherlock completed with a non-zero exit status"
            )

    except subprocess.TimeoutExpired:

        result["red_flags"].append(
            "Sherlock search timed out"
        )

    except Exception as error:

        result["red_flags"].append(
            f"Sherlock error: {error}"
        )

    return result