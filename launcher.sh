#!/bin/sh
#launcher.sh
# Désactive les ports USB, navigue jusqu'au dossier TrackSwim_Codes et execute TS_main.py

echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind

cd /
cd home/tspi/TrackSwim_Codes
python3 TS_main.py
cd /