[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('Project','User')][string]$Scope,
    [string]$ProjectPath,
    [string]$UserRoot = [Environment]::GetFolderPath('UserProfile'),
    [string[]]$Skills = @('all'),
    [switch]$DryRun,
    [switch]$Replace,
    [string]$GalleryDestination
)
& (Join-Path $PSScriptRoot 'install-skills.ps1') -Client claude @PSBoundParameters
