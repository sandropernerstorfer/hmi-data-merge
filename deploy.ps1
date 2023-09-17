Read-Host -Prompt 'Make sure everything is pushed'

$mainDir  = Split-Path $MyInvocation.MyCommand.Path -Parent
$srcDir   = "$mainDir/src"
$icon 	  = "$mainDir/icon.ico"
$deskDir  = "C:\Users\Synelecs\Desktop"
$tempDir  = "$deskDir\temp-py-src"
$distDir  = "$tempDir\dist"
$exeCMD   = "pyinstaller --onefile --icon=icon.ico main.py"
$appName  = "HMI-DataMerge"

# create temp dir + files
Copy-Item -Path $srcDir -Destination $tempDir -Recurse
Copy-Item $icon -Destination $tempDir

# go to temp dir and run build command
try {
	Set-Location $tempDir
	Invoke-Expression $exeCMD
}
catch {
	Write-Host "Error: build failed"
	Start-Sleep -s 3
	Exit
}

# move old .zip to trash
Remove-ItemSafely "$mainDir/*.zip"

# move old .exe from desktop to trash
Remove-ItemSafely "$deskDir/$appName.exe"

# name new exe - compress to zip - and move into main dir
Rename-Item -Path "$distDir\*.exe" -NewName "$appName.exe"
Copy-Item -Path "$distDir\*.exe" -Destination $deskDir
Compress-Archive -Path "$distDir\*.exe" -Destination "$mainDir\$appName.zip"

# remove temp dir
Remove-ItemSafely $tempDir

# github actions
Set-Location $mainDir
$date   = Get-Date -Format "dd/MM/yyyy HH:mm"
Invoke-Expression "git status"
Read-Host -Prompt "continue?"
Invoke-Expression "git add ."
Invoke-Expression "git commit -m 'updated zip/exe -> $date'"
Invoke-Expression "git push origin main"