# Install eight Project Surgeon Codex subagent profiles without changing config.toml.
param(
    [ValidateSet('User', 'Project')][string]$Scope = 'User',
    [string]$ProjectPath = '.',
    [switch]$Force
)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'plugins\project-surgeon\agents'
if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw 'Agent source folder is missing.' }
$expected = @('frontend-developer','backend-developer','ai-ml-engineer','data-engineer','devops-cloud-engineer','security-engineer','ui-ux-designer','qa-engineer')
if ($Scope -eq 'User') {
    $destination = Join-Path $HOME '.codex\agents'
} else {
    $base = (Resolve-Path -LiteralPath $ProjectPath).Path
    $destination = Join-Path $base '.codex\agents'
}
foreach ($name in $expected) {
    $from = Join-Path $source "$name.toml"
    if (-not (Test-Path -LiteralPath $from -PathType Leaf)) { throw "Required profile missing: $from" }
}
$existing = @($expected | Where-Object { Test-Path -LiteralPath (Join-Path $destination "$_.toml") })
if ($existing.Count -gt 0 -and -not $Force) {
    throw "Existing profiles found: $($existing -join ', '). No changes made. Use -Force to back up and overwrite."
}
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
foreach ($name in $expected) {
    $from = Join-Path $source "$name.toml"
    $to = Join-Path $destination "$name.toml"
    if (Test-Path -LiteralPath $to) {
        $backup = "$to.backup-$stamp"
        Copy-Item -LiteralPath $to -Destination $backup -ErrorAction Stop
    }
    Copy-Item -LiteralPath $from -Destination $to -Force
}
Write-Host "Installed 8 Codex subagent profiles in $destination. Restart Codex."
Write-Host "Use the tech-lead skill in the main session to delegate as needed."
