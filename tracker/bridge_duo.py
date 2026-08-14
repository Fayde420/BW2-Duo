"""
═══════════════════════════════════════════════════════════
  AutoTracker-Brücke (Duo-Soullink)  state.json → Firebase

  Liest die lokale state.json (vom Lua-Skript erzeugt) und
  pusht sie in den Duo-Run unter dem Slot des jeweiligen
  Spielers. Feste Slots: p1 / p2 (die Anzeigenamen setzt man
  pro Run auf der Duo-Seite selbst).

  Aufruf:
    python bridge_duo.py --player p1
    python bridge_duo.py --player p2

  Firebase-Pfad:  /{runId}/autoTeam_{player}   (DB: bw2-duo)
═══════════════════════════════════════════════════════════
"""
from __future__ import annotations
import os
import argparse
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ── Konfiguration ──
FIREBASE_URL  = "https://bw2-duo-default-rtdb.europe-west1.firebasedatabase.app"
# state.json-Ort universell (wie live_team.lua / bridge.py): Umgebungsvariable
# AUTOTRACKER_DIR, sonst neben diesem Skript. Mit --state überschreibbar.
_ATDIR        = os.environ.get("AUTOTRACKER_DIR")
DEFAULT_STATE = (Path(_ATDIR) if _ATDIR else Path(__file__).resolve().parent) / "state.json"
DEFAULT_RUN   = "duo"             # selbe Default-ID wie im Duo-Frontend
POLL_INTERVAL = 0.5               # Sekunden
RUN_CHECK_INTERVAL = 3.0          # Sekunden zwischen aktiv-Run-Polls
VALID_PLAYERS = ("p1", "p2")

# Laufzeit-Zustand
_current_run_id = DEFAULT_RUN
_last_run_check = 0.0


def fetch_active_run() -> None:
    """Liest /_active_run aus Firebase und aktualisiert _current_run_id."""
    global _current_run_id, _last_run_check
    _last_run_check = time.time()
    url = f"{FIREBASE_URL}/_active_run.json"
    try:
        with urllib.request.urlopen(url, timeout=3) as res:
            body = res.read().decode("utf-8")
        new_run = json.loads(body) if body and body != "null" else None
        if isinstance(new_run, str) and new_run and new_run != _current_run_id:
            print(f"[INFO] Aktiver Run gewechselt: {_current_run_id}  →  {new_run}")
            _current_run_id = new_run
    except Exception:
        pass  # silent fail – aktiver Run optional


def push(state_text: str, player: str, force_run: str | None) -> None:
    """Validiert state.json und schiebt sie unter autoTeam_{player} hoch."""
    try:
        d = json.loads(state_text)
    except json.JSONDecodeError:
        return  # Lua mitten im Schreiben – nächste Runde

    if force_run is None and time.time() - _last_run_check > RUN_CHECK_INTERVAL:
        fetch_active_run()
    run_id = force_run or _current_run_id

    # Server-Zeitstempel mitschicken: 'updatedAt' aus der Lua ist die Uhr
    # DIESES PCs. Geht sie falsch, zeigt die Website faelschlich "offline".
    # {".sv":"timestamp"} laesst Firebase die Zeit selbst setzen.
    d["serverAt"] = {".sv": "timestamp"}
    payload = json.dumps(d).encode("utf-8")
    url = f"{FIREBASE_URL}/{run_id}/autoTeam_{player}.json"
    req = urllib.request.Request(url, data=payload, method="PUT")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            res.read()
        ts = datetime.now().strftime("%H:%M:%S")
        print(
            f"[{ts}] OK  Run={run_id[-12:]:<12} Player={player:<4} "
            f"Team={d.get('teamCount', '?')} Map={d.get('mapHeader', '?')}"
        )
    except urllib.error.HTTPError as e:
        print(f"!! Firebase HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"!! Netzwerk: {e.reason}")
    except Exception as e:
        print(f"!! Fehler: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Duo-Soullink Bridge")
    parser.add_argument(
        "--player", required=True, choices=VALID_PLAYERS,
        help="Fester Slot p1 oder p2 (Anzeigename kommt aus dem Run)."
    )
    parser.add_argument(
        "--run", default=None,
        help=f"Fix-Run-ID (überschreibt _active_run-Polling). Default: '{DEFAULT_RUN}' "
             "bzw. Wert aus /_active_run, falls vorhanden."
    )
    parser.add_argument(
        "--state", default=str(DEFAULT_STATE), type=Path,
        help=f"Pfad zur state.json. Default: {DEFAULT_STATE}"
    )
    args = parser.parse_args()
    player = args.player
    state_file: Path = args.state
    force_run: str | None = args.run

    print("== AutoTracker-Brücke (Duo) ==")
    print(f"Spieler:    {player}")
    print(f"Beobachte:  {state_file}")
    if force_run:
        print(f"Run-ID:     {force_run}  (fixiert via --run)")
    else:
        fetch_active_run()
        print(f"Run-ID:     {_current_run_id}  (aus _active_run / Default)")
    print(f"Firebase:   {FIREBASE_URL}/<runId>/autoTeam_{player}")
    print("Warte auf das Lua-Skript ... (Strg+C zum Beenden)\n")

    last_mtime = 0.0
    while True:
        try:
            if state_file.exists():
                mtime = state_file.stat().st_mtime
                if mtime != last_mtime:
                    last_mtime = mtime
                    time.sleep(0.05)  # Race gegen Lua-Rename abfangen
                    try:
                        text = state_file.read_text(encoding="utf-8")
                        push(text, player, force_run)
                    except FileNotFoundError:
                        pass
        except KeyboardInterrupt:
            print("\nBrücke gestoppt.")
            return
        except Exception as e:
            print(f"!! Watch-Fehler: {e}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
