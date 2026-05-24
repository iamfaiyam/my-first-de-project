from extract import fetch_matches, save_raw_data
from transform import transform_matches
from load import create_connection, load_to_sqlite
from gold import (
    create_gold_match_type_summary,
    create_gold_match_status_summary,
    create_gold_team_match_counts
)
from queries import (
    get_row_count,
    preview_matches,
    matches_by_type,
    matches_by_status,
    preview_teams
)


def main():
    print("Fetching cricket match data...")
    raw_data = fetch_matches()

    print("Saving raw JSON to Bronze layer...")
    save_raw_data(raw_data, "data/bronze/matches_raw.json")

    print("Transforming data into Silver layer...")
    df_matches, df_teams = transform_matches(raw_data)

    if df_matches.empty:
        print("No match data found.")
        return

    print("Loading Silver tables to SQLite...")
    conn = create_connection()
    load_to_sqlite(df_matches, "silver_matches", conn)
    load_to_sqlite(df_teams, "silver_teams", conn)

    print("Creating Gold tables...")
    df_gold_match_type_summary = create_gold_match_type_summary(conn)
    df_gold_match_status_summary = create_gold_match_status_summary(conn)
    df_gold_team_match_counts = create_gold_team_match_counts(conn)

    print("Loading Gold tables to SQLite...")
    load_to_sqlite(df_gold_match_type_summary, "gold_match_type_summary", conn)
    load_to_sqlite(df_gold_match_status_summary, "gold_match_status_summary", conn)
    load_to_sqlite(df_gold_team_match_counts, "gold_team_match_counts", conn)

    print("\nSilver row count:")
    print(get_row_count(conn))

    print("\nPreview matches:")
    print(preview_matches(conn))

    print("\nMatches by type:")
    print(matches_by_type(conn))

    print("\nMatches by status:")
    print(matches_by_status(conn))

    print("\nPreview teams:")
    print(preview_teams(conn))

    print("\nGold: match type summary")
    print(df_gold_match_type_summary)

    print("\nGold: match status summary")
    print(df_gold_match_status_summary)

    print("\nGold: team match counts")
    print(df_gold_team_match_counts)

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()