# Install Project Surgeon locally. Never modifies application source.
param(
  [ValidateSet('User','Project')][string]$Scope = 'User',
  [string]$ProjectPath = '.',
  [switch]$Force
)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'plugins\project-surgeon'
if (-not (Test-Path -LiteralPath (Join-Path $source 'plugin.json'))) { throw 'Plugin source is missing' }
if ($Scope -eq 'User') {
  $root = $HOME
  $destination = Join-Path $root '.codex\plugins\project-surgeon'
  $marketPath = Join-Path $root '.agents\plugins\marketplace.json'
  $localPath = './.codex/plugins/project-surgeon'
} else {
  $root = (Resolve-Path -LiteralPath $ProjectPath).Path
  $destination = Join-Path $root 'plugins\project-surgeon'
  $marketPath = Join-Path $root '.agents\plugins\marketplace.json'
  $localPath = './plugins/project-surgeon'
}
if ((Test-Path $destination) -and (-not $Force)) { throw "Existing plugin at $destination. Use -Force to back it up and replace it." }
if (Test-Path $marketPath) {
  $catalog = Get-Content $marketPath -Raw | ConvertFrom-Json
  if ($null -eq $catalog.name) { throw 'Unrecognized existing marketplace' }
  if ($null -eq $catalog.plugins) { $catalog | Add-Member -NotePropertyName plugins -NotePropertyValue @() -Force }
  if ((@($catalog.plugins | Where-Object { $_.name -eq 'project-surgeon' }).Count -gt 0) -and (-not $Force)) {
    throw 'Project Surgeon already exists in marketplace. Use -Force.'
  }
} else {
  $catalog = [pscustomobject]@{ name='project-surgeon-local'; interface=[pscustomobject]@{displayName='Local Tools'}; plugins=@() }
}
New-Item -ItemType Directory -Force -Path (Split-Path $destination -Parent) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $marketPath -Parent) | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
if (Test-Path $destination) { Move-Item $destination "$destination.backup-$stamp" }
if (Test-Path $marketPath) { Copy-Item $marketPath "$marketPath.backup-$stamp" }
Copy-Item -LiteralPath $source -Destination $destination -Recurse
$entry = [pscustomobject]@{
  name='project-surgeon'
  source=[pscustomobject]@{source='local';path=$localPath}
  policy=[pscustomobject]@{installation='AVAILABLE';authentication='ON_INSTALL'}
  category='Productivity'
}
$catalog.plugins = @(@($catalog.plugins | Where-Object { $_.name -ne 'project-surgeon' }) + @($entry))
[System.IO.File]::WriteAllText($marketPath, ($catalog | ConvertTo-Json -Depth 30), (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Installed at $destination. Restart Codex and enable the plugin if needed."
