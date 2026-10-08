[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('Project','User')][string]$Scope,
    [ValidateSet('codex','claude')][string]$Client = 'codex',
    [string]$ProjectPath,
    [string]$UserRoot = [Environment]::GetFolderPath('UserProfile'),
    [string[]]$Skills = @('all'),
    [switch]$DryRun,
    [switch]$Replace,
    [string]$GalleryDestination
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repo ".$Client\skills"
$clientDirectory = if ($Client -eq 'codex') { '.agents' } else { '.claude' }
if ($Scope -eq 'Project') {
    if (-not $ProjectPath) { throw 'Project scope requires -ProjectPath.' }
    $base = [IO.Path]::GetFullPath($ProjectPath)
} else { $base = [IO.Path]::GetFullPath($UserRoot) }
$destination = Join-Path $base "$clientDirectory\skills"
function Test-Overlap([string]$Left, [string]$Right) {
    $a = [IO.Path]::GetFullPath($Left).TrimEnd('\','/')
    $b = [IO.Path]::GetFullPath($Right).TrimEnd('\','/')
    return $a.Equals($b,[StringComparison]::OrdinalIgnoreCase) -or
        $a.StartsWith($b + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or
        $b.StartsWith($a + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)
}

function Copy-SkillContent([string]$Source, [string]$Destination) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    foreach ($entry in Get-ChildItem -LiteralPath $Source -Force) {
        if ($entry.Name -eq '__pycache__' -or $entry.Name -match '\.py[co]$') { continue }
        if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Source contains a reparse point: $($entry.FullName)" }
        $target = Join-Path $Destination $entry.Name
        if ($entry.PSIsContainer) { Copy-SkillContent $entry.FullName $target }
        else { Copy-Item -LiteralPath $entry.FullName -Destination $target }
    }
}
$names = if ($Skills.Count -eq 1 -and $Skills[0] -eq 'all') {
    @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Select-Object -ExpandProperty Name)
} else { @($Skills | Select-Object -Unique) }
$names = @($names)

# A selected skill may link to a sibling skill's resources. Include those
# dependencies so selective installation does not leave broken links.
do {
    $added = $false
    foreach ($name in @($names)) {
        $entry = Join-Path (Join-Path $sourceRoot $name) 'SKILL.md'
        if (-not (Test-Path -LiteralPath $entry)) { continue }
        foreach ($match in [regex]::Matches([IO.File]::ReadAllText($entry), '\]\(\.\./([a-z0-9]+(?:-[a-z0-9]+)*)/')) {
            $dependency = $match.Groups[1].Value
            if ($names -notcontains $dependency) {
                $names += $dependency
                $added = $true
            }
        }
    }
} while ($added)

function Assert-NoReparse([string]$Path) {
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Refusing reparse-point path: $cursor"
            }
        }
        $next = Split-Path -Parent $cursor
        if ($next -eq $cursor) { break }
        $cursor = $next
    }
}

$plan = @()
foreach ($name in $names) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$' -or $name.Length -gt 63) { throw "Invalid skill: $name" }
    $src = Join-Path $sourceRoot $name
    if (-not (Test-Path -LiteralPath (Join-Path $src 'SKILL.md'))) { throw "Unknown skill: $name" }
    $dst = Join-Path $destination $name
    Assert-NoReparse $dst
    if (Test-Overlap $dst $sourceRoot) { throw 'Skill destination overlaps source skills.' }
    $legacy = Join-Path $UserRoot ".codex\skills\$name"
    if ($Client -eq 'codex' -and (Test-Path -LiteralPath $legacy)) { Write-Warning "Same-name legacy skill remains at $legacy; review duplicate discovery." }
    $plan += [pscustomobject]@{Source=$src; Destination=$dst; Conflict=(Test-Path -LiteralPath $dst); Kind='skill'}
}
if ($GalleryDestination) {
    $gallery = [IO.Path]::GetFullPath($GalleryDestination)
    Assert-NoReparse $gallery
    if ((Test-Overlap $gallery $repo) -or (Test-Overlap $gallery (Join-Path $base $clientDirectory))) {
        throw 'Gallery destination overlaps the repository or skill installation area.'
    }
    $plan += [pscustomobject]@{Source=(Join-Path $repo 'documentation/references'); Destination=$gallery; Conflict=(Test-Path -LiteralPath $gallery); Kind='gallery'}
}
# Complete preflight before any destination is moved or copied.
foreach ($item in $plan) {
    Assert-NoReparse $item.Source
    if (@(Get-ChildItem -LiteralPath $item.Source -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw "Source contains reparse points: $($item.Source)"
    }
}
foreach ($item in $plan) { Write-Output ("{0} -> {1} (conflict: {2})" -f $item.Source,$item.Destination,$item.Conflict) }
if ($DryRun) { return }
if (@($plan | Where-Object Conflict).Count -gt 0 -and -not $Replace) {
    throw 'Destination conflicts found. No files changed. Use -Replace explicitly to preserve backups and replace.'
}
foreach ($item in $plan) {
    # Destination was resolved and checked before any move; never remove existing files.
    $parent = Split-Path -Parent $item.Destination
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    $backup = $null
    if ($item.Conflict) {
        $backupRoot = Join-Path $base "$clientDirectory\skill-backups"
        if ($item.Kind -eq 'gallery') { $backupRoot = Join-Path $parent '.gallery-backups' }
        Assert-NoReparse $backupRoot
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        $backup = Join-Path $backupRoot ((Split-Path -Leaf $item.Destination) + '-' + [guid]::NewGuid().ToString('N'))
        Move-Item -LiteralPath $item.Destination -Destination $backup
        Write-Output "Backup: $backup"
    }
    try {
        Copy-SkillContent $item.Source $item.Destination
    } catch {
        throw "Copy failed. Recover prior content from '$backup' if present. Error: $_"
    }
}
Write-Output "Installation complete for $Client. Restart the client if discovery has not refreshed. MCP configuration was not changed."
