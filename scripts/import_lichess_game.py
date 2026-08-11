#!/usr/bin/env python3
"""Download Lichess games as PGN from URLs or request files."""
import re
import sys
import urllib.request
from pathlib import Path

URL = re.compile(r"^https?://(?:www\.)?lichess\.org/([A-Za-z0-9]{8})(?:[A-Za-z0-9]{4})?(?:[/?#].*)?$")

def import_game(game_url: str) -> Path:
    match = URL.fullmatch(game_url.strip())
    if not match:
        raise SystemExit("Expected a Lichess game URL.")
    game_id = match.group(1)
    request = urllib.request.Request(
        f"https://lichess.org/game/export/{game_id}",
        headers={"Accept": "application/x-chess-pgn", "User-Agent": "zhenya-chess-importer"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        pgn = response.read().decode("utf-8").strip()
    if not pgn or not pgn.startswith("[Event "):
        raise SystemExit(f"Lichess did not return a PGN for {game_id}.")
    output = Path("games") / f"{game_id}.pgn"
    output.parent.mkdir(exist_ok=True)
    output.write_text(pgn + "\n", encoding="utf-8")
    return output

def request_urls() -> list[str]:
    urls: list[str] = []
    for request_file in sorted(Path("requests").glob("*.txt")):
        urls.extend(
            line.strip()
            for line in request_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    return urls

def main() -> None:
    urls = sys.argv[1:] or request_urls()
    if not urls:
        raise SystemExit("Pass a Lichess URL or add it to requests/*.txt.")
    for game_url in urls:
        print(import_game(game_url))

if __name__ == "__main__":
    main()
