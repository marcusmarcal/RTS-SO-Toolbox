# PhenixRTS Real-Time Channel Health Monitor

A clean, fast and modern terminal tool to monitor the health of your PhenixRTS live streams in real time.

## Features

- Automatically loads all channels from the PhenixRTS API
- Real-time monitoring of active sources (publishers count)
- Clear visual status: **✓ SOURCE ACTIVE** or **✗ NO SOURCE**
- Beautiful rich terminal interface with live updates
- Channels automatically sorted alphabetically by name
- Updates every 1 second
- Fully read-only — safe for production environments
- Simple configuration via `.env`

## Requirements

- Python 3.8+
- PhenixRTS App ID and Password

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/marcusmarcal/RTS-SO-Toolbox.git
   cd RTS-SO-Toolbox


   ```

`````markdown
## Usage

Start the monitor:

````bash
python channel_health_monitor.py


---

```markdown
## Version History

| Version | Date       | Changes |
|---------|------------|---------|
| 1.2.0   | 2026-03-25 | Added alphabetical channel sorting |
| 1.1.0   | 2026-03-25 | Full English translation + rich GUI + 1-second refresh |
| 1.0.0   | 2026-03-25 | Initial real-time health monitor |

**Current Version: 1.2.0**

## Important Notes

- This application is **read-only**. It performs only GET requests and cannot stop or affect your live streams.
- Updating every 1 second is safe for typical use. For accounts with a large number of channels, consider increasing the interval.
- Built with the `rich` library for a modern and colorful terminal experience.

## License

MIT License

---

Made for reliable live streaming monitoring
````
`````

```

```
