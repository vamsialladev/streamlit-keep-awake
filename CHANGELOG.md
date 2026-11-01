# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.2.0] - 2026-10-25

### Added

- Every visit adds `?source=keepawake`, so the hotel apps run nothing, log nothing and leave the database asleep.
- Daily failure summary workflow: reads the shared ops log read-only and opens an issue (or posts to Slack) when an
  app's error rate passes 5% or nothing succeeded.

### Changed

- Apps are visited three at a time, each in its own browser; the job's timeout is 40 minutes.

## [1.1.0] - 2026-10-25

### Added

- README in the portfolio's standard order, architecture and sequence diagrams.
- Unit tests for the app list and the awake / asleep / stays-asleep decisions; CI (ruff, pytest, pip-audit, lychee,
  gitleaks); pinned Playwright; LICENSE, SECURITY, decisions.

## [1.0.0] - 2026-10-24

### Added

- Scheduled browser visits to the Streamlit apps every 4 hours, wake button click, screenshots, monthly keepalive
  commit.
