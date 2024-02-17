#!/bin/bash

sudo cp rpi-noctua-fan-control.service /lib/systemd/system
sudo systemctl start rpi-noctua-fan-control.service