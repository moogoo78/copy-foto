param(
  [string]$date,
  [string]$source,
  [string]$target
)

if ($date -ne "") {
  if ($date -eq "-") {
    $date = (Get-Date -Format 'yyMMdd')
  }

  $target_folder = "$target\$date"

  "Date) $date"
  "Target) $target_folder"

  if (Test-Path -Path $target_folder) {
    "Folder exists"
  }
  else {
    New-Item -ItemType directory -Path $target_folder
  }

  $date_y = [int]$date.Substring(0,2)
  $date_m = [int]$date.Substring(2,2)
  $date_d = [int]$date.Substring(4,2)

  $files = Get-ChildItem $source | Where{($_.CreationTime.month -eq $date_m) -and ($_.CreationTime.day -eq $date_d)}
  foreach ($f in $files) {
    "copy $f"
    Copy-Item $f -Destination $target_folder
  }
}
else {
  Get-Item $source
}