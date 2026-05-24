import pandas as pd


def transform_matches(api_response: dict):
    matches = api_response.get("data", [])

    if not matches:
        return pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(matches)

    # ----------------------------
    # Silver matches table
    # ----------------------------
    desired_cols = [
        "id",
        "name",
        "matchType",
        "status",
        "venue",
        "date"
    ]

    available_cols = [col for col in desired_cols if col in df.columns]
    df_matches = df[available_cols].copy()

    df_matches["ingestion_timestamp"] = pd.Timestamp.now()

    # ----------------------------
    # Silver teams table
    # ----------------------------
    teams = []

    if "teamInfo" in df.columns:
        for _, row in df.iterrows():
            match_id = row.get("id")
            team_info = row.get("teamInfo", [])

            if isinstance(team_info, list):
                for team in team_info:
                    if isinstance(team, dict):
                        teams.append({
                            "match_id": match_id,
                            "team_name": team.get("name"),
                            "team_shortname": team.get("shortname"),
                            "team_img": team.get("img"),
                            "ingestion_timestamp": pd.Timestamp.now()
                        })

    df_teams = pd.DataFrame(teams)

    return df_matches, df_teams