from prometheus_client import Gauge, start_http_server
import urllib3
import json
import os

SONARR_URL = os.environ.get('SONARR_URL')
SONARR_API_KEY = os.environ.get('SONARR_API_KEY')

TOTAL_SERIES = Gauge('sonarr_total_series', 'Total Series in Sonarr')
TOTAL_SERIES_FILES = Gauge('sonarr_total_series_files', 'Total episodes downloaded by sonarr')
TOTAL_EPISODES = Gauge('sonarr_total_episodes', 'Total number of episodes in sonarr')
TOTAL_MISSING_EPISODES = Gauge('sonarr_missing_episodes', 'Total missing episodes in sonarr')

def sonarr_client(path):
    api_call = urllib3.PoolManager()
    headers = {
        "X-Api-Key": SONARR_API_KEY
    }
    try:
        r = api_call.request('GET', SONARR_URL + path, headers=headers)
        return json.loads(r.data)
    except urllib3.exceptions.HTTPError:
        print(f"Cannot complete request")

def total_series():
    data = sonarr_client("/api/series")
    TOTAL_SERIES.set(len(data))

def total_series_files():
    data = sonarr_client("/api/series")
    TOTAL_SERIES_FILES.set(sum(s['episodeFileCount'] for s in data))

def total_episodes():
    data = sonarr_client("/api/series")
    TOTAL_EPISODES.set(sum(s['episodeCount'] for s in data))

def total_missing_episodes():
    data = sonarr_client("/api/series")
    total_episodes = sum(s['episodeCount'] for s in data)
    total_files = sum(s['episodeFileCount'] for s in data)
    TOTAL_MISSING_EPISODES.set(total_episodes - total_files)

if __name__ == '__main__':
    start_http_server(9315, addr='0.0.0.0')
    while True:
        total_series()
        total_series_files()
        total_episodes()
        total_missing_episodes()




