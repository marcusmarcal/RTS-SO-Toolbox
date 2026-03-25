import os
import time
import curses
from dotenv import load_dotenv
from main import PhenixRTS

load_dotenv()

VERSION = "1.6.0"

class ChannelHealthMonitor:
    def __init__(self, interval_seconds: int = 5):
        app_id = os.getenv('PHENIXRTS_APP_ID')
        password = os.getenv('PHENIXRTS_PASSWORD')

        if not app_id or not password:
            raise SystemExit("❌ PHENIXRTS_APP_ID and PHENIXRTS_PASSWORD not found in .env")

        self.phenix = PhenixRTS(app_id, password)
        self.interval = interval_seconds
        self.channels = {}           # channelId -> {name, alias}
        self.prev_statuses = {}
        self.channel_statuses = {}

    def load_channels(self):
        ch_list = self.phenix.get_channels()
        self.channels = {
            ch.get("channelId"): {
                "name": ch.get("name", "No name"),
                "alias": ch.get("alias") or "-"
            }
            for ch in sorted(ch_list, key=lambda x: x.get("name", "No name").lower())
        }
        return len(self.channels)

    def fetch_statuses(self):
        try:
            ch_list = self.phenix.get_channels()
            new_channels = {
                ch.get("channelId"): {
                    "name": ch.get("name", "No name"),
                    "alias": ch.get("alias") or "-"
                }
                for ch in sorted(ch_list, key=lambda x: x.get("name", "No name").lower())
            }
        except Exception:
            new_channels = self.channels

        channels_changed = new_channels.keys() != self.channels.keys()
        self.channels = new_channels

        new_statuses = {}
        for channel_id in self.channels:
            try:
                pub_count = self.phenix.get_publishers_count(channel_id)
                new_statuses[channel_id] = (pub_count, None)
            except Exception as e:
                new_statuses[channel_id] = (0, str(e))

        return new_statuses, channels_changed

    def has_changes(self, new_statuses):
        if new_statuses.keys() != self.prev_statuses.keys():
            return True
        for cid, val in new_statuses.items():
            if self.prev_statuses.get(cid) != val:
                return True
        return False

    def draw(self, stdscr, max_y, max_x, now, next_in,
             COL_CYAN, COL_GREEN, COL_RED, COL_YELLOW,
             COL_WHITE, COL_HEADER, COL_FOOTER, BOLD):

        stdscr.erase()

        col_name_w  = max(25, max_x - 50)
        col_alias_w = 20
        col_pub_w   = 12

        header = f" PhenixRTS Channel Health Monitor  v{VERSION} "
        stdscr.addstr(0, 0, " " * max_x, COL_HEADER)
        stdscr.addstr(0, max(0, (max_x - len(header)) // 2), header, COL_HEADER | BOLD)

        row = 2
        stdscr.addstr(row, 2, "CHANNEL", COL_CYAN | BOLD)
        stdscr.addstr(row, col_name_w, "ALIAS", COL_CYAN | BOLD)
        stdscr.addstr(row, col_name_w + col_alias_w, "PUBLISHERS", COL_CYAN | BOLD)
        stdscr.addstr(row, col_name_w + col_alias_w + col_pub_w, "STATUS", COL_CYAN | BOLD)

        row += 1
        stdscr.addstr(row, 1, "─" * (max_x - 2), COL_CYAN)
        row += 1

        for channel_id, ch_data in self.channels.items():
            if row >= max_y - 2:
                stdscr.addstr(row, 2, "... terminal too small to show all channels", COL_YELLOW)
                break

            name = ch_data["name"]
            alias = ch_data["alias"]

            status = self.channel_statuses.get(channel_id)

            if status is None:
                stdscr.addstr(row, 2, name[:col_name_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w, alias[:col_alias_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w + col_alias_w, "---", COL_YELLOW)
                stdscr.addstr(row, col_name_w + col_alias_w + col_pub_w, "LOADING...", COL_YELLOW)

            elif status[1] is not None:
                err = status[1][:15]
                stdscr.addstr(row, 2, name[:col_name_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w, alias[:col_alias_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w + col_alias_w, "ERR", COL_RED | BOLD)
                stdscr.addstr(row, col_name_w + col_alias_w + col_pub_w, err, COL_RED)

            else:
                pub_count, _ = status
                has_source = pub_count > 0
                col_status = COL_GREEN | BOLD if has_source else COL_RED | BOLD
                stat_str = "✓ SOURCE ACTIVE" if has_source else "✗ NO SOURCE"

                stdscr.addstr(row, 2, name[:col_name_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w, alias[:col_alias_w - 2], COL_WHITE)
                stdscr.addstr(row, col_name_w + col_alias_w, str(pub_count), col_status)
                stdscr.addstr(row, col_name_w + col_alias_w + col_pub_w, stat_str, col_status)

            row += 1

        if row < max_y - 2:
            stdscr.addstr(row, 1, "─" * (max_x - 2), COL_CYAN)

        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        footer = f"  {ts}   Channels: {len(self.channels)}   Next refresh in {next_in}s   [Q] Quit  "
        footer = footer[:max_x].ljust(max_x)

        try:
            stdscr.addstr(max_y - 1, 0, footer, COL_FOOTER | BOLD)
        except curses.error:
            pass

        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_CYAN,  -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED,   -1)
        curses.init_pair(4, curses.COLOR_YELLOW,-1)
        curses.init_pair(5, curses.COLOR_WHITE, -1)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

        COL_CYAN   = curses.color_pair(1)
        COL_GREEN  = curses.color_pair(2)
        COL_RED    = curses.color_pair(3)
        COL_YELLOW = curses.color_pair(4)
        COL_WHITE  = curses.color_pair(5)
        COL_HEADER = curses.color_pair(6)
        COL_FOOTER = curses.color_pair(7)
        BOLD       = curses.A_BOLD

        draw_colors = (COL_CYAN, COL_GREEN, COL_RED, COL_YELLOW,
                       COL_WHITE, COL_HEADER, COL_FOOTER, BOLD)

        stdscr.clear()
        stdscr.addstr(1, 2, "Loading channels...", COL_YELLOW | BOLD)
        stdscr.refresh()

        try:
            self.load_channels()
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(1, 2, f"Error loading channels: {e}", COL_RED | BOLD)
            stdscr.addstr(3, 2, "Press any key to exit.")
            stdscr.nodelay(False)
            stdscr.getch()
            return

        last_fetch = 0
        last_max_yx = (0, 0)
        last_next_in = -1
        dirty = True

        while True:
            key = stdscr.getch()
            if key in (ord('q'), ord('Q'), 27):
                break

            now = time.time()
            max_yx = stdscr.getmaxyx()
            next_in = max(0, int(self.interval - (now - last_fetch)))

            if now - last_fetch >= self.interval:
                new_statuses, channels_changed = self.fetch_statuses()

                if channels_changed or self.has_changes(new_statuses):
                    self.channel_statuses = new_statuses
                    self.prev_statuses = dict(new_statuses)
                    dirty = True

                last_fetch = now

            if dirty or max_yx != last_max_yx:
                self.draw(stdscr, *max_yx, now, next_in, *draw_colors)
                last_max_yx = max_yx
                last_next_in = next_in
                dirty = False

            elif next_in != last_next_in:
                max_y, max_x = max_yx
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                footer = f"  {ts}   Channels: {len(self.channels)}   Next refresh in {next_in}s   [Q] Quit  "
                footer = footer[:max_x].ljust(max_x)
                try:
                    stdscr.addstr(max_y - 1, 0, footer, COL_FOOTER | BOLD)
                    stdscr.refresh()
                except curses.error:
                    pass
                last_next_in = next_in

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
