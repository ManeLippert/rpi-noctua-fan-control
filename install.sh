#!/bin/bash

# Copy service and enable it
sudo cp rpi-noctua-fan-control.service /etc/systemd/system
systemctl enable rpi-noctua-fan-control
sudo systemctl start rpi-noctua-fan-control.service

# Append service to ~/printer_data/moonraker.asvc
echo "rpi-noctua-fan-control" >> ~/printer_data/moonraker.asvc

# Append update manager entry
cat moonraker-config.conf >> ~/printer_data/config/moonraker.conf

