import pandas as pd


def transform_matches(api_response: dict) -> pd.DataFrame:
    matches = api_response.get("data", [])

    if not matches:
        return pd.DataFrame()

    df = pd.DataFrame(matches)

    desired_cols = [
        "id",
        "name",
        "matchType",
        "status",
        "venue",
        "date"
    ]

    available_cols = [col for col in desired_cols if col in df.columns]
    df_clean = df[available_cols].copy()

    return df_clean
