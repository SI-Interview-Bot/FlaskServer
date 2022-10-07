function Invoke-WebhookTCPListener
{
  [CmdletBinding(DefaultParameterSetName = 'Start')]
  param (
    [Parameter(ParameterSetName = 'Start')] [string]$Hostname = 'localhost',
    [Parameter(ParameterSetName = 'Start')] [int]$Port = 8088,
    [Parameter(ParameterSetName = 'Start')] [int]$Response = 200 # HTTP response code
  )

  Try {
    $endpoint = New-Object System.Net.IPEndPoint([ipaddress]::any, $Port)
    $server = New-Object System.Net.Sockets.TcpListener($endpoint)
    $server.Start()

    Write-Host "HTTCP Server Ready: http://$($Hostname):$($Port)/ [$($endpoint)]" -f 'black' -b 'green'

    $keepGoing = $True
    while ($keepGoing) {
      $client = $server.AcceptTcpClient()
      $client.ReceiveTimeout = 1000
      $stream = $client.GetStream()
      $bytes = New-Object System.Byte[](65536)
      $req = ""

      $i = 1
      while ($i -ne  0) {
        Try {
          $i = $stream.Read($bytes, 0, $bytes.Length)
        }
        Catch {
          # Exception on receive timeout
          #Write-Host "Error during read?" -f 'red'
          break
        }
        $encoder = New-Object System.Text.ASCIIEncoding
        $req = $req + $encoder.GetString($bytes, 0, $i)
      }
      Write-Host $req -f 'green'

      if ($req.StartsWith("GET /end ")) {
        $keepGoing = $False
      }

      $now = (Get-Date).ToUniversalTime().ToString("r")
      $result = "HTTP/1.1 $($Response) OK`r`nContent-Length: 2`r`nDate: $($now)`r`n"
      $result = "$($result)Server: MS-Sux/1.0`r`nConnection: Close`r`n`r`n{}"
      Write-Host $result -f 'magenta'
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($result)
      $stream.Write($bytes, 0, $bytes.Length)
      $stream.Close()
      $client.Close()
    }

    $server.Stop()
  }
  Catch {
    Write-Host "Server failed with: $($_)`r`n$($_.Exception)" -f 'red'
  }
}
