param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $CommandArgs
)

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..')).TrimEnd('\', '/')
$currentPath = [System.IO.Path]::GetFullPath((Get-Location).ProviderPath).TrimEnd('\', '/')
$insideProject = $currentPath.Equals($projectRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
    $currentPath.StartsWith($projectRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)

if (-not $insideProject) {
    Write-Error "Lệnh codepro chỉ chạy trong project: $projectRoot"
    exit 1
}

$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe -PathType Leaf)) {
    $pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $pythonExe) {
    Write-Error 'Không tìm thấy Python. Hãy cài Python hoặc tạo .venv cho project.'
    exit 1
}

$hasUser = $false
foreach ($arg in $CommandArgs) {
    if ($arg -eq '--user' -or $arg.StartsWith('--user=')) {
        $hasUser = $true
        break
    }
}
if (-not $hasUser -and '--help' -notin $CommandArgs -and '-h' -notin $CommandArgs) {
    $username = Read-Host 'Tên tài khoản quản trị Django'
    if ([string]::IsNullOrWhiteSpace($username)) {
        Write-Error 'Cần tên tài khoản quản trị.'
        exit 1
    }
    $CommandArgs = @('--user', $username) + $CommandArgs
}

Push-Location -LiteralPath $projectRoot
try {
    & $pythonExe (Join-Path $projectRoot 'manage.py') site_terminal @CommandArgs
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
