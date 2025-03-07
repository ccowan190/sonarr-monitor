import requests
import time

# Configuration
SONARR_API_URL = "http://localhost:8989/api/v3"
SONARR_API_KEY = "your-api-key"
CHECK_INTERVAL = 60  # Check every 60 seconds

def get_queue():
    response = requests.get(f"{SONARR_API_URL}/queue", headers={"X-Api-Key": SONARR_API_KEY})
    response.raise_for_status()
    return response.json()

def blocklist_download(download_id):
    response = requests.delete(f"{SONARR_API_URL}/queue/{download_id}", headers={"X-Api-Key": SONARR_API_KEY})
    response.raise_for_status()

def search_again(series_id):
    response = requests.post(f"{SONARR_API_URL}/command", json={"name": "SeriesSearch", "seriesId": series_id}, headers={"X-Api-Key": SONARR_API_KEY})
    response.raise_for_status()

def monitor_sonarr():
    while True:
        print("Checking Sonarr queue...")
        queue = get_queue()
        for item in queue.get("records", []):
            status_messages = item.get("statusMessages", [])
            skip_download = False
            for message in status_messages:
                if "This show has individual episode mappings on TheXEM but the mapping for this episode has not been confirmed yet by their administrators. TheXEM needs manual input." in message.get("messages", []):
                    print(f"Skipping download {item.get('id')} due to pending XEM mapping")
                    skip_download = True
                    break
            if skip_download:
                continue
            if item.get("status") == "failed" or item.get("trackedDownloadState") == "importBlocked":
                download_id = item.get("id")
                series_id = item.get("seriesId")
                print(f"Blocking download {download_id} and searching again for series {series_id}")
                blocklist_download(download_id)
                search_again(series_id)
        print(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_sonarr()