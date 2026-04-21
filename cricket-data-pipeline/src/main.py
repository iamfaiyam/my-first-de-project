from extract import fetch_matches, save_raw_data
from transform import transform_matches
from load import create_connection, load_to_sqlite
from queries import (
    get_row_count,
    preview_matches,
    matches_by_type,
    matches_by_status
)

def main():
    
    print("Fetching cricket match data...")
    raw_data = fetch_matches()

    print("Saving raw JSON...")
    save_raw_data(raw_data, "data/raw/matches_raw.json")

    print("Transforming data...")
    df_matches = transform_matches(raw_data)

    if df_matches.empty:
        print("No match data found.")
        return

    print("Loading to SQLite...")
    conn = create_connection()
    load_to_sqlite(df_matches, "matches", conn)

    print("\nRow count:")
    print(get_row_count(conn))

    print("\nPreview matches:")
    print(preview_matches(conn))

    print("\nMatches by type:")
    print(matches_by_type(conn))

    print("\nMatches by status:")
    print(matches_by_status(conn))

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
