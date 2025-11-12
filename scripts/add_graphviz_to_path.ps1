# Add Graphviz to PATH for current session
# Usage: . .\scripts\add_graphviz_to_path.ps1

$graphvizPaths = @(
    "C:\Program Files\Graphviz\bin",
    "C:\Program Files (x86)\Graphviz\bin"
)

foreach ($path in $graphvizPaths) {
    if (Test-Path $path) {
        if ($env:PATH -notlike "*$path*") {
            $env:PATH = "$path;$env:PATH"
            Write-Host "✅ Added to PATH: $path" -ForegroundColor Green
        } else {
            Write-Host "✅ Already in PATH: $path" -ForegroundColor Green
        }

        # Verify
        $dotPath = Join-Path $path "dot.exe"
        if (Test-Path $dotPath) {
            Write-Host "✅ Graphviz found: $dotPath" -ForegroundColor Green
            & $dotPath -V 2>&1 | Select-Object -First 1
            break
        }
    }
}

if (-not (Get-Command dot -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Graphviz not found. Please restart PowerShell or add manually to PATH." -ForegroundColor Yellow
}
