🌐 **English** | [Italiano](README.it.md)

# PiKVM OLED screensaver

A screensaver for the small OLED display of a [PiKVM](https://pikvm.org): it alternates the usual PiKVM information screen with a random animation, so the same pixels are not lit all day, and dims the display at night.

- Alternates the PiKVM info screen (60 s) and a random animation (30 s); both times can be changed.
- Night hours with their own contrast (by default the contrast drops to the minimum from 23:00 to 07:00).
- Three animations included (bouncing squares, orbiting dots, rain grid); more can be downloaded from the [luma.oled examples](https://github.com/sadotn/luma.oled.examples).
- Optional rotation per animation.

## Install

On the PiKVM, as root. The PiKVM file system is read-only: make it writable with `rw` first, and go back with `ro` at the end.

```bash
rw
git clone https://github.com/suppressio/pikvm-oled-screensaver.git
cd pikvm-oled-screensaver
./install.sh
ro
```

`install.sh` copies the program and the animations to `/usr/share/kvmd-oled/`, downloads `demo_opts.py` (the display helper of the luma examples), then creates, enables and starts the `oled-manager` service.

To add more animations (`rw` first): `./fetch_animations.sh` asks whether to download only the basic ones (`matrix`, `game_of_life`) or all the luma examples.

## Configuration

Optional file `/etc/oled-screensaver.conf`, one `key = value` per line (`#` for comments). Missing keys keep their default.

| Key | Default | Meaning |
|---|---|---|
| `info_time` | `60` | seconds of PiKVM info screen |
| `screensaver_time` | `30` | seconds of animation |
| `night_off` | `23:00` | start of the night |
| `night_on` | `07:00` | end of the night |
| `contrast_day` | `110` | daytime contrast (0–255) |
| `contrast_night` | `0` | night contrast (0 = minimum) |
| `<animation>_rotate` | `0` | rotation of one animation, e.g. `rain_grid_rotate = 2` (0–3, steps of 90°) |

The file is read when the service starts: `systemctl restart oled-manager` after a change.

## Uninstall

```bash
rw
systemctl disable --now oled-manager
rm /etc/systemd/system/oled-manager.service
rm -r /usr/share/kvmd-oled/oled_ctl.py /usr/share/kvmd-oled/oled_manager.py /usr/share/kvmd-oled/animations
systemctl daemon-reload
systemctl start kvmd-oled
ro
```
