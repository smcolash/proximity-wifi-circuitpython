Param (
    $PORT = "COM5"
)

Set-PSDebug -Trace 0

$port = new-Object System.IO.Ports.SerialPort $PORT,115200,None,8,one
$port.Open()

try {
    do {
        $line = $port.ReadLine().Replace("\r\n", "")
        Write-Host $line
    } while ($port.IsOpen)
}
finally {
    $port.Close()
}

exit
