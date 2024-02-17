# Raspberry Noctua Fan Control`

```
                              GPIO

              [ +3V2  ]-{01}-⬤  ⬤-{02}-[  +5V  ]
              [GPIO 02]-{03}-⬤  ⬤-{04}-[  +5V  ]--{NF +5V (Y)}
              [GPIO 03]-{05}-⬤  ⬤-{06}-[  ---  ]--{NF --- (B)}
              [GPIO 04]-{07}-⬤  ⬤-{08}-[GPIO 14]--{NF RPM (G)}
              [  ---  ]-{09}-⬤  ⬤-{10}-[GPIO 15]--{NF PWM (b)}
              [GPIO 17]-{11}-⬤  ⬤-{12}-[GPIO 18]
              [GPIO 27]-{13}-⬤  ⬤-{14}-[  ---  ]
              [GPIO 22]-{15}-⬤  ⬤-{16}-[GPIO 23]
              [ +3V3  ]-{17}-⬤  ⬤-{18}-[GPIO 24]
              [GPIO 10]-{19}-⬤  ⬤-{20}-[  ---  ]
              [GPIO 09]-{21}-⬤  ⬤-{22}-[GPIO 25]
              [GPIO 11]-{23}-⬤  ⬤-{24}-[GPIO 08]
              [  ---  ]-{25}-⬤  ⬤-{26}-[GPIO 07]
              [ ID_SD ]-{27}-⬤  ⬤-{28}-[ ID_SC ]
              [GPIO 05]-{29}-⬤  ⬤-{30}-[  ---  ]
              [GPIO 06]-{31}-⬤  ⬤-{32}-[GPIO 12]
              [GPIO 13]-{33}-⬤  ⬤-{34}-[  ---  ]
              [GPIO 19]-{35}-⬤  ⬤-{36}-[GPIO 16]
              [GPIO 26]-{37}-⬤  ⬤-{38}-[GPIO 20]
              [  ---  ]-{39}-⬤  ⬤-{40}-[GPIO 21]

NF = Noctua Fan

Colors
B = Black, Y = Yellow, G = Green, b = Blue
```

For quick MainsailOS install run:

```
bash install.sh
```

For manual install:

- Create system service by copying service into ```/etc/systemd/system``` 
  
  ```
  sudo cp rpi-noctua-fan-control.service /etc/systemd/system
  ```

- Enable and start service 

  ```
  systemctl enable rpi-noctua-fan-control
  sudo systemctl start rpi-noctua-fan-control.service
  ```

- Append ```rpi-noctua-fan-control``` to ```~/printer_data/moonraker.asvc```

  ```
  echo "rpi-noctua-fan-control" >> ~/printer_data/moonraker.asvc
  ```

- Append update config to ```~/printer_data/config/moonraker.conf```

  ```
  cat moonraker-config.conf >> ~/printer_data/config/moonraker.conf
  ```

  or copy and paste

  ```
  [update_manager rpi-noctua-fan-control]
  type: git_repo
  path: ~/rpi-noctua-fan-control
  origin: https://github.com/ManeLippert/rpi-noctua-fan-control.git
  managed_services: rpi-noctua-fan-control
  primary_branch: main
  ```

- Restart system

  ```
  sudo reboot now
  ```
