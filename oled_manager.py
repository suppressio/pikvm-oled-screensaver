#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import signal
import os
from pathlib import Path
from oled_ctl import fade
from datetime import datetime

# --- Config ---
CONFIG_FILE = "/etc/oled-screensaver.conf"
ANIM_DIR = Path("/usr/share/kvmd-oled/animations")
INFO_SERVICE = "kvmd-oled"
BLACKLIST = ["demo_opts.py"]

# --- Lettura config ---
def read_config(key, default=None):
    if not os.path.exists(CONFIG_FILE):
        return default
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip()
    return default

INFO_TIME = int(read_config("info_time", 60))
SCREENSAVER_TIME = int(read_config("screensaver_time", 30))
NIGHT_OFF = read_config("night_off", "23:00")
NIGHT_ON = read_config("night_on", "07:00")
CONTRAST_DAY = int(read_config("contrast_day", 110))
CONTRAST_NIGHT = int(read_config("contrast_night", 0))

# --- Global screensaver process ---
current_screensaver = None

def start_info():
    os.system(f"systemctl start {INFO_SERVICE} 2>/dev/null")
    fade(CONTRAST_DAY)

def stop_info():
    os.system(f"systemctl stop {INFO_SERVICE} 2>/dev/null")

def launch_screensaver(script_path, rotate=0):
    global current_screensaver
    current_screensaver = subprocess.Popen(
        ["python3", str(script_path), "--rotate", str(rotate)]
    )

def stop_screensaver():
    global current_screensaver
    if current_screensaver:
        current_screensaver.terminate()
        try:
            current_screensaver.wait(timeout=5)
        except subprocess.TimeoutExpired:
            current_screensaver.kill()
        current_screensaver = None

def is_night():
    now = datetime.now().strftime("%H:%M")
    return now > NIGHT_OFF or now < NIGHT_ON

def signal_handler(sig, frame):
    stop_info()
    stop_screensaver()
    fade(CONTRAST_DAY)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- Main loop ---
while True:
    if is_night():
        fade(CONTRAST_NIGHT)
        time.sleep(60)
        continue

    # Mostra info KVM
    start_info()
    time.sleep(INFO_TIME)
    stop_info()

    # Sceglie uno screensaver casuale
    scripts = [
        f for f in ANIM_DIR.glob("*.py")
        if f.name not in BLACKLIST
    ]    
    if not scripts:
        continue
    scr = scripts[int(time.time()) % len(scripts)]

    # Rotazione opzionale
    rotate_val = int(read_config(f"{scr.stem}_rotate", 0))

    # Lancia screensaver
    launch_screensaver(scr, rotate_val)
    time.sleep(SCREENSAVER_TIME)
    stop_screensaver()

