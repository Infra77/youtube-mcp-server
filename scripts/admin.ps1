param([ValidateSet('fixture','live')][string]$Mode='fixture',[Parameter(ValueFromRemainingArguments=$true)][string[]]$Command)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$jdk=Get-ChildItem -LiteralPath "$projectRoot/.tools" -Directory -Filter 'jdk-21*' -ErrorAction SilentlyContinue | Select-Object -First 1
$java=if ($jdk) { Join-Path $jdk.FullName 'bin/java.exe' } elseif ($env:JAVA_HOME) { Join-Path $env:JAVA_HOME 'bin/java.exe' } else { 'java' }
if (-not $env:DB_PASSWORD -and (Test-Path "$projectRoot/.local/db-password")) { $env:DB_PASSWORD=(Get-Content "$projectRoot/.local/db-password" -Raw).Trim() }
$env:CURATOR_MODE=$Mode
$socketDir=if ($env:CURATOR_SOCKET_DIR) { $env:CURATOR_SOCKET_DIR } else { "$projectRoot/target" }
$desktopOptions = @()
if ($Command.Count -eq 2 -and $Command[0] -eq 'auth' -and $Command[1] -eq 'login') {
    # Desktop OAuth must be able to open the system browser before Spring initializes AWT.
    $desktopOptions = @('-Djava.awt.headless=false')
}
& $java @desktopOptions "-Djdk.net.unixdomain.tmpdir=$socketDir" -jar "$projectRoot/target/curator.jar" @Command
exit $LASTEXITCODE
