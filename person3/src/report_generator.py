import csv
import json
from pathlib import Path


def save_json(data, filepath):
    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_csv(data, filepath):
    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []

    for evidence in data.get(
        "evidence_table",
        []
    ):

        rows.append({
            "Entity":
                evidence.get("entity"),

            "Found Information":
                evidence.get("found_information"),

            "Source":
                evidence.get("source"),

            "Relationship":
                evidence.get("relationship"),

            "Suspicious":
                evidence.get("suspicious"),

            "Confidence":
                evidence.get("confidence")
        })

    if not rows:

        rows.append({
            "Entity": "System",
            "Found Information":
                "No evidence generated",
            "Source": "Person 3 OSINT",
            "Relationship":
                "Investigation",
            "Suspicious": "Unknown",
            "Confidence": "None"
        })

    with path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Entity",
                "Found Information",
                "Source",
                "Relationship",
                "Suspicious",
                "Confidence"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)