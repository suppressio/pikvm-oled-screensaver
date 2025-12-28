#!/bin/bash
set -e

OLED_DIR="/usr/share/kvmd-oled/animations"
GITHUB_REPO="https://github.com/sadotn/luma.oled.examples"
RAW_BASE="https://raw.githubusercontent.com/sadotn/luma.oled.examples/master/examples"

mkdir -p "$OLED_DIR"

echo "Seleziona cosa scaricare:"
echo "1) Demo base (consigliato)"
echo "2) Tutte le demo (richiede risorse aggiuntive)"
read -rp "Scelta [1/2]: " CHOICE

if [ "$CHOICE" == "1" ]; then
    echo "Scarico demo base..."
    # whitelist dei file base verificati
    WHITELIST=("matrix.py" "game_of_life.py")
    for f in "${WHITELIST[@]}"; do
        echo "  -> $f"
        wget -q -O "$OLED_DIR/$f" "$RAW_BASE/$f"
    done
elif [ "$CHOICE" == "2" ]; then
    echo "Scarico tutte le demo (anche sottocartelle)..."
    TMPDIR=$(mktemp -d)
    git clone --depth 1 "$GITHUB_REPO" "$TMPDIR"
    rsync -a --exclude demo_opts.py "$TMPDIR/examples/" "$OLED_DIR/"
    rm -rf "$TMPDIR"
else
    echo "Scelta non valida. Esco."
    exit 1
fi

echo "Download completato."

