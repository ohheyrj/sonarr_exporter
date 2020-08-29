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

QUEUE_SIZE = Gauge('sonarr_queue_size', 'Total items in Sonarr Queue')

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

def series_gauges():
    data = sonarr_client("/api/series")

    total_episodes = sum(s['episodeCount'] for s in data)
    total_files = sum(s['episodeFileCount'] for s in data)

    TOTAL_SERIES.set(len(data))
    TOTAL_SERIES_FILES.set(total_files)
    TOTAL_EPISODES.set(total_episodes)
    TOTAL_MISSING_EPISODES.set(total_episodes - total_files)

def queue_gauges():
    data = sonarr_client("/api/queue")

    QUEUE_SIZE.set(len(data))



if __name__ == '__main__':
    start_http_server(9315, addr='0.0.0.0')
    while True:
        series_gauges()
        queue_gauges()


