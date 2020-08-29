Sonarr Exporter
====================

![Docker Pulls](https://img.shields.io/docker/pulls/rj170590/sonarr_exporter)

:thinking: What is this?
------------------------
A simple docker image running a exporter for Sonarr to be used with Prometheus

:raised_eyebrow: What does it give me?
--------------------------------------
The exporter provides the following metrics for us within Prometheus:
* `sonarr_total_series` - Total number of series within sonarr
* `sonarr_total_series_files` - Total number downloaded files within Sonarr
* `sonarr_total_episodes` - Total number of episodes over all series
* `sonarr_missing_episodes` - Total number of missing episodes
* `sonarr_queue_size` - Size of Sonarr Queue

:exploding_head: How do I use this?
-----------------------------------
Run docker as follows with these environment variables:

* `SONARR_URL` - The url (including http/https and port) of your sonarr instance. E.g. `https://mysonarr.local`
* `SONARR_API_KEY` - The API key to use with sonarr

On the CLI run:

```bash
docker run -p 9315:9315 -e SONARR_URL=$SONARR_URL -e SONARR_API_KEY=$SONARR_API_KEY rj170590/sonarr_exporter
```

Once running, configure a Prometheus job:

```
- job_name: 'sonarr'
    scrape_interval: 1m
    static_configs:
        - targets: ['172.17.0.1:9315']
```