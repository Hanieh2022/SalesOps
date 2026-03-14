import pandas as pd

# ------------------------------------------------------------
# Scoring logic (1-10 scale)
# Weights:
#   Compliance Pressure = 40% -> Regulations, sensitive data, security expectations (health, cloud, telecom, defense, etc.)
#   Business Model Fit  = 35% -> B2B SaaS / infrastructure companies often need certifications like ISO/IEC 27001 to sell to enterprise clients.
#   Size Fit            = 25% -> Cyberday’s best segment is typically 50–1000 employees (they need compliance but lack large internal GRC teams).
# ------------------------------------------------------------

compliance_score_map = {
    "Cloud Infrastructure": 10.0,
    "Secure Communications": 10.0,
    "Space Technology": 9.5,
    "Health Tech": 9.5,
    "Telecommunications": 9.0,
    "Machine Learning Infrastructure": 9.0,
    "XR Technology": 8.5,
    "Automotive Software": 8.0,
    "AdTech": 7.5,
    "Retail Tech": 7.0,
    "Data Consulting": 7.0,
    "Software Development": 6.5,
    "IT Services": 6.5,
    "E-commerce AI": 7.5,
    "E-commerce": 5.5,
    "Platform": 5.0,
    "Mobile Gaming": 4.0,
}

business_fit_score_map = {
    "Cloud Infrastructure": 10.0,
    "Machine Learning Infrastructure": 9.5,
    "Secure Communications": 9.0,
    "Health Tech": 8.5,
    "Space Technology": 8.5,
    "XR Technology": 8.0,
    "AdTech": 8.0,
    "Retail Tech": 7.5,
    "E-commerce AI": 7.5,
    "Automotive Software": 7.0,
    "Data Consulting": 6.5,
    "Software Development": 6.0,
    "IT Services": 6.0,
    "Telecommunications": 4.5,
    "E-commerce": 5.0,
    "Platform": 4.5,
    "Mobile Gaming": 3.5,
}

def size_fit_score(approximate_size: float) -> float:
    """
    Score company size based on Cyberday-style ICP:
    best fit is roughly 50-1000 employee size.
    """
    if 50 <= approximate_size <= 1000:
        return 10.0
    elif 1001 <= approximate_size <= 3000:
        return 7.5
    elif 20 <= approximate_size < 50:
        return 7.0
    elif 3001 <= approximate_size <= 10000:
        return 4.5
    elif approximate_size > 10000:
        return 2.0
    else:
        return 5.0


def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    df["compliance_pressure_score"] = (
        df["business_segment"].map(compliance_score_map).fillna(5.0)
    )

    df["business_model_fit_score"] = (
        df["business_segment"].map(business_fit_score_map).fillna(5.0)
    )

    df["size_fit_score"] = df["approximate_size"].apply(size_fit_score)

    df["lead_score"] = (
        df["compliance_pressure_score"] * 0.40
        + df["business_model_fit_score"] * 0.35
        + df["size_fit_score"] * 0.25
    ).round(2)

    return df