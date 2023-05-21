# proximity-wifi-circuitpython
WiFi-based proximity trigger for IoT devices, written for ESP32 devices in CircuitPython.

# Notes

There are many different types of ESP32 boards, and CircuitPython is built specific to some
of those boards. Not all CircuitPython builds (the kernel/flash) are compatible with
all ESP32 boards.

Flashing the wrong kernel will not likely cause any damage to your board, but it
just might not work. You may see boot errors, reboot cycles, complaint of illegal instructions,
etc. if there is a mismatch of board and kernel.

The code presented here has been specifically used on and tested with an ESP32 'doit'
style board, flashed from a Windows 10 laptop, over a serial connection on COM5. You
will see most of those details as overridable parameters in the 'reflash.ps1' and
'monitor.ps1' PowerShell scripts.
