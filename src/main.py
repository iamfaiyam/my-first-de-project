from extract import fetch_matches, save_raw_data
from transform import transform_matches
from load import create_connection, load_to_sqlite
from gold import (
    create_gold_match_type_summary,
    create_gold_match_status_summary,
    create_gold_team_match_counts
)
from logger import log
from queries import (
    get_row_count,
    preview_matches,
    matches_by_type,
    matches_by_status,
    preview_teams
)
from validate import (
    validate_silver_matches,
    validate_silver_teams,
    validate_gold_tables
)


SHOW_PREVIEWS = False


def print_validation_results(validation_checks: dict) -> None:
    for check_name, result in validation_checks.items():
        log(f"Validation check completed: {check_name}")

        if SHOW_PREVIEWS:
            print(f"\n{check_name}:")
            print(result)


def print_pipeline_summary(
    df_matches,
    df_teams,
    df_gold_match_type_summary,
    df_gold_match_status_summary,
    df_gold_team_match_counts
):
    print("\n==============================")
    print("Pipeline Summary")
    print("==============================")
    print(f"Silver matches loaded: {len(df_matches)}")
    print(f"Silver teams loaded: {len(df_teams)}")
    print(f"Gold match type summary rows: {len(df_gold_match_type_summary)}")
    print(f"Gold match status summary rows: {len(df_gold_match_status_summary)}")
    print(f"Gold team match count rows: {len(df_gold_team_match_counts)}")
    print("==============================\n")


def main():
    log("Pipeline started")

    log("Fetching cricket match data")
    raw_data = fetch_matches()

    log("Saving raw JSON to Bronze layer")
    save_raw_data(raw_data, "data/bronze/matches_raw.json")

    log("Transforming data into Silver layer")
    df_matches, df_teams = transform_matches(raw_data)

    if df_matches.empty:
        log("No match data found. Pipeline stopped.")
        return

    log("Connecting to SQLite database")
    conn = create_connection()

    try:
        log("Loading Silver tables to SQLite")
        load_to_sqlite(df_matches, "silver_matches", conn)
        load_to_sqlite(df_teams, "silver_teams", conn)

        log(f"Loaded {len(df_matches)} rows into silver_matches")
        log(f"Loaded {len(df_teams)} rows into silver_teams")

        log("Running Silver validation checks")
        silver_match_checks = validate_silver_matches(conn)
        print_validation_results(silver_match_checks)
        log("Silver validation checks completed")

        log("Running Silver teams validation checks")
        silver_team_checks = validate_silver_teams(conn)
        print_validation_results(silver_team_checks)
        log("Silver teams validation checks completed")

        log("Creating Gold tables")
        df_gold_match_type_summary = create_gold_match_type_summary(conn)
        df_gold_match_status_summary = create_gold_match_status_summary(conn)
        df_gold_team_match_counts = create_gold_team_match_counts(conn)

        log("Loading Gold tables to SQLite")
        load_to_sqlite(df_gold_match_type_summary, "gold_match_type_summary", conn)
        load_to_sqlite(df_gold_match_status_summary, "gold_match_status_summary", conn)
        load_to_sqlite(df_gold_team_match_counts, "gold_team_match_counts", conn)

        log("Running Gold validation checks")
        gold_checks = validate_gold_tables(conn)
        print_validation_results(gold_checks)
        log("Gold validation checks completed")

        log(f"Created {len(df_gold_match_type_summary)} rows in gold_match_type_summary")
        log(f"Created {len(df_gold_match_status_summary)} rows in gold_match_status_summary")
        log(f"Created {len(df_gold_team_match_counts)} rows in gold_team_match_counts")

        print_pipeline_summary(
            df_matches,
            df_teams,
            df_gold_match_type_summary,
            df_gold_match_status_summary,
            df_gold_team_match_counts
        )

        if SHOW_PREVIEWS:
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

        log("Pipeline completed successfully")

    finally:
        conn.close()
        log("Database connection closed")


if __name__ == "__main__":
    main()