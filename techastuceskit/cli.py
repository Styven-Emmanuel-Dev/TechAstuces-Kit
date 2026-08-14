"""cli.py — main entry point. Dispatches to each tool's subcommand."""

import argparse
import sys

from techastuceskit.banner import show_banner
from techastuceskit import passcheck, filecheck, headers, codestats


def main():
    show_banner()

    parser = argparse.ArgumentParser(
        prog="techastuceskit",
        description="TechAstuces Kit — security & dev toolkit",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("passcheck", help="Password strength audit + HIBP breach check")

    fc = subparsers.add_parser("filecheck", help="File integrity check (hash + change detection)")
    fc.add_argument("path", nargs="?", default=".", help="Directory to scan (default: current directory)")
    fc.add_argument("--init", action="store_true", help="Create the initial baseline")

    hd = subparsers.add_parser("headers", help="Scan a site's HTTP security headers")
    hd.add_argument("url", help="URL to scan, e.g. example.com")

    cs = subparsers.add_parser("codestats", help="Code statistics for a project")
    cs.add_argument("path", nargs="?", default=".", help="Project directory (default: current directory)")

    args = parser.parse_args()

    if args.command == "passcheck":
        passcheck.run()
    elif args.command == "filecheck":
        filecheck.run(args)
    elif args.command == "headers":
        headers.run(args.url)
    elif args.command == "codestats":
        codestats.run(args.path)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
