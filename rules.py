RULES = {
    "R1 record date before declared date": (
        "High", "record_date < declared",
        "record_date || ' is before declared ' || declared"),
    "R2 pay date before record date": (
        "High", "pay_date < record_date",
        "pay_date || ' is before record ' || record_date"),
    "R3 declared date in the future": (
        "Medium", "declared > CURRENT_DATE",
        "'declared date is after today'"),
    "R4 amount missing or not positive": (
        "High", "amount IS NULL OR amount <= 0",
        "'amount is missing or not positive'"),
    "R5 declared to record gap over 90 days": (
        "Low", "date_diff('day', declared, record_date) > 90",
        "'gap is unusually long'"),
    "R6 record to pay gap over 60 days": (
        "Low", "date_diff('day', record_date, pay_date) > 60",
        "'gap is unusually long'"),
    "R7 source link is not an SEC filing": (
        "Medium",
        "link IS NULL OR link NOT LIKE 'https://www.sec.gov/Archives/%'",
        "'link missing or not from sec.gov'"),
}


def run_rules(con):
    """Create the breaks table, run every rule on events, return break count."""
    con.execute("""
        CREATE OR REPLACE TABLE breaks (
            break_id INTEGER, company VARCHAR, rule VARCHAR,
            severity VARCHAR, detail VARCHAR,
            detected_on DATE, status VARCHAR
        )
    """)
    for rule, (severity, condition, detail) in RULES.items():
        con.execute(f"""
            INSERT INTO breaks
            SELECT COALESCE((SELECT MAX(break_id) FROM breaks), 0) + 1,
                   company, '{rule}', '{severity}', {detail},
                   CURRENT_DATE, 'Open'
            FROM events WHERE {condition}
        """)
    return con.execute("SELECT COUNT(*) FROM breaks").fetchone()[0]
