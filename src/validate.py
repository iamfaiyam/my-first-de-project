import pandas as pd


def validate_silver_matches(conn):
    checks = {}

    checks["row_count"] = pd.read_sql(
        """
        SELECT COUNT(*) AS count
        FROM silver_matches
        """,
        conn
    )

    checks["null_ids"] = pd.read_sql(
        """
        SELECT COUNT(*) AS null_ids
        FROM silver_matches
        WHERE id IS NULL
        """,
        conn
    )

    checks["duplicate_ids"] = pd.read_sql(
        """
        SELECT
            id,
            COUNT(*) AS count
        FROM silver_matches
        GROUP BY id
        HAVING COUNT(*) > 1
        """,
        conn
    )

    return checks

def validate_silver_teams(conn):
    checks = {}

    checks["row_count"] = pd.read_sql(
        "SELECT COUNT(*) AS count FROM silver_teams",
        conn
    )

    checks["null_match_ids"] = pd.read_sql(
        """
        SELECT COUNT(*) AS null_match_ids
        FROM silver_teams
        WHERE match_id IS NULL
        """,
        conn
    )

    checks["null_team_names"] = pd.read_sql(
        """
        SELECT COUNT(*) AS null_team_names
        FROM silver_teams
        WHERE team_name IS NULL
        """,
        conn
    )

    checks["orphan_team_records"] = pd.read_sql(
        """
        SELECT COUNT(*) AS orphan_records
        FROM silver_teams t
        LEFT JOIN silver_matches m
            ON t.match_id = m.id
        WHERE m.id IS NULL
        """,
        conn
    )

    return checks


def validate_gold_tables(conn):
    checks = {}

    checks["gold_match_type_summary_row_count"] = pd.read_sql(
        "SELECT COUNT(*) AS count FROM gold_match_type_summary",
        conn
    )

    checks["gold_match_status_summary_row_count"] = pd.read_sql(
        "SELECT COUNT(*) AS count FROM gold_match_status_summary",
        conn
    )

    checks["gold_team_match_counts_row_count"] = pd.read_sql(
        "SELECT COUNT(*) AS count FROM gold_team_match_counts",
        conn
    )

    checks["gold_match_type_total_vs_silver"] = pd.read_sql(
        """
        SELECT
            (SELECT SUM(match_count) FROM gold_match_type_summary) AS gold_total,
            (SELECT COUNT(*) FROM silver_matches) AS silver_total
        """,
        conn
    )

    return checks




