from pathlib import Path
import time
import requests
import pandas as pd

BASE_URL = "https://avoindata.prh.fi/opendata-ytj-api/v3/companies"

def extract_best_name(company: dict) -> str | None:
    """
    Try to extract the most useful company name from the API response.
    """
    names = company.get("names", [])
    if not names:
        return None

    for entry in names:
        name_value = entry.get("name")
        if name_value:
            return name_value

    return None


def extract_business_line(company: dict) -> str | None:
    """
    Extract the English description of the main business line if available.
    """
    main_line = company.get("mainBusinessLine")
    if not main_line:
        return None

    descriptions = main_line.get("descriptions", [])
    if not descriptions:
        return None

    for entry in descriptions:
        if entry.get("languageCode") == "3" and entry.get("description"):
            return entry["description"]

    # fallback to any description
    for entry in descriptions:
        if entry.get("description"):
            return entry["description"]

    return None


def extract_website(company: dict) -> str | None:
    website = company.get("website")
    if not website:
        return None
    return website.get("url")


def extract_location(company: dict) -> str | None:
    addresses = company.get("addresses", [])
    if not addresses:
        return None

    for address in addresses:
        post_offices = address.get("postOffices", [])
        for office in post_offices:
            city = office.get("city")
            if city:
                return city

    return None


def search_company_by_name(name: str) -> dict | None:
    """
    Search PRH/YTJ by company name and return the first match.
    """
    params = {"name": name}

    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    companies = data.get("companies", [])

    if not companies:
        return None

    return companies[0]


def enrich_companies(df: pd.DataFrame, sleep_seconds: float = 0.5) -> pd.DataFrame:
    """
    Enrich seed companies with PRH/YTJ company data.
    """
    enriched_rows = []

    for _, row in df.iterrows():
        seed_name = row["company_name"]

        try:
            company = search_company_by_name(seed_name)
        except requests.RequestException as exc:
            print(f"API error for {seed_name}: {exc}")
            company = None

        enriched_row = {
            "company_name": seed_name,
            "country": row["country"],
            "business_segment": row["business_segment"],
            "approximate_size": row["approximate_size"],
            "matched_name": None,
            "business_id": None,
            "business_line": None,
            "website": None,
            "location": None,
            "match_found": False,
        }

        if company:
            enriched_row.update(
                {
                    "matched_name": extract_best_name(company),
                    "business_id": company.get("businessId", {}).get("value"),
                    "business_line": extract_business_line(company),
                    "website": extract_website(company),
                    "location": extract_location(company),
                    "match_found": True,
                }
            )

        enriched_rows.append(enriched_row)

        # polite pause to avoid hammering the API
        time.sleep(sleep_seconds)

    return pd.DataFrame(enriched_rows)

