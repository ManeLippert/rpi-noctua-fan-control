#!/bin/bash

sudo cp rpi-noctua-fan-control.service /etc/systemd/system
systemctl enable rpi-noctua-fan-control
sudo systemctl start rpi-noctua-fan-control.service
