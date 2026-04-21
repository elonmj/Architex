param(
    [Parameter(Mandatory = $true)]
    [string]$InputDir,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [string]$PythonExe = "python",

    [int]$LimitPerFile = 0,

    [switch]$WorldCoords
)

$inputPath = Resolve-Path -Path $InputDir
if (-not $inputPath) {
    Write-Error "Input directory not found: $InputDir"
    exit 2
}

if (-not (Test-Path -Path $OutputDir)) {
    New-Item -Path $OutputDir -ItemType Directory -Force | Out-Null
}

$ifcFiles = Get-ChildItem -Path $inputPath -Filter *.ifc -File
if ($ifcFiles.Count -eq 0) {
    Write-Error "No IFC files found in: $inputPath"
    exit 3
}

foreach ($file in $ifcFiles) {
    $outFile = Join-Path $OutputDir ($file.BaseName + ".obj")
    $cmd = @(
        "scripts/ifc_to_mesh.py",
        "--input", $file.FullName,
        "--output", $outFile
    )

    if ($LimitPerFile -gt 0) {
        $cmd += @("--limit", "$LimitPerFile")
    }

    if ($WorldCoords.IsPresent) {
        $cmd += "--world-coords"
    }

    Write-Host "Processing $($file.Name) -> $outFile"
    & $PythonExe $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Failed for file: $($file.FullName)"
    }
}

Write-Host "Done."
