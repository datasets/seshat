## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: repository had no executable updater workflow despite direct downloadable source assets in README.
- Fixes made: added `scripts/update.py` to sync core Seshat CSV/XLSX assets from documented source URLs with CSV header-shape checks.
- Automation: added first scheduled/manual workflow with explicit `permissions: contents: write` and commit-if-changed behavior.
- Validation: ran updater locally and confirmed output files remain schema-compatible.
