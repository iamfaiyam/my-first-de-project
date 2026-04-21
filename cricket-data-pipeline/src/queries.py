import pandas as pd

def get_row_count(conn):
    query = "SELECT COUNT(*) AS row_count FROM matches"
    return pd.read_sql(query, conn)


def preview_matches(conn):
    query = "SELECT * FROM matches LIMIT 10"
    return pd.read_sql(query, conn)


def matches_by_type(conn):
    query = """
    SELECT matchType, COUNT(*) AS num_matches
    FROM matches
    GROUP BY matchType
    ORDER BY num_matches DESC
    """
    return pd.read_sql(query, conn)


def matches_by_status(conn):
    query = """
    SELECT status, COUNT(*) AS num_matches
    FROM matches
    GROUP BY status
    ORDER BY num_matches DESC
    """
    return pd.read_sql(query, conn)
