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

