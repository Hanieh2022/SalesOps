from load_clean_data import load_seed_companies
from api_request import enrich_companies
from score_leads import score_leads


def main() -> None:
    seed_df = load_seed_companies("data/seed_companies.csv")
    enriched_df = enrich_companies(seed_df)
    scored_df = score_leads(enriched_df)

    enriched_df.to_csv("data/enriched_companies.csv", index=False)
    scored_df.to_csv("data/scored_companies.csv", index=False)

    print(scored_df[[
    "company_name",
    "lead_score",
]].sort_values("lead_score", ascending=False))


if __name__ == "__main__":
    main()