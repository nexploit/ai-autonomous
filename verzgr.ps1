Get-ChildItem -Directory | ForEach-Object {
    $size = (Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        FolderName = $_.Name
        SizeMB     = [math]::Round($size / 1MB, 2)
    }
} | Sort-Object SizeMB -Descending
