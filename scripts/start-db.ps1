$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
New-Item -ItemType Directory -Force "$projectRoot/.local" | Out-Null
if (-not (Test-Path "$projectRoot/.local/db-password")) {
  $bytes=New-Object byte[] 32
  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
  [Convert]::ToBase64String($bytes) | Set-Content "$projectRoot/.local/db-password"
}
$env:DB_PASSWORD=(Get-Content "$projectRoot/.local/db-password" -Raw).Trim()
& docker compose -f "$projectRoot/infra/compose.yaml" up -d --wait
if ($LASTEXITCODE -ne 0) { throw 'PostgreSQL startup failed.' }
