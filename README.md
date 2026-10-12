# Corporate Actions & Proxy Processing Desk

Processing real corporate action events from public SEC filings (EDGAR).
This is a learning project using public data. It is not employer or client data.

## Status
- events.csv, other_events.csv, proxy_meetings.csv: real events read by hand from
  SEC filings (dividends, a merger, a proxy meeting), each with a source link
- desk.duckdb (built by build_db.py): relational tables for the events
- rules.py / checks.py: 7 date-logic controls that write exceptions to a breaks table
- test_rules.py: 9 pytest tests; each rule is shown to catch a deliberately bad
  test row (test fixtures, not real data)
- Result on the real events: 10 events checked, 7 rules, 0 breaks

## Next
- Reconcile each event against a second independent source and log differences
- Maker-checker records, SLA clock, escalation matrix
- Entitlements from 13F holdings, proxy vote reconciliation
- Procedures, UAT log, Excel operations pack


## Next
- Add more events (dividends, a merger or tender, a proxy meeting)
- Reconcile terms against a second source and log differences
- Procedures, test log and Excel operations pack
