<#
start_dev.ps1
Usage:
  - Run in PowerShell from the project root:
      .\scripts\start_dev.ps1 -AllowFirewall
  - `-AllowFirewall` will add a Windows Firewall rule for port 8000 (requires Admin).
#>
param(
    [switch]$AllowFirewall
)

Push-Location $PSScriptRoot\..\

if ($AllowFirewall) {
    Write-Host "Adding Firewall rule for TCP/8000 (requires Admin)..."
    try {
        netsh advfirewall firewall add rule name="Django 8000" dir=in action=allow protocol=TCP localport=8000 | Out-Null
        Write-Host "Firewall rule added."
    } catch {
        Write-Warning "Failed to add firewall rule. Run PowerShell as Administrator if you want to add it."
    }
}

Write-Host "Starting Django dev server on 0.0.0.0:8000..."
# Start in foreground so user can see output; this blocks the script.
python manage.py runserver 0.0.0.0:8000

Pop-Location
