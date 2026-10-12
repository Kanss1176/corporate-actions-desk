import duckdb

con = duckdb.connect("desk.duckdb")

files = {
    "events": "events.csv",
    "other_events": "other_events.csv",
    "proxy_meetings": "proxy_meetings.csv",
}

for table, path in files.items():
    con.execute(
        f"CREATE OR REPLACE TABLE {table} AS "
        f"SELECT * FROM read_csv_auto('{path}', header=true)"
    )
    n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"\n{table}: {n} rows")
    for col, dtype, *_ in con.execute(f"DESCRIBE {table}").fetchall():
        print(f"  - {col} ({dtype})")