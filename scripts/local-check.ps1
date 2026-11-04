$ErrorActionPreference='Stop'
python "$PSScriptRoot/quality_pipeline.py"
if ($LASTEXITCODE -ne 0) { throw 'Local quality pipeline failed; inspect target/evidence/local-check.json' }
