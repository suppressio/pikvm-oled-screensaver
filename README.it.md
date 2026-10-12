🌐 [English](README.md) | **Italiano**

# PiKVM OLED screensaver

Uno screensaver per il piccolo display OLED di un [PiKVM](https://pikvm.org): alterna la solita schermata informativa di PiKVM a un'animazione casuale, così non restano accesi tutto il giorno gli stessi pixel, e di notte abbassa il display.

- Alterna la schermata info di PiKVM (60 s) e un'animazione casuale (30 s); entrambi i tempi si possono cambiare.
- Ore notturne con un contrasto a parte (di default dalle 23:00 alle 07:00 il contrasto scende al minimo).
- Tre animazioni incluse (quadrati che rimbalzano, punti in orbita, pioggia su griglia); altre si possono scaricare dagli [esempi di luma.oled](https://github.com/sadotn/luma.oled.examples).
- Rotazione facoltativa per ogni animazione.

## Installazione

Sul PiKVM, da root. Il file system di PiKVM è in sola lettura: rendilo scrivibile con `rw` prima, e torna indietro con `ro` alla fine.

```bash
rw
git clone https://github.com/suppressio/pikvm-oled-screensaver.git
cd pikvm-oled-screensaver
./install.sh
ro
```

`install.sh` copia il programma in `/usr/share/kvmd-oled/`, scarica `demo_opts.py` (l'aiuto per il display degli esempi luma), poi crea, abilita e avvia il servizio `oled-manager`.

Per aggiungere altre animazioni (prima `rw`): `./fetch_animations.sh` chiede se scaricare solo quelle di base (`matrix`, `game_of_life`) o tutti gli esempi luma.

## Configurazione

File facoltativo `/etc/oled-screensaver.conf`, una `chiave = valore` per riga (`#` per i commenti). Le chiavi assenti mantengono il default.

| Chiave | Default | Significato |
|---|---|---|
| `info_time` | `60` | secondi di schermata info di PiKVM |
| `screensaver_time` | `30` | secondi di animazione |
| `night_off` | `23:00` | inizio della notte |
| `night_on` | `07:00` | fine della notte |
| `contrast_day` | `110` | contrasto di giorno (0–255) |
| `contrast_night` | `0` | contrasto di notte (0 = minimo) |
| `<animazione>_rotate` | `0` | rotazione di una singola animazione, es. `rain_grid_rotate = 2` (0–3, passi di 90°) |

Il file viene letto all'avvio del servizio: dopo una modifica, `systemctl restart oled-manager`.

## Disinstallazione

```bash
rw
systemctl disable --now oled-manager
rm /etc/systemd/system/oled-manager.service
rm -r /usr/share/kvmd-oled/oled_ctl.py /usr/share/kvmd-oled/oled_manager.py /usr/share/kvmd-oled/animations
systemctl daemon-reload
systemctl start kvmd-oled
ro
```
