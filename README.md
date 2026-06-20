<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&pause=1000&color=C8102E&center=true&vCenter=true&width=600&lines=F1+Live+Telemetry+Dashboard;Real+race+data.+Updated+live.;Built+from+scratch+to+learn.)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Backend-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Live%20Updates-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

![GitHub last commit](https://img.shields.io/github/last-commit/r2meen/Formula-One-Telemetry-?style=flat-square&color=C8102E)
![GitHub repo size](https://img.shields.io/github/repo-size/r2meen/Formula-One-Telemetry-?style=flat-square&color=1F4E5F)
![GitHub stars](https://img.shields.io/github/stars/r2meen/Formula-One-Telemetry-?style=flat-square&color=yellow)

</div>

A web app that shows real Formula 1 race data — lap times, positions, and intervals — updating live in the browser while a real Grand Prix is happening. Built from scratch as a learning project.

> **Note:** This project pulls real-world F1 data from a public API. 

## What This Is

This project fetches live and historical Formula 1 session data from [OpenF1](https://openf1.org/) — a free, public, real-world F1 data API — and displays it as a live-updating dashboard.

## Tech Stack

| Layer | Choice |
|---|---|
| Data source | [OpenF1 API](https://openf1.org/) (free, public, real F1 data) |
| Data fetching | Python script that polls OpenF1 for updates every few seconds |
| Backend | Django (Python) |
| Live updates | Django Channels + Redis |
| Database | MySQL |
| Frontend | Django templates + a small amount of plain JavaScript (no React) |

## Architecture

This project uses two architectural patterns at different layers:

- **Pipe-and-filter** — the data pipeline itself. Data passes through a series of stages, and each stage transforms it before handing it to the next: fetch → process → store/broadcast → display.
- **MTV (Django's MVC)** — the web application layer. This comes automatically from using Django, which structures apps as Models, Templates, and Views.

### Data Flow

```
OpenF1 API (free, public, real F1 data)
    |   our backend asks: "anything new?" every few seconds
    v
[1] Poller  (Python script, runs on a timer)
    |
    v
[2] Processor  (compares to last check — what changed?)
    |                                   |
    v                                   v
[3a] MySQL                      [3b] Redis -> Django Channels
(sessions, laps, results)               |
                                         v
                                 Browser (live dashboard,
                                 Django template + JavaScript)
```

**Why polling instead of instant push?** True real-time push streaming from OpenF1 requires a paid/sponsor account. The free tier works by polling — our code asks "anything new?" every few seconds instead of being notified instantly. A few seconds of delay is unnoticeable for this kind of dashboard, and it's far simpler to build first. This can be upgraded to push later without changing the rest of the system.

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Git

### Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/r2meen/Formula-One-Telemetry-.git
   cd Formula-One-Telemetry-
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run a test script to confirm everything's working:
   ```bash
   python test_openf1.py
   ```
   You should see `Status code: 200` followed by real F1 session data.

## Project Status

This project is in early development. Progress so far:

- [x] Python environment set up
- [x] Confirmed connection to OpenF1 API (sessions endpoint)
- [x] Confirmed lap data can be fetched (laps endpoint)
- [x] Basic polling loop that checks for new data every few seconds
- [ ] Django project setup
- [ ] MySQL database and models
- [ ] Save polled data to the database
- [ ] Django Channels + Redis for live updates
- [ ] Dashboard frontend

## How We're Working

This is a two-person learning project, built pair-programming style — working through the code together rather than splitting into separate halves for now.

## Data Source Credit

Race data provided by [OpenF1](https://openf1.org/), a free and open-source Formula 1 data API. OpenF1 is an unofficial project and is not associated with Formula 1 companies.
