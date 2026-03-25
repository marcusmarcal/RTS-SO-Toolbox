import os
import time
import curses
from dotenv import load_dotenv
from main import PhenixRTS

load_dotenv()

VERSION = "1.3.0"

class ChannelHealthMonitor:
    def __init__(self, interval_seconds: int = 5):
        app_id = os.getenv('PHENIXRTS_APP_ID')
        password = os.getenv('PHENIXRTS_PASSWORD')

        if not app_id or not password:
            raise SystemExit("❌ PHENIXRTS_APP_ID and PHENIXRTS_PASSWORD not found in .env")

        self.phenix = PhenixRTS(app_id, password)
        self.interval = interval_seconds
        self.channels = {}  # channelId -> name

    def load_channels(self):
        """Load all channels from PhenixRTS API and sort them alphabetically by name"""
        ch_list = self.phenix.get_channels()
        self.channels = {
            ch.get("channelId"): ch.get("name", "No name")
            for ch in sorted(ch_list, key=lambda x: x.get("name", "No name").lower())
        }
        return len(self.channels)

    def run(self, stdscr):
        # Curses setup
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.start_color()
        curses.use_default_colors()

        # Color pairs
        curses.init_pair(1, curses.COLOR_CYAN,    -1)  # Title / header
        curses.init_pair(2, curses.COLOR_GREEN,   -1)  # Active
        curses.init_pair(3, curses.COLOR_RED,     -1)  # Inactive / error
        curses.init_pair(4, curses.COLOR_YELLOW,  -1)  # Warning / loading
        curses.init_pair(5, curses.COLOR_WHITE,   -1)  # Normal text
        curses.init_pair(6, curses.COLOR_BLACK,   curses.COLOR_CYAN)   # Header bar
        curses.init_pair(7, curses.COLOR_BLACK,   curses.COLOR_WHITE)  # Footer bar

        COL_CYAN   = curses.color_pair(1)
        COL_GREEN  = curses.color_pair(2)
        COL_RED    = curses.color_pair(3)
        COL_YELLOW = curses.color_pair(4)
        COL_WHITE  = curses.color_pair(5)
        COL_HEADER = curses.color_pair(6)
        COL_FOOTER = curses.color_pair(7)
        BOLD       = curses.A_BOLD

        # Load channels once
        stdscr.clear()
        stdscr.addstr(1, 2, "Loading channels...", COL_YELLOW | BOLD)
        stdscr.refresh()

        try:
            count = self.load_channels()
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(1, 2, f"Error loading channels: {e}", COL_RED | BOLD)
            stdscr.addstr(3, 2, "Press any key to exit.")
            stdscr.nodelay(False)
            stdscr.getch()
            return

        last_refresh = 0
        channel_statuses = {}  # channelId -> (count, error_msg)

        while True:
            # Handle input
            key = stdscr.getch()
            if key in (ord('q'), ord('Q'), 27):
                break

            now = time.time()
            if now - last_refresh >= self.interval:
                # Fetch all channel statuses
                for channel_id in self.channels:
                    try:
                        pub_count = self.phenix.get_publishers_count(channel_id)
                        channel_statuses[channel_id] = (pub_count, None)
                    except Exception as e:
                        channel_statuses[channel_id] = (0, str(e))
                last_refresh = now

            # Draw UI
            stdscr.erase()
            max_y, max_x = stdscr.getmaxyx()

            # ── Header bar ──────────────────────────────────────────────────
            header = f" PhenixRTS Channel Health Monitor  v{VERSION} "
            stdscr.addstr(0, 0, " " * max_x, COL_HEADER)
            stdscr.addstr(0, max(0, (max_x - len(header)) // 2), header, COL_HEADER | BOLD)

            # ── Column headers ───────────────────────────────────────────────
            col_name_w  = max(30, max_x - 30)
            col_pub_w   = 12
            col_stat_w  = 16

            row = 2
            stdscr.addstr(row, 2,  "CHANNEL",    COL_CYAN | BOLD)
            stdscr.addstr(row, col_name_w,        "PUBLISHERS", COL_CYAN | BOLD)
            stdscr.addstr(row, col_name_w + col_pub_w, "STATUS", COL_CYAN | BOLD)
            row += 1
            stdscr.addstr(row, 1, "─" * (max_x - 2), COL_CYAN)
            row += 1

            # ── Channel rows ─────────────────────────────────────────────────
            for channel_id, name in self.channels.items():
                if row >= max_y - 2:
                    stdscr.addstr(row, 2, f"... and more (terminal too small)", COL_YELLOW)
                    row += 1
                    break

                status = channel_statuses.get(channel_id)

                if status is None:
                    # Not yet fetched
                    stdscr.addstr(row, 2, name[:col_name_w - 4], COL_WHITE)
                    stdscr.addstr(row, col_name_w, "---", COL_YELLOW)
                    stdscr.addstr(row, col_name_w + col_pub_w, "LOADING...", COL_YELLOW)

                elif status[1] is not None:
                    # Error
                    err = status[1][:col_stat_w - 1]
                    stdscr.addstr(row, 2, name[:col_name_w - 4], COL_WHITE)
                    stdscr.addstr(row, col_name_w, "ERR", COL_RED | BOLD)
                    stdscr.addstr(row, col_name_w + col_pub_w, err, COL_RED)

                else:
                    pub_count, _ = status
                    has_source = pub_count > 0
                    count_str  = str(pub_count)
                    stat_str   = "SOURCE ACTIVE" if has_source else "NO SOURCE"
                    col_status = COL_GREEN | BOLD if has_source else COL_RED | BOLD

                    stdscr.addstr(row, 2, name[:col_name_w - 4], COL_WHITE)
                    stdscr.addstr(row, col_name_w, count_str, col_status)
                    stdscr.addstr(row, col_name_w + col_pub_w,
                                  ("✓ " if has_source else "✗ ") + stat_str, col_status)

                row += 1

            # ── Separator ────────────────────────────────────────────────────
            if row < max_y - 2:
                stdscr.addstr(row, 1, "─" * (max_x - 2), COL_CYAN)

            # ── Footer bar ───────────────────────────────────────────────────
            ts       = time.strftime("%Y-%m-%d %H:%M:%S")
            next_in  = max(0, int(self.interval - (now - last_refresh)))
            footer   = f"  {ts}   Channels: {len(self.channels)}   Next refresh in {next_in}s   [Q] Quit  "
            footer   = footer[:max_x]
            footer   = footer.ljust(max_x)
            try:
                stdscr.addstr(max_y - 1, 0, footer, COL_FOOTER | BOLD)
            except curses.error:
                pass

            stdscr.refresh()
            time.sleep(0.25)


def main():
    monitor = ChannelHealthMonitor(interval_seconds=5)
    curses.wrapper(monitor.run)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
    except SystemExit as e:
        print(e)
    except Exception as e:
        print(f"Fatal error: {e}")
