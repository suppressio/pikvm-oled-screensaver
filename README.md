
## Quick Start

# PiKVM OLED Demos

Repository of animations and scripts for PiKVM OLED display.

## Quick Install

1. Clone the repository:

```bash
cd /usr/share
sudo git clone https://your-repo-url/ oled_demos
cd oled_demos
```

2. Run installation:

```bash
sudo ./install.sh
```

3. Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable oled-manager
sudo systemctl start oled-manager
```

## Update animations (demos)

```bash
sudo ./fetch_demos.sh
```

## Configuration

File: `/etc/oled-screensaver.conf`
Set screen on/off schedule, contrast, and optional rotation.


