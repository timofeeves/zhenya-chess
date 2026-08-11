#!/usr/bin/env python3
"""Download one Lichess game as PGN from a shared game URL."""
import re
import sys
import urllib.request
from pathlib import Path

URL = re.compile(r"^https?://(?:www\.)?lichess\.org/([A-Za-z0-9]{8})(?:[A-Za-z0-9]{4})?(?:[/?#].*)?$")

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: import_lichess_game.py <lichess-game-url>")
    match = URL.fullmatch(sys.argv[1].strip())
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
        raise SystemExit("Lichess did not return a PGN for this game.")
    output = Path("games") / f"{game_id}.pgn"
    output.parent.mkdir(exist_ok=True)
    output.write_text(pgn + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
