Param (
    [string] $PORT = "COM5",
    [string] $IMAGE = "adafruit-circuitpython-doit_esp32_devkit_v1-en_US-8.0.5.bin"
)

#Set-PSDebug -Trace 1

Write-Host ""
Write-Host "info - erasing the contents of the ESP32 board"
Write-Host ""

$esptool = "esptool --chip esp32 --port $PORT --baud 921600"

Invoke-Expression "$esptool erase_flash"

Write-Host ""
Write-Host "info - re-flashing the ESP32 board"
Write-Host ""

Invoke-Expression "$esptool write_flash -z 0x0 $IMAGE"

#Write-Host ""
#Write-Host "info - verifying the flash contents"
#Write-Host ""
#
# $esptool verify_flash 0x0 $IMAGE

Write-Host ""
Write-Host "info - listing the initial board contents"
Write-Host ""

ampy --port $PORT ls

Write-Host ""
Write-Host "info - preparing the Python source to be run"
Write-Host ""

$remove = @(
    "code.py"
)

Foreach ($file in $remove) {
    Write-Host "info - removing '$file'"
    ampy --port $PORT rm $file 
}

$upload = @(
    "safemode.py",
    "adafruit_requests.py",
    "output.py",
    "beacon.py",
    "secrets.py",
    "main.py"
)

Foreach ($file in $upload) {
    Write-Host "info - uploading '$file'"
    ampy --port $PORT put $file 
}

Set-PSDebug -Trace 0

Write-Host ""
Write-Host "info - monitoring device output"
Write-Host ""

./monitor.ps1 -port $PORT

exit
