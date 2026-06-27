# BW2-Duo

Live-Tracker-Webseite für einen **Duo-Soullink** in Pokémon Schwarz 2 — abgeleitet
aus dem Trio-Tracker ([BW2-Tracker](https://github.com/Fayde420/BW2-Tracker)),
reduziert auf **zwei Spieler**.

Live (nach Pages-Aktivierung): https://fayde420.github.io/BW2-Duo/

## Einrichtung (noch offen)

Die Seite läuft erst, wenn eine eigene Firebase-Realtime-DB hinterlegt ist:

1. **Firebase-Projekt** anlegen → Realtime Database erstellen.
2. In `index.html` den Block `const firebaseConfig = { … }` ausfüllen
   (alle `TODO_DUO_*`-Platzhalter ersetzen).
3. **Spieler anpassen** (drei Stellen, gleiche `slot`-Keys verwenden):
   - `const PLAYERS = ['p1','p2'];`
   - `const PLAYER_LABELS = { p1:'Spieler 1', p2:'Spieler 2' };`
   - `const LIVE_PLAYERS = [ { slot:'p1', … }, { slot:'p2', … } ];`
4. **Bridge:** Jeder Spieler startet `bridge_trio.py --player <slot>` (z.B. `p1`).
   Hinweis: In `bridge_trio.py` muss `VALID_PLAYERS` die gewählten Slots
   enthalten.

Der RAM-Tracker (`live_team.lua`) + die Bridge liegen unverändert im
[BW2-Tracker](https://github.com/Fayde420/BW2-Tracker)-Repo.
