import duckdb

con = duckdb.connect("desk.duckdb")

print("events:", con.execute("SELECT COUNT(*) FROM events").fetchone()[0], "rows")
for col, dtype, *_ in con.execute("DESCRIBE events").fetchall():
    print(" -", col, f"({dtype})")

print()
print(con.execute("SELECT * EXCLUDE (link) FROM events").df().to_string())