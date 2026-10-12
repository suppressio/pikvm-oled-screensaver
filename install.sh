#!/bin/bash
set -e

OLED_DIR="/usr/share/kvmd-oled"
SERVICE_FILE="/etc/systemd/system/oled-manager.service"

echo "Creazione cartelle..."
mkdir -p "$OLED_DIR/animations"

echo "Copia dei file..."
cp oled_ctl.py "$OLED_DIR/"
cp oled_manager.py "$OLED_DIR/"
cp animations/demo_opts.py "$OLED_DIR/animations/"
# Proposta da provare sul PiKVM: demo_opts.py non è nel repository (lo scarica
# il wget qui sotto), quindi con set -e la riga sopra ferma l'installazione su
# un clone pulito; questa copia invece le animazioni incluse.
# cp animations/*.py "$OLED_DIR/animations/"

echo "Scarico demo_opts.py aggiornato da GitHub..."
wget -q -O "$OLED_DIR/animations/demo_opts.py" \
    https://raw.githubusercontent.com/sadotn/luma.oled.examples/master/examples/demo_opts.py

echo "Creazione systemd service..."
cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=PiKVM OLED Manager
After=kvmd.service

[Service]
WorkingDirectory=$OLED_DIR
ExecStart=/usr/bin/python3 -m oled_manager
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Ricarico systemd e abilito il servizio..."
systemctl daemon-reload
systemctl enable oled-manager
systemctl start oled-manager

echo "Installazione completata."

