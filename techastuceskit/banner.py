"""banner.py — clears the terminal and shows a clean branded banner
on every launch of the CLI.
"""

import os
import shutil

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# ---- Edit these with your real links ----
AUTHOR = "Styven Emmanuel"
GITHUB_URL = "https://github.com/Styven-Emmanuel-Dev"
WHATSAPP_CHANNEL_URL = "https://whatsapp.com/channel/0029VbCUG0XHltYAlmcp9A3T"
TELEGRAM_URL = "https://t.me/StyvenEmmanuelDev"
BRAND = "TechAstuces Kit"
VERSION = "1.0.0"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    clear_screen()

    if HAS_RICH:
        console = Console()
        width = min(shutil.get_terminal_size().columns, 60)

        title = f"[bold cyan]⚡ {BRAND}[/bold cyan] [dim]v{VERSION}[/dim]"
        body = (
            f"[white]Security & dev toolkit — by [bold]{AUTHOR}[/bold][/white]\n\n"
            f"[green]📢 WhatsApp[/green]  {WHATSAPP_CHANNEL_URL}\n"
            f"[cyan]✈️  Telegram[/cyan]  {TELEGRAM_URL}\n"
            f"[white]🐙 GitHub[/white]    {GITHUB_URL}"
        )

        console.print(
            Panel(
                Align.left(body),
                title=title,
                border_style="cyan",
                width=width,
                padding=(1, 2),
            )
        )
    else:
        print(f"⚡ {BRAND} v{VERSION}")
        print(f"Security & dev toolkit — by {AUTHOR}")
        print(f"📢 WhatsApp : {WHATSAPP_CHANNEL_URL}")
        print(f"✈️  Telegram : {TELEGRAM_URL}")
        print(f"🐙 GitHub   : {GITHUB_URL}")
        print("-" * 50)
