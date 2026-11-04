param([ValidateSet('fixture','live')][string]$Mode='fixture')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$jdk=Get-ChildItem -LiteralPath "$projectRoot/.tools" -Directory -Filter 'jdk-21*' -ErrorAction SilentlyContinue | Select-Object -First 1
$java=if ($jdk) { Join-Path $jdk.FullName 'bin/java.exe' } elseif ($env:JAVA_HOME) { Join-Path $env:JAVA_HOME 'bin/java.exe' } else { 'java' }
if (-not $env:DB_PASSWORD -and (Test-Path "$projectRoot/.local/db-password")) { $env:DB_PASSWORD=(Get-Content "$projectRoot/.local/db-password" -Raw).Trim() }
if (-not $env:DB_PASSWORD) { throw 'DB_PASSWORD is required.' }
$env:CURATOR_MODE=$Mode
if (-not $env:CURATOR_PROFILE) { $env:CURATOR_PROFILE='local-user' }
$jar=Join-Path $projectRoot 'target/curator.jar'
if (-not (Test-Path $jar)) { throw 'Build target/curator.jar first.' }
$socketDir=if ($env:CURATOR_SOCKET_DIR) { $env:CURATOR_SOCKET_DIR } else { "$projectRoot/target" }
& $java "-Djdk.net.unixdomain.tmpdir=$socketDir" -jar $jar mcp
exit $LASTEXITCODE
