import pandas as pd

def get_row_count(conn):
    query = "SELECT COUNT(*) AS row_count FROM silver_matches"
    return pd.read_sql(query, conn)


def preview_matches(conn):
    query = "SELECT * FROM silver_matches LIMIT 10"
    return pd.read_sql(query, conn)


def matches_by_type(conn):
    query = """
    SELECT matchType, COUNT(*) AS num_matches
    FROM silver_matches
    GROUP BY matchType
    ORDER BY num_matches DESC
    """
    return pd.read_sql(query, conn)


def matches_by_status(conn):
    query = """
    SELECT status, COUNT(*) AS num_matches
    FROM silver_matches
    GROUP BY status
    ORDER BY num_matches DESC
    """
    return pd.read_sql(query, conn)

def preview_teams(conn):
    query = "SELECT * FROM silver_teams LIMIT 10"
    return pd.read_sql(query, conn)