import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich import box
from main import PhenixRTS

load_dotenv()

console = Console()

class ChannelHealthMonitor:
    def __init__(self, interval_seconds: int = 1):
        app_id = os.getenv('PHENIXRTS_APP_ID')
        password = os.getenv('PHENIXRTS_PASSWORD')

        if not app_id or not password:
            console.print("[bold red]❌ PHENIXRTS_APP_ID and PHENIXRTS_PASSWORD not found in .env[/]")
            raise SystemExit(1)

        self.phenix = PhenixRTS(app_id, password)
        self.interval = interval_seconds
        self.channels = {}  # channelId -> name

    def load_channels(self):
        """Load all channels from PhenixRTS API"""
        try:
            ch_list = self.phenix.get_channels()
            self.channels = {ch.get("channelId"): ch.get("name", "No name") for ch in ch_list}
            console.print(f"[bold green]✓ Loaded {len(self.channels)} channel(s)[/]")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Error loading channels: {e}[/]")
            return False

    def run(self):
        if not self.load_channels():
            return

        console.clear()
        console.print(Panel("[bold cyan]PhenixRTS - Real-Time Channel Health Monitor[/]", 
                           style="bold blue", box=box.ROUNDED))

        with Live(console=console, refresh_per_second=4, screen=True) as live:
            while True:
                table = Table(title=f"Channel Health - {time.strftime('%H:%M:%S')}", 
                             box=box.ROUNDED, show_lines=True)
                table.add_column("Channel", style="cyan")
                table.add_column("Publishers", justify="center")
                table.add_column("Source Status", justify="center")

                for channel_id, name in self.channels.items():
                    try:
                        count = self.phenix.get_publishers_count(channel_id)
                        has_source = count > 0

                        status_text = "[bold green]✓ SOURCE ACTIVE[/]" if has_source else "[bold red]✗ NO SOURCE[/]"
                        count_text = f"[bold green]{count}[/]" if has_source else f"[bold red]{count}[/]"

                        table.add_row(name, count_text, status_text)

                    except Exception as e:
                        table.add_row(name, "[red]ERROR[/]", f"[red]{e}[/]")

                live.update(Panel(table, title="PhenixRTS Live Monitor (1s refresh)", border_style="blue"))

                time.sleep(self.interval)


if __name__ == "__main__":
    try:
        monitor = ChannelHealthMonitor(interval_seconds=1)   # ← Now 1 second
        monitor.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 Monitor stopped by user.[/]")
    except Exception as e:
        console.print(f"[bold red]Fatal error: {e}[/]")