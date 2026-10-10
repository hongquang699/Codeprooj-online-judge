$projectScript = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'codepro.ps1'))
$profilePath = $PROFILE.CurrentUserCurrentHost
$profileDir = Split-Path -Parent $profilePath
New-Item -ItemType Directory -Path $profileDir -Force | Out-Null

$begin = '# BEGIN CodeProOJ terminal command'
$end = '# END CodeProOJ terminal command'
$existing = if (Test-Path -LiteralPath $profilePath) {
    [System.IO.File]::ReadAllText($profilePath)
} else {
    ''
}

$escapedPath = $projectScript.Replace("'", "''")
$block = @"
$begin
function global:codepro { & '$escapedPath' @args }
$end
"@
$pattern = '(?s)' + [regex]::Escape($begin) + '.*?' + [regex]::Escape($end)
if ([regex]::IsMatch($existing, $pattern)) {
    $updated = [regex]::Replace($existing, $pattern, { param($match) $block })
} else {
    $updated = $existing.TrimEnd("`r", "`n") + "`r`n" + $block + "`r`n"
}
[System.IO.File]::WriteAllText($profilePath, $updated, [System.Text.UTF8Encoding]::new($false))
Write-Output "Đã cài lệnh codepro vào $profilePath"
Write-Output 'Mở PowerShell mới hoặc chạy: . $PROFILE'
