# utils/oled_ctl.py
import time

# Import relativo verso demo_opts nella cartella animations
from animations.demo_opts import get_device

_device = None

def device():
    """Restituisce l'istanza del dispositivo OLED"""
    global _device
    if _device is None:
        _device = get_device()
    return _device

def clear():
    """Pulisce lo schermo"""
    device().clear()

def set_contrast(value: int):
    """Imposta il contrasto"""
    device().contrast(int(value))

def fade(target: int, step=5, delay=0.05):
    """Effettua il fade del contrasto fino al valore target"""
    d = device()
    try:
        current = d._contrast
    except AttributeError:
        current = target
    direction = 1 if target > current else -1
    for v in range(current, target + direction, direction * step):
        d.contrast(max(0, min(255, v)))
        time.sleep(delay)

def status():
    """Mostra informazioni sul display"""
    d = device()
    print(f"OLED {d.width}x{d.height} contrast={getattr(d, '_contrast', 'unknown')}")

