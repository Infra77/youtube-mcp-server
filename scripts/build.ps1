param([string[]]$Goals = @('clean','verify'))
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
New-Item -ItemType Directory -Force "$projectRoot/.tools" | Out-Null
$jdk = Get-ChildItem -LiteralPath "$projectRoot/.tools" -Directory -Filter 'jdk-21*' | Select-Object -First 1
if ($jdk) { $env:JAVA_HOME = $jdk.FullName }
if (-not $env:JAVA_HOME) { throw 'Set JAVA_HOME to JDK 21.' }
$env:MAVEN_USER_HOME=Join-Path $projectRoot '.tools/maven-home'
Push-Location $projectRoot
try { & "$projectRoot/mvnw.cmd" @Goals; if ($LASTEXITCODE -ne 0) { throw "Maven exit $LASTEXITCODE" } }
finally { Pop-Location }
