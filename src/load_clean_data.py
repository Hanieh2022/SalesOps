from pathlib import Path
import pandas as pd

required_columns = ["company_name", "country", "business_segment", "approximate_size"]

def load_seed_companies(csv_path: str) -> pd.DataFrame:
    """
    Load company data from a CSV file and perform basic validation/cleaning.
    """
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    df = pd.read_csv(path)

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Expected columns: {required_columns}"
        )

    # Keep only required columns for now
    df = df[required_columns].copy()

    # Basic cleaning - only strip string columns
    string_columns = ["company_name", "country", "business_segment"]
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Convert numeric columns
    df["approximate_size"] = pd.to_numeric(df["approximate_size"], errors="coerce")

    # Remove empty company names
    df = df[df["company_name"].notna()]
    df = df[df["company_name"].str.lower() != "nan"]
    df = df[df["company_name"] != ""]

    # Remove duplicates by company name + country
    df = df.drop_duplicates(subset=["company_name", "country"]).reset_index(drop=True)

    return df


