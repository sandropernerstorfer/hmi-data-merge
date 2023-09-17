Write-Host 
"Deploying a new executable requires the following installations:
* pip
* openpyxl
* xlrd
* pyinstaller
"

$pkgConfirm = Read-Host -Prompt "Try to install missing packages using 'pip'? (y/n)"
if($pkgConfirm.toLower() -ne 'y' -and $pkgConfirm -ne ""){
	return
}

try{
	Invoke-Expression "pip install pyinstaller"
	Invoke-Expression "pip install openpyxl"
	Invoke-Expression "pip install xlrd"
}
catch{
	Write-Host
	"Error: Unable to install packages
	Make sure 'pip' is installed"
	return
}


# save needed directory paths
$mainDir  = Split-Path $MyInvocation.MyCommand.Path -Parent
$srcDir   = "$mainDir/src"
$icon 	  = "$mainDir/icon.ico"
$tempDir  = "$mainDir/src-temp"
$distDir  = "$mainDir/src-temp/dist"
$exeCMD   = "pyinstaller --onefile --icon=icon.ico main.py"
$appName  = "HMIDataMerge"

# git check
if(Test-Path -Path "$mainDir/.git"){
	Write-Host ""
	Read-Host -Prompt 'git warning: make sure everything is pushed before proceeding'
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
	Write-Host
	"Error: build failed"
	Start-Sleep -s 3
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
if(Test-Path -Path "$mainDir/.git"){
	$date   = Get-Date -Format "dd/MM/yyyy HH:mm"
	Invoke-Expression "git status"
	Read-Host -Prompt "continue?"
	Invoke-Expression "git add ."
	Invoke-Expression "git commit -m 'updated zip/exe -> $date'"
	Invoke-Expression "git push origin main"
}