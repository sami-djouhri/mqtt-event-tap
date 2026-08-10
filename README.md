# mqtt-event-tap

![CI](https://github.com/sami-djouhri/mqtt-event-tap/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-660066?logo=mqtt&logoColor=white)
![Docker](https://img.shields.io/badge/hardened%20container-2496ED?logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A tiny infrastructure service that subscribes to an entire MQTT topic tree
(`homelab/#`) and prints every message as structured JSON logs.

```mermaid
flowchart LR
  bus[(MQTT homelab/#)] --> tap[tap.py<br/>subscribe]
  tap -->|1 JSON line per message| out[stdout]
  out --> pipe[docker logs / Loki /<br/>any log pipeline]
```

## Why
A passive tap is the simplest way to see what is actually flowing across an event
bus, without touching any publisher or subscriber. Point `docker logs`, Loki or
any log pipeline at it and you get a decoupled, queryable event feed for free.

## Use
- `tap.py` connects to the broker, subscribes to the configured topic tree, and
  emits one JSON line per message
- Configuration is environment-driven: broker host and port, topic, and
  credentials via a mounted secret file

## Container
- **Hardened**: read-only root filesystem, dropped capabilities,
  `no-new-privileges`, memory-limited (64 MB)
- **Healthcheck**: verifies the broker is reachable over TCP

## Stack
- **Python**, paho-mqtt, Docker

MIT licensed.

## About this snapshot

This repository is a curated, secret-free extract from a private source repository.
A script performs the extraction: it drops non-public files, rewrites internal
addresses and paths to placeholders, and requires two independent secret scanners
to pass before anything is pushed.

The development history stays private, which is why you see a single commit here
instead of the real timeline. The code itself is not a demo: it runs in my own
infrastructure and is maintained there.
