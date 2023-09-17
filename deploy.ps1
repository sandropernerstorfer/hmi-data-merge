# save needed directory paths
$mainDir  = Split-Path $MyInvocation.MyCommand.Path -Parent
$srcDir   = "$mainDir/src"
$icon 	  = "$mainDir/icon.ico"
$tempDir  = "$mainDir/temp-src"
$distDir  = "$mainDir/temp-src/dist"
$exeCMD   = "pyinstaller --onefile --icon=icon.ico main.py"
$appName  = "HMIDataMerge"

# git check
if(Test-Path -Path "$mainDir/.git"){
	Read-Host -Prompt 'Caution: Make sure everything is pushed before proceeding'
}

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
	Write-Host "Make sure you have 'pyinstaller' installed"
	Start-Sleep -s 4
	Exit
}

Set-Location $mainDir

# move old .zip and .exe to trash
Remove-Item "$mainDir/*.zip"
Remove-Item "$mainDir/*.exe"

# name new exe - compress to zip - and move into main dir
Rename-Item -Path "$distDir\main.exe" -NewName "$appName.exe"
Copy-Item -Path "$distDir\$appName.exe" -Destination $mainDir
Compress-Archive -Path "$distDir\$appName.exe" -Destination "$mainDir\$appName.zip"

# remove temp dir
Get-ChildItem -Path $tempDir -Recurse | Remove-Item -force -recurse
Remove-Item $tempDir -Force

# github actions
$date   = Get-Date -Format "dd/MM/yyyy HH:mm"
Invoke-Expression "git status"
Read-Host -Prompt "continue?"
Invoke-Expression "git add ."
Invoke-Expression "git commit -m 'updated zip/exe -> $date'"
Invoke-Expression "git push origin main"