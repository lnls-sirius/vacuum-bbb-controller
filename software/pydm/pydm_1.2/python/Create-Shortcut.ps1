$WorkDir = "$Home\Documents\vacuum-bbb-controller\software\pydm\pydm_1.2\python"
$IcoUrl = "https://github.com/lnls-sirius/pydm-opi/raw/master/miscellaneous/windows/"
$IcoDestPath = "$Home\Icons\"

$IcoSirius = "sirius.ico"

New-Item -ItemType Directory -Force -Path "$IcoDestPath"

Invoke-WebRequest -Uri "$IcoUrl/$IcoSirius" -OutFile "$IcoDestPath\$IcoSirius"

function CreateShortcut {
    param ( [string]$DestinationPath, [string]$Ico, [string]$Desc )

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($DestinationPath)
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = "-Command .\Start.ps1;"
    $Shortcut.IconLocation = "$IcoDestPath\$Ico"
    $Shortcut.WorkingDirectory = "$WorkDir"
    $Shortcut.Description = "$Desc"
    $Shortcut.Save()
}

CreateShortcut "$Home\Desktop\VBC.lnk" $IcoSirius "VBC"