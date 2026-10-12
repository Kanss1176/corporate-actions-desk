import duckdb
import pytest
from rules import RULES, run_rules

GOOD = dict(company="GOOD", amount=0.5, declared="2026-01-01",
            record_date="2026-01-15", pay_date="2026-02-01",
            link="https://www.sec.gov/Archives/x")

# One deliberately bad row per rule. TEST FIXTURES, not real events.
BAD = {
    "R1 record date before declared date": dict(record_date="2025-12-01", pay_date="2026-01-01"),
    "R2 pay date before record date": dict(pay_date="2026-01-10"),
    "R3 declared date in the future": dict(declared="2999-01-01", record_date="2999-01-15", pay_date="2999-02-01"),
    "R4 amount missing or not positive": dict(amount=0),
    "R5 declared to record gap over 90 days": dict(record_date="2026-06-01", pay_date="2026-06-15"),
    "R6 record to pay gap over 60 days": dict(pay_date="2026-06-01"),
    "R7 source link is not an SEC filing": dict(link="http://example.com"),
}


def make_con(rows):
    con = duckdb.connect(":memory:")
    con.execute("""CREATE TABLE events (company VARCHAR, amount DOUBLE,
                   declared DATE, record_date DATE, pay_date DATE, link VARCHAR)""")
    for r in rows:
        con.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
                    [r["company"], r["amount"], r["declared"],
                     r["record_date"], r["pay_date"], r["link"]])
    return con


def test_good_row_has_no_breaks():
    con = make_con([GOOD])
    assert run_rules(con) == 0


@pytest.mark.parametrize("rule", list(BAD))
def test_each_rule_catches_its_bad_row(rule):
    bad = {**GOOD, **BAD[rule], "company": "BAD"}
    con = make_con([GOOD, bad])
    run_rules(con)
    hits = con.execute(
        "SELECT company FROM breaks WHERE rule = ?", [rule]).fetchall()
    assert hits == [("BAD",)]


def test_every_rule_has_a_test():
    assert set(BAD) == set(RULES)
    