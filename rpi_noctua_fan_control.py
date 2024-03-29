# AUTHOR: Manuel Lippert (GitHub: ManeLippert)

#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

# The Noctua PWM control actually wants 25 kHz (kilo!), see page 6 on:
# https://noctua.at/pub/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf
# However, the RPi.GPIO library causes high CPU usage when using high
# frequencies - probably because it can currently only do software PWM.
# So we set a lower frequency in the 10s of Hz here. You should expect that
# this value doesn't work very well and adapt it to what works in your setup.
# We will work on the issue and try to use hardware PWM in the future:

# ------------- INFO --------------

INFO = False            # Output informations
WAIT_TIME = 1           # [s] Time to wait between each refresh

# -------------- PWM --------------
 
PWM_FREQ = 25           # [Hz] PWM frequency

FAN_PIN = 15            # BCM pin used to drive PWM fan

OFF_TEMP = 40           # [°C] temperature below which to stop the fan
MIN_TEMP = 50           # [°C] temperature above which to start the fan
MAX_TEMP = 70           # [°C] temperature at which to operate at max fan speed

FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)

# -------------- RPM --------------

TACH_PIN = 14           # Fan's tachometer output pin
PULSE = 2               # Noctua fans puts out two pluses per revolution
RPM = 0
TIME = time.time()

# ----------- FUNCTIONS -----------

# Get temperature
def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000

# Set fan speed
def setFanSpeed(fan, temperature):
    if temperature > MIN_TEMP:
        delta = min(temperature, MAX_TEMP) - MIN_TEMP   # Difference in temperature
        fan.start(FAN_LOW + delta * FAN_GAIN)           # Increase fan speed (for MAX_TEMP fan speed 100)

    elif temperature < OFF_TEMP:
        fan.start(FAN_OFF)                              # Turn fan off if under the duty temperature
        
# Caculate pulse frequency and RPM
def calculateRPM(n):

    global RPM, TIME
    
    dt = time.time() - TIME
    if dt < 0.005:
        return  # Reject spuriously short pulses

    freq = 1 / dt
    RPM = (freq / PULSE) * 60
    TIME = time.time()    

def printHeader():
    print(" TEMP [°C] | RPM       ")
    print("-----------|-----------")

# Get information about system
def printInfo():
    
    global RPM
    TEMP = getCpuTemperature()
        
    print(" {:<9} | {:<9}".format(int(TEMP), int(RPM)))
    RPM = 0 

# -------------- EXE --------------

try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    
    GPIO.setwarnings(False)                             # Do not show any GPIO warnings
    GPIO.setmode(GPIO.BCM)                              # BCM pin numbers - PIN10 as ‘GPIO15’
    
    # -------------- PWM --------------
    
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)     # Initialize GPIO15 as our fan output pin
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)                   # Set GPIO14 as a PWM output, with 25Hz
    
    # -------------- RPM --------------
    
    if INFO:
        GPIO.setup(TACH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # Pull up to 3.3V
        GPIO.add_event_detect(TACH_PIN, GPIO.FALLING, calculateRPM)     # Add event to detect
        printHeader()                                                   # Print tabular header
    
    while True:
        
        setFanSpeed(fan, getCpuTemperature())
        
        if INFO:
            printInfo()
            
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
