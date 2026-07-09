# BW2-Duo — Live-Tracker (Duo-Soullink)

Live-Anzeige eines **2-Spieler-Soullinks** in Pokémon Schwarz 2: Teams, PC-Box,
aktueller Gegner (folgt automatisch dem Kampf), Routen und Orden — direkt aus
dem laufenden Spiel.

**Live:** https://fayde420.github.io/BW2-Duo/  (Passwort erforderlich)

## Mitspielen — Tracker einrichten
Du brauchst: **BizHawk** (melonDS-Core), dein **BW2-ROM**, **Python 3**.

1. Den Ordner **`tracker/`** herunterladen.
2. In der CMD einmalig den Ordner festlegen — **Pfad an deinen echten
   tracker-Ordner anpassen** (nicht wörtlich übernehmen!). Danach CMD **und**
   BizHawk neu starten, sonst greift die Variable nicht:
   ```cmd
   setx AUTOTRACKER_DIR "C:\Pfad\zum\tracker"
   ```
3. BizHawk → ROM laden → **Tools → Lua Console** → `live_team.lua` laden
   (Konsole zeigt `state.json → <dein Ordner>`).
4. Bridge starten — jeder Spieler hat einen festen Slot:
   - **Spieler 1:** `start_duo_p1.bat`  (= `python bridge_duo.py --player p1`)
   - **Spieler 2:** `start_duo_p2.bat`  (= `--player p2`)
5. Diese Seite öffnen (Passwort eingeben) → oben auf den **Spielernamen
   klicken** und den echten Namen eintragen. Die Namen sind **pro Run frei
   wählbar**.

Fertig — die Daten erscheinen live.

## Hinweise
- Die Firebase-DB ist offen (kein Login) — teile die URL nicht breit.
- BW2-ROM & BizHawk sind nicht enthalten (besorgst du selbst).
