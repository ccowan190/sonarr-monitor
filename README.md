# Sonarr Monitor

A Python utility that monitors your Sonarr queue and automatically manages downloads based on specific conditions.

## Features

- Monitors Sonarr queue continuously
- Automatically handles failed downloads by:
  - Adding them to the blocklist
  - Triggering a new search for the affected series
- Skips downloads with pending XEM mappings to prevent incorrect episode matching
- Configurable check interval

## Requirements

- Python 3.x
- `requests` library
- Running Sonarr instance with API access

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install requests
```

## Configuration

Edit `sonarr-monitor/sonarr-monitor.py` and update the following variables:

```python
SONARR_API_URL = "http://localhost:8989/api/v3"  # Update with your Sonarr URL
SONARR_API_KEY = "your-api-key"
CHECK_INTERVAL = 60  # Adjust check frequency (in seconds)
```

To find your Sonarr API key:
1. Open Sonarr web interface
2. Go to Settings -> General
3. Look for "API Key" in the "Security" section

⚠️ **Security Note**: Never commit your actual API key to version control. Consider using environment variables or a configuration file for sensitive data.

## Usage

Run the script using Python:

```bash
python sonarr-monitor/sonarr-monitor.py
```

The script will:
1. Check your Sonarr queue every 60 seconds (configurable)
2. Look for failed downloads or import-blocked items
3. Handle any pending XEM mapping issues
4. Automatically retry failed downloads with a new search

To run in the background, consider using a process manager like systemd, supervisor, or running it in a screen/tmux session.

## How It Works

1. The script queries Sonarr's queue API endpoint at regular intervals
2. For each item in the queue:
   - If there's a pending XEM mapping, it skips the download to prevent incorrect episode matching
   - If the download has failed or is blocked from importing, it:
     - Adds the download to the blocklist
     - Triggers a new search for that series

This helps maintain your download queue by automatically handling common issues that might prevent successful downloads.