# Hellvape Hotspot Creative Board

Automated daily trending topics dashboard with brand-aligned creative proposals for Hellvape.

## How to use

### Quick Start (Recommended)
1. Fork this repository
2. Add your `hotspot_data.json` file to the root (or update the build script's data source)
3. Enable GitHub Pages: Settings > Pages > Source: GitHub Actions
4. The workflow will run automatically every day

### Manual Update
Edit `hotspot_data.json` directly on GitHub, then trigger manually via Actions tab.

## Files

- `build_dashboard.py` - Generates the HTML from hotspot_data.json
- `hotspot_data.json` - Trend data with creative proposals
- `.github/workflows/daily-hotspot.yml` - GitHub Actions CI/CD

## Schedule

Runs at 01:00 UTC daily (= 09:00 Beijing Time).
