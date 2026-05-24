import pandas as pd

def create_gold_match_type_summary(conn) -> pd.DataFrame: 
    query = """
        SELECT matchType, 
            COUNT(*) AS match_count
        FROM silver_matches
        GROUP BY matchType
        ORDER BY match_count DESC
    """
    return pd.read_sql(query, conn)

def create_gold_match_status_summary(conn) -> pd.DataFrame: 
    query = """
        SELECT status, 
            COUNT(*) AS match_count
        FROM silver_matches
        GROUP BY status
        ORDER BY match_count DESC
    """
    return pd.read_sql(query, conn) 

def create_gold_team_match_counts(conn) -> pd.DataFrame: 
    query = """
        SELECT team_name, 
            team_shortname, 
            COUNT(DISTINCT match_id) AS matches_played
        FROM silver_teams
        GROUP BY team_name, team_shortname
        ORDER BY matches_played DESC
    """
    return pd.read_sql(query, conn) 