$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$dest=Join-Path $projectRoot '.tools/gitleaks'
New-Item -ItemType Directory -Force $dest | Out-Null
$version='8.30.1'
$archive="gitleaks_${version}_windows_x64.zip"
$base="https://github.com/gitleaks/gitleaks/releases/download/v$version"
Invoke-WebRequest "$base/$archive" -OutFile "$dest/$archive"
Invoke-WebRequest "$base/gitleaks_${version}_checksums.txt" -OutFile "$dest/checksums.txt"
$line=Get-Content "$dest/checksums.txt" | Where-Object { $_ -match ([regex]::Escape($archive)+'$') }
if (-not $line) { throw 'Checksum entry missing' }
$expected=($line -split '\s+')[0]
if ((Get-FileHash "$dest/$archive" -Algorithm SHA256).Hash -ne $expected) { throw 'Gitleaks checksum mismatch' }
Expand-Archive "$dest/$archive" -DestinationPath $dest -Force
& "$dest/gitleaks.exe" version
if ($LASTEXITCODE -ne 0) { throw 'Gitleaks installation failed' }
