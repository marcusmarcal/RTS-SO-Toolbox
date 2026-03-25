# PhenixRTS Real-Time Channel Health Monitor

A clean, fast and modern terminal tool to monitor the health of your PhenixRTS live streams in real time.

---

## Features

- Automatically loads all channels from the PhenixRTS API  
- Real-time monitoring of active sources (publishers count)  
- Clear visual status: **✓ SOURCE ACTIVE** or **✗ NO SOURCE**  
- Beautiful rich terminal interface with live updates  
- Channels automatically sorted alphabetically by name  
- Updates every 1 second  
- Fully read-only — safe for production environments  
- Simple configuration via `.env`  

---

## Requirements

- Python 3.8+  
- PhenixRTS App ID and Password  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/marcusmarcal/RTS-SO-Toolbox.git
cd RTS-SO-Toolbox
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

4. Edit `.env` with your credentials:

```env
PHENIXRTS_APP_ID=your_app_id_here
PHENIXRTS_PASSWORD=your_password_here
```

---

## Usage

Start the monitor:

```bash
python channel_health_monitor.py
```

The tool will:

- Load and sort all your channels alphabetically  
- Display a live updating table  
- Show real-time source status for each channel  

Press `Ctrl + C` to stop monitoring.

---

## Project Structure

```text
RTS-SO-Toolbox/
├── main.py                    # PhenixRTS API client
├── channel_health_monitor.py  # Real-time monitor with rich UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Version History

| Version | Date       | Changes                                              |
|--------|-----------|------------------------------------------------------|
| 1.2.0  | 2026-03-25 | Added alphabetical channel sorting                  |
| 1.1.0  | 2026-03-25 | Full English translation + rich UI + 1s refresh     |
| 1.0.0  | 2026-03-25 | Initial real-time health monitor                    |

**Current Version:** 1.2.0

---

## Important Notes

- This application is read-only. It performs only GET requests and cannot stop or affect your live streams.  
- Updating every 1 second is safe for typical use. For accounts with a large number of channels, consider increasing the interval.  
- Built with the `rich` library for a modern and colorful terminal experience.  

---

## License

MIT License

---

Made for reliable live streaming monitoring 🚀
