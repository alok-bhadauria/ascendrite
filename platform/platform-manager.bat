@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = Get-Content -LiteralPath '%~f0' -Raw; $c = $c -replace '(?s)^.*#PS_START\r?\n', ''; iex $c"
exit /b %errorlevel%
#PS_START
# Ascendrite Platform Manager
# Self-contained PowerShell backend launcher and status monitor

$PlatformDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $PlatformDir
$ServerDir = Join-Path $PlatformDir "server"
$ClientDir = Join-Path $PlatformDir "client"
$RuntimeDir = "E:\Projects\ascendrite-data\runtime"
$BackendPidFile = Join-Path $RuntimeDir "backend.pid"
$FrontendPidFile = Join-Path $RuntimeDir "frontend.pid"

# Defensive checks for directory structure
if (-not (Test-Path $ServerDir)) {
    Write-Host "[ERROR] Platform server directory not found at: $ServerDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
if (-not (Test-Path $ClientDir)) {
    Write-Host "[ERROR] Platform client directory not found at: $ClientDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
$PkgJson = Join-Path $ClientDir "package.json"
if (-not (Test-Path $PkgJson)) {
    Write-Host "[ERROR] Frontend package.json not found at: $PkgJson" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Ensure runtime directories exist
if (-not (Test-Path $RuntimeDir)) {
    New-Item -ItemType Directory -Path $RuntimeDir -Force | Out-Null
}
$LogsDir = Join-Path $RepoRoot "logs"
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# Find python interpreter
$VenvPython = Join-Path $ServerDir "python-venv-3.10.11\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    $VenvPython = Join-Path $ServerDir ".venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPython)) {
        $VenvPython = Join-Path $ServerDir "venv\Scripts\python.exe"
        if (-not (Test-Path $VenvPython)) {
            $VenvPython = "python.exe"
        }
    }
}

function Test-PortConnection($port) {
    # Check listening ports
    $netstat = netstat -ano | Select-String "LISTENING" | Select-String ":$port\s+"
    return [bool]$netstat
}

function Get-PortOccupyingPID($port) {
    $netstat = netstat -ano | Select-String "LISTENING" | Select-String ":$port\s+"
    if ($netstat) {
        $line = $netstat | Select-Object -First 1 | ForEach-Object { $_.Line.Trim() }
        $parts = $line -split '\s+'
        if ($parts.Count -ge 5) {
            return $parts[4]
        }
    }
    return $null
}

function Get-ProcessDescendants($parentPid) {
    $descendants = @()
    $queue = [System.Collections.Generic.Queue[int]]::new()
    $queue.Enqueue($parentPid)
    while ($queue.Count -gt 0) {
        $curr = $queue.Dequeue()
        $children = Get-CimInstance Win32_Process -Filter "ParentProcessId = $curr" -ErrorAction SilentlyContinue
        foreach ($child in $children) {
            $descendants += $child.ProcessId
            $queue.Enqueue($child.ProcessId)
        }
    }
    return $descendants
}

function Test-ManagedOwnership($pidFile, $port) {
    if (-not (Test-Path $pidFile)) {
        return $false
    }
    $launcherPidVal = Get-Content $pidFile -Raw -ErrorAction SilentlyContinue
    if (-not $launcherPidVal) {
        return $false
    }
    $launcherPid = [int]($launcherPidVal.Trim())

    # Check if launcher process is running
    $launcherProc = Get-Process -Id $launcherPid -ErrorAction SilentlyContinue
    if (-not $launcherProc) {
        return $false
    }

    # Retrieve all process IDs in our managed tree (launcher + descendants)
    $treePids = @($launcherPid)
    $treePids += Get-ProcessDescendants $launcherPid

    # Get the PID currently listening on the port
    $portPidVal = Get-PortOccupyingPID $port
    if ($portPidVal) {
        $portPid = [int]$portPidVal
        # If the port owner is part of our managed process tree, ownership is verified
        if ($treePids -contains $portPid) {
            return $true
        }
    }

    # Fallback keyword validation on process tree members
    foreach ($p in $treePids) {
        $procObj = Get-CimInstance Win32_Process -Filter "ProcessId = $p" -ErrorAction SilentlyContinue
        if ($procObj) {
            $cmd = $procObj.CommandLine
            $path = $procObj.ExecutablePath
            if ($port -eq 8000) {
                if ($cmd -match "uvicorn|main:app" -or $path -match "python") {
                    return $true
                }
            } elseif ($port -eq 5173) {
                if ($cmd -match "vite|node|npm" -or $path -match "node") {
                    return $true
                }
            }
        }
    }

    return $false
}

function Get-ServiceState($serviceName, $port) {
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($service) {
        $serviceRunning = $service.Status -eq "Running"
    } else {
        $serviceRunning = $false
    }
    $portListening = Test-PortConnection $port

    if ($serviceRunning -and $portListening) {
        return "ONLINE"
    } elseif ($serviceRunning -and -not $portListening) {
        return "DEGRADED"
    } elseif (-not $serviceRunning -and $portListening) {
        return "UNKNOWN"
    } else {
        return "OFFLINE"
    }
}

function Test-HTTPStatus($url) {
    try {
        $res = Invoke-WebRequest -Uri $url -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($res.StatusCode -match "2\d\d|3\d\d") {
            return $true
        }
    } catch {
        # ignore error
    }
    return $false
}

function Get-AppStatus($pidFile, $port, $url) {
    if (Test-Path $pidFile) {
        $launcherPid = Get-Content -Path $pidFile -Raw -ErrorAction SilentlyContinue
        if ($launcherPid) {
            $launcherPid = $launcherPid.Trim()
            $proc = Get-Process -Id $launcherPid -ErrorAction SilentlyContinue
            if ($proc) {
                if (Test-ManagedOwnership $pidFile $port) {
                    if (Test-PortConnection $port) {
                        if (Test-HTTPStatus $url) {
                            return "ONLINE"
                        } else {
                            return "DEGRADED"
                        }
                    } else {
                        return "DEGRADED"
                    }
                } else {
                    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
                }
            } else {
                Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
            }
        }
    }
    $occupyPid = Get-PortOccupyingPID $port
    if ($occupyPid) {
        return "UNKNOWN"
    }
    return "OFFLINE"
}

function Get-FullStatus {
    $pg = Get-ServiceState "postgresql-x64-18" 5432
    $mongo = Get-ServiceState "MongoDB" 27017
    $redis = Get-ServiceState "Memurai" 6379
    $rustfsS3 = Get-ServiceState "AscendriteRustFS" 9000
    $rustfsConsole = Get-ServiceState "AscendriteRustFS" 9001
    
    $backend = Get-AppStatus $BackendPidFile 8000 "http://127.0.0.1:8000/health"
    $frontend = Get-AppStatus $FrontendPidFile 5173 "http://localhost:5173"

    return [PSCustomObject]@{
        Postgres = $pg
        MongoDB = $mongo
        Redis = $redis
        RustFS_S3 = $rustfsS3
        RustFS_Console = $rustfsConsole
        Backend = $backend
        Frontend = $frontend
    }
}

function Write-ColoredStatus($status) {
    switch ($status) {
        "ONLINE" { Write-Host " [ONLINE] " -ForegroundColor Green -NoNewline }
        "OFFLINE" { Write-Host " [OFFLINE]" -ForegroundColor Gray -NoNewline }
        "DEGRADED" { Write-Host " [DEGRADED]" -ForegroundColor Yellow -NoNewline }
        "UNKNOWN" { Write-Host " [UNKNOWN] " -ForegroundColor Red -NoNewline }
    }
}

function Show-Dashboard($statuses) {
    Clear-Host
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                  ASCENDRITE PLATFORM MANAGER                   " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    if (-not $isAdmin) {
        Write-Host "  * Running in USER mode (Infrastructure control requires Admin) *" -ForegroundColor Yellow
        Write-Host "================================================================" -ForegroundColor Cyan
    }
    Write-Host " Infrastructure Status:"
    Write-Host "   PostgreSQL:        " -NoNewline; Write-ColoredStatus $statuses.Postgres; Write-Host " (Service: postgresql-x64-18, Port: 5432)"
    Write-Host "   MongoDB:           " -NoNewline; Write-ColoredStatus $statuses.MongoDB; Write-Host " (Service: MongoDB, Port: 27017)"
    Write-Host "   Memurai / Redis:   " -NoNewline; Write-ColoredStatus $statuses.Redis; Write-Host " (Service: Memurai, Port: 6379)"
    Write-Host "   RustFS S3 API:     " -NoNewline; Write-ColoredStatus $statuses.RustFS_S3; Write-Host " (Service: AscendriteRustFS, Port: 9000)"
    Write-Host "   RustFS Console:    " -NoNewline; Write-ColoredStatus $statuses.RustFS_Console; Write-Host " (Service: AscendriteRustFS, Port: 9001)"
    Write-Host ""
    Write-Host " Application Status:"
    Write-Host "   Backend API:       " -NoNewline; Write-ColoredStatus $statuses.Backend; Write-Host " (Port: 8000)"
    Write-Host "   Frontend:          " -NoNewline; Write-ColoredStatus $statuses.Frontend; Write-Host " (Port: 5173)"
    Write-Host "================================================================" -ForegroundColor Cyan
}

function Start-WinService($serviceName) {
    if (-not $isAdmin) {
        Write-Host "[ERROR] Starting service '$serviceName' requires Administrator privileges." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if (-not $status) {
        Write-Host "[ERROR] Service '$serviceName' is not installed." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    if ($status.Status -eq "Running") {
        Write-Host "Service '$serviceName' is already healthy. [SKIP]" -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        return
    }
    Write-Host "Starting service '$serviceName'..."
    Start-Service -Name $serviceName -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($status.Status -eq "Running") {
        Write-Host "Service '$serviceName' started successfully. [OK]" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to start service '$serviceName'." -ForegroundColor Red
        Read-Host "Press Enter to continue"
    }
}

function Stop-WinService($serviceName) {
    if (-not $isAdmin) {
        Write-Host "[ERROR] Stopping service '$serviceName' requires Administrator privileges." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if (-not $status) {
        Write-Host "[ERROR] Service '$serviceName' is not installed." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    if ($status.Status -eq "Stopped") {
        Write-Host "Service '$serviceName' is already stopped. [SKIP]" -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        return
    }
    Write-Host "Stopping service '$serviceName'..."
    Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($status.Status -eq "Stopped") {
        Write-Host "Service '$serviceName' stopped successfully. [OK]" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to stop service '$serviceName'." -ForegroundColor Red
        Read-Host "Press Enter to continue"
    }
}

function Restart-WinService($serviceName) {
    if (-not $isAdmin) {
        Write-Host "[ERROR] Restarting service '$serviceName' requires Administrator privileges." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if (-not $status) {
        Write-Host "[ERROR] Service '$serviceName' is not installed." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    Write-Host "Restarting service '$serviceName'..."
    Restart-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($status.Status -eq "Running") {
        Write-Host "Service '$serviceName' restarted successfully. [OK]" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to restart service '$serviceName'." -ForegroundColor Red
        Read-Host "Press Enter to continue"
    }
}

function Start-AllInfra {
    Write-Host "Starting all infrastructure services..."
    $services = @("postgresql-x64-18", "MongoDB", "Memurai", "AscendriteRustFS")
    foreach ($svc in $services) {
        $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
        if ($status) {
            if ($status.Status -eq "Running") {
                Write-Host "Service '$svc' is already running. [SKIP]" -ForegroundColor Yellow
            } else {
                if ($isAdmin) {
                    Write-Host "Starting '$svc'..."
                    Start-Service -Name $svc -ErrorAction SilentlyContinue
                } else {
                    Write-Host "[ERROR] Administrator privileges required to start '$svc'." -ForegroundColor Red
                }
            }
        } else {
            Write-Host "Service '$svc' is not installed. [SKIP]" -ForegroundColor Red
        }
    }
    Start-Sleep -Seconds 2
}

function Stop-AllInfra {
    Write-Host "Are you sure you want to stop all infrastructure? (y/N): " -NoNewline
    $confirm = Read-Host
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        $services = @("postgresql-x64-18", "MongoDB", "Memurai", "AscendriteRustFS")
        foreach ($svc in $services) {
            $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
            if ($status) {
                if ($status.Status -eq "Stopped") {
                    Write-Host "Service '$svc' is already stopped. [SKIP]" -ForegroundColor Yellow
                } else {
                    if ($isAdmin) {
                        Write-Host "Stopping '$svc'..."
                        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
                    } else {
                        Write-Host "[ERROR] Administrator privileges required to stop '$svc'." -ForegroundColor Red
                    }
                }
            }
        }
        Start-Sleep -Seconds 2
    }
}

function Start-BackendApp {
    Write-Host "Verifying infrastructure requirements before Backend startup..."
    $statuses = Get-FullStatus
    if ($statuses.Postgres -ne "ONLINE" -or $statuses.MongoDB -ne "ONLINE" -or $statuses.Redis -ne "ONLINE") {
        Write-Host "[WARN] Infrastructure dependencies are not fully online." -ForegroundColor Yellow
        Write-Host "  PostgreSQL: $($statuses.Postgres)"
        Write-Host "  MongoDB:    $($statuses.MongoDB)"
        Write-Host "  Redis:      $($statuses.Redis)"
        Write-Host "Starting API server in degraded/partial capability state." -ForegroundColor Yellow
    }

    if ($VenvPython -eq "python.exe") {
        $pyCheck = Get-Command "python" -ErrorAction SilentlyContinue
        if (-not $pyCheck) {
            Write-Host "[ERROR] Python execution path not found. Please install Python or set up a virtual environment." -ForegroundColor Red
            Read-Host "Press Enter to continue"
            return $false
        }
    }

    # Test if python can import uvicorn
    Write-Host "Testing python interpreter and uvicorn availability..."
    $testCmd = "& `"$VenvPython`" -c `"import uvicorn; print('OK')`""
    $output = Invoke-Expression $testCmd -ErrorAction SilentlyContinue
    if ($output -ne "OK") {
        Write-Host "[ERROR] Selected Python interpreter ($VenvPython) cannot run or import 'uvicorn'. Please run 'pip install -r requirements.txt'." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    $occupyPid = Get-PortOccupyingPID 8000
    if ($occupyPid) {
        if (Test-Path $BackendPidFile) {
            $managedPid = Get-Content $BackendPidFile -Raw -ErrorAction SilentlyContinue
            if ($managedPid -and $managedPid.Trim() -eq $occupyPid) {
                Write-Host "Backend is already running. [SKIP]" -ForegroundColor Yellow
                Start-Sleep -Seconds 1
                return $true
            }
        }
        Write-Host "[ERROR] Port 8000 occupied by an unmanaged process (PID: $occupyPid). Aborting startup to prevent killing unrelated tasks." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    if (Test-Path $BackendPidFile) {
        Remove-Item $BackendPidFile -Force -ErrorAction SilentlyContinue
    }

    Write-Host "Starting Backend API Server..."
    $logPath = Join-Path $RepoRoot "logs\backend.log"
    
    try {
        # Redirect standard output and error using CMD to avoid lock conflicts on Windows
        $args = '/c ""' + $VenvPython + '" -m uvicorn main:app --host 127.0.0.1 --port 8000 >> "' + $logPath + '" 2>&1"'
        $proc = Start-Process -FilePath "cmd.exe" -ArgumentList $args -WorkingDirectory "$ServerDir" -PassThru -NoNewWindow
        $proc.Id | Out-File -FilePath $BackendPidFile -Encoding ascii
        
        Write-Host "Waiting for Backend to listen on port 8000..." -NoNewline
        $started = $false
        for ($i = 0; $i -lt 15; $i++) {
            Start-Sleep -Seconds 1
            $chkProc = Get-Process -Id $proc.Id -ErrorAction SilentlyContinue
            if (-not $chkProc -or $chkProc.HasExited) {
                Write-Host " [FAILED] Process died during startup." -ForegroundColor Red
                break
            }
            if (Test-PortConnection 8000) {
                $started = $true
                break
            }
        }
        if ($started) {
            Write-Host " [OK] (PID: $($proc.Id))" -ForegroundColor Green
        } else {
            Write-Host " [TIMEOUT/FAILED] Check backend.log for errors." -ForegroundColor Red
            if (Test-Path $BackendPidFile) {
                Remove-Item $BackendPidFile -Force -ErrorAction SilentlyContinue
            }
            Read-Host "Press Enter to continue"
            return $false
        }
    } catch {
        Write-Host "[ERROR] Failed to start Backend process: $_" -ForegroundColor Red
        if (Test-Path $BackendPidFile) {
            Remove-Item $BackendPidFile -Force -ErrorAction SilentlyContinue
        }
        Read-Host "Press Enter to continue"
        return $false
    }
    return $true
}

function Stop-BackendApp {
    Stop-AppProcess $BackendPidFile 8000 "Backend"
}

function Restart-BackendApp {
    Stop-BackendApp
    Start-BackendApp
}

function Start-FrontendApp {
    $npmCheck = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if (-not $npmCheck) {
        Write-Host "[ERROR] npm executable not found in PATH. Please install Node.js." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    $occupyPid = Get-PortOccupyingPID 5173
    if ($occupyPid) {
        if (Test-Path $FrontendPidFile) {
            $managedPid = Get-Content $FrontendPidFile -Raw -ErrorAction SilentlyContinue
            if ($managedPid -and $managedPid.Trim() -eq $occupyPid) {
                Write-Host "Frontend is already running. [SKIP]" -ForegroundColor Yellow
                Start-Sleep -Seconds 1
                return $true
            }
        }
        Write-Host "[ERROR] Port 5173 occupied by an unmanaged process (PID: $occupyPid). Aborting startup to prevent killing unrelated tasks." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    if (Test-Path $FrontendPidFile) {
        Remove-Item $FrontendPidFile -Force -ErrorAction SilentlyContinue
    }

    Write-Host "Starting Frontend (Vite) Server..."
    $logPath = Join-Path $RepoRoot "logs\frontend.log"
    
    try {
        # Redirect standard output and error using CMD to avoid lock conflicts on Windows
        $args = '/c "npm run dev >> "' + $logPath + '" 2>&1"'
        $proc = Start-Process -FilePath "cmd.exe" -ArgumentList $args -WorkingDirectory "$ClientDir" -PassThru -NoNewWindow
        $proc.Id | Out-File -FilePath $FrontendPidFile -Encoding ascii
        
        Write-Host "Waiting for Frontend to listen on port 5173..." -NoNewline
        $started = $false
        for ($i = 0; $i -lt 15; $i++) {
            Start-Sleep -Seconds 1
            $chkProc = Get-Process -Id $proc.Id -ErrorAction SilentlyContinue
            if (-not $chkProc -or $chkProc.HasExited) {
                Write-Host " [FAILED] Process died during startup." -ForegroundColor Red
                break
            }
            if (Test-PortConnection 5173) {
                $started = $true
                break
            }
        }
        if ($started) {
            Write-Host " [OK] (PID: $($proc.Id))" -ForegroundColor Green
        } else {
            Write-Host " [TIMEOUT/FAILED] Check frontend.log for errors." -ForegroundColor Red
            if (Test-Path $FrontendPidFile) {
                Remove-Item $FrontendPidFile -Force -ErrorAction SilentlyContinue
            }
            Read-Host "Press Enter to continue"
            return $false
        }
    } catch {
        Write-Host "[ERROR] Failed to start Frontend process: $_" -ForegroundColor Red
        if (Test-Path $FrontendPidFile) {
            Remove-Item $FrontendPidFile -Force -ErrorAction SilentlyContinue
        }
        Read-Host "Press Enter to continue"
        return $false
    }
    return $true
}

function Stop-FrontendApp {
    Stop-AppProcess $FrontendPidFile 5173 "Frontend"
}

function Stop-AppProcess($pidFile, $port, $appName) {
    if (Test-Path $pidFile) {
        $launcherPidVal = Get-Content $pidFile -Raw -ErrorAction SilentlyContinue
        if ($launcherPidVal) {
            $launcherPid = [int]($launcherPidVal.Trim())
            # Verify process ownership to prevent killing reused/unrelated Windows PIDs
            if (Test-ManagedOwnership $pidFile $port) {
                Write-Host "Stopping $appName (PID: $launcherPid)..." -NoNewline
                taskkill /f /t /pid $launcherPid >$null 2>&1
                Start-Sleep -Seconds 1
                Write-Host " [OK]" -ForegroundColor Green
            } else {
                Write-Host "[WARN] Process ID $launcherPid does not match managed process tree. Stale PID file cleaned." -ForegroundColor Yellow
            }
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    } else {
        $occupyPid = Get-PortOccupyingPID $port
        if ($occupyPid) {
            Write-Host "[WARN] Port $port is occupied by unmanaged process (PID: $occupyPid). Not killing it." -ForegroundColor Yellow
        } else {
            Write-Host "$appName is already stopped. [SKIP]" -ForegroundColor Yellow
        }
        Start-Sleep -Seconds 1
    }
}

function Restart-FrontendApp {
    Stop-FrontendApp
    Start-FrontendApp
}

function Start-BothApps {
    Start-BackendApp
    Start-FrontendApp
}

function Stop-BothApps {
    Stop-BackendApp
    Stop-FrontendApp
}

function Start-FullStack {
    Write-Host "Starting Full Stack..."
    Start-AllInfra
    Start-BackendApp
    Start-FrontendApp
    Read-Host "Full stack start sequence finished. Press Enter to return to Dashboard."
}

function Manage-Infrastructure {
    while ($true) {
        $statuses = Get-FullStatus
        Clear-Host
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "                      MANAGE INFRASTRUCTURE                     " -ForegroundColor Cyan
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "  [1] Start PostgreSQL       (Current: $($statuses.Postgres))"
        Write-Host "  [2] Stop PostgreSQL"
        Write-Host "  [3] Restart PostgreSQL"
        Write-Host "  [4] Start MongoDB          (Current: $($statuses.MongoDB))"
        Write-Host "  [5] Stop MongoDB"
        Write-Host "  [6] Restart MongoDB"
        Write-Host "  [7] Start Memurai (Redis)  (Current: $($statuses.Redis))"
        Write-Host "  [8] Stop Memurai (Redis)"
        Write-Host "  [9] Restart Memurai (Redis)"
        Write-Host "  [10] Start RustFS          (Current: $($statuses.RustFS_S3))"
        Write-Host "  [11] Stop RustFS"
        Write-Host "  [12] Restart RustFS"
        Write-Host "  [13] Start All Infrastructure"
        Write-Host "  [14] Stop All Infrastructure (Requires Confirmation)"
        Write-Host "  [0] Back"
        Write-Host "================================================================" -ForegroundColor Cyan
        
        $choice = Read-Host "Choice"
        switch ($choice) {
            "1" { Start-WinService "postgresql-x64-18" }
            "2" { Stop-WinService "postgresql-x64-18" }
            "3" { Restart-WinService "postgresql-x64-18" }
            "4" { Start-WinService "MongoDB" }
            "5" { Stop-WinService "MongoDB" }
            "6" { Restart-WinService "MongoDB" }
            "7" { Start-WinService "Memurai" }
            "8" { Stop-WinService "Memurai" }
            "9" { Restart-WinService "Memurai" }
            "10" { Start-WinService "AscendriteRustFS" }
            "11" { Stop-WinService "AscendriteRustFS" }
            "12" { Restart-WinService "AscendriteRustFS" }
            "13" { Start-AllInfra }
            "14" { Stop-AllInfra }
            "0" { return }
            default { Write-Host "Invalid choice." -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    }
}

function Manage-Application {
    while ($true) {
        $statuses = Get-FullStatus
        Clear-Host
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "                       MANAGE APPLICATION                       " -ForegroundColor Cyan
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "  [1] Start Backend          (Current: $($statuses.Backend))"
        Write-Host "  [2] Stop Backend"
        Write-Host "  [3] Restart Backend"
        Write-Host "  [4] Start Frontend         (Current: $($statuses.Frontend))"
        Write-Host "  [5] Stop Frontend"
        Write-Host "  [6] Restart Frontend"
        Write-Host "  [7] Start Both Applications"
        Write-Host "  [8] Stop Both Applications"
        Write-Host "  [0] Back"
        Write-Host "================================================================" -ForegroundColor Cyan
        
        $choice = Read-Host "Choice"
        switch ($choice) {
            "1" { Start-BackendApp }
            "2" { Stop-BackendApp }
            "3" { Restart-BackendApp }
            "4" { Start-FrontendApp }
            "5" { Stop-FrontendApp }
            "6" { Restart-FrontendApp }
            "7" { Start-BothApps }
            "8" { Stop-BothApps }
            "0" { return }
            default { Write-Host "Invalid choice." -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    }
}

function Show-Diagnostics {
    Clear-Host
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                     HEALTH AND DIAGNOSTICS                     " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "Privilege Level: " -NoNewline
    if ($isAdmin) {
        Write-Host "ADMINISTRATOR (Full Service Control Enabled)" -ForegroundColor Green
    } else {
        Write-Host "USER (Service startup/stop disabled)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Windows Services Checks:"
    $services = @(
        @{ Name = "postgresql-x64-18"; Desc = "Primary Relational Store - Struct data and user registries (CRITICAL)" },
        @{ Name = "MongoDB"; Desc = "NoSQL Document Store - Workspace document metadata indexers (DEGRADED CAPABILITY)" },
        @{ Name = "Memurai"; Desc = "Volatile Cache & Realtime PubSub - Realtime subscriptions and socket rooms (DEGRADED CAPABILITY)" },
        @{ Name = "AscendriteRustFS"; Desc = "RustFS Object Storage - Binary files, attachments, and learning artifacts (DEGRADED CAPABILITY)" }
    )
    foreach ($svc in $services) {
        $status = Get-Service -Name $svc.Name -ErrorAction SilentlyContinue
        if ($status) {
            Write-Host "  Service '$($svc.Name)': " -NoNewline
            if ($status.Status -eq "Running") {
                Write-Host "RUNNING" -ForegroundColor Green
            } else {
                Write-Host "STOPPED (Impact: $($svc.Desc))" -ForegroundColor Red
            }
        } else {
            Write-Host "  Service '$($svc.Name)': NOT INSTALLED (Impact: $($svc.Desc))" -ForegroundColor Yellow
        }
    }
    Write-Host ""
    Write-Host "Port Occupancy and Conflicts Check:"
    $ports = @(5432, 27017, 6379, 9000, 9001, 8000, 5173)
    foreach ($port in $ports) {
        $occupy = Get-PortOccupyingPID $port
        if ($occupy) {
            Write-Host "  Port $($port): Listening (PID: $occupy)" -ForegroundColor Green
        } else {
            Write-Host "  Port $($port): Closed" -ForegroundColor Gray
        }
    }
    Write-Host ""
    Write-Host "Managed Application Runtime State:"
    if (Test-Path $BackendPidFile) {
        $bPid = Get-Content $BackendPidFile -Raw -ErrorAction SilentlyContinue
        if ($bPid) {
            $bPid = $bPid.Trim()
            $bProc = Get-Process -Id $bPid -ErrorAction SilentlyContinue
            if ($bProc) {
                if (Test-ManagedOwnership $BackendPidFile 8000) {
                    Write-Host "  Backend process is running with PID: $bPid (Ownership: VERIFIED)" -ForegroundColor Green
                } else {
                    Write-Host "  Backend process is running with PID: $bPid (Ownership: UNVERIFIED/REUSED)" -ForegroundColor Red
                }
            } else {
                Write-Host "  Backend: Stale PID file found (PID: $bPid, process dead)" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "  Backend: PID file not found (stopped)" -ForegroundColor Gray
    }

    if (Test-Path $FrontendPidFile) {
        $fPid = Get-Content $FrontendPidFile -Raw -ErrorAction SilentlyContinue
        if ($fPid) {
            $fPid = $fPid.Trim()
            $fProc = Get-Process -Id $fPid -ErrorAction SilentlyContinue
            if ($fProc) {
                if (Test-ManagedOwnership $FrontendPidFile 5173) {
                    Write-Host "  Frontend process is running with PID: $fPid (Ownership: VERIFIED)" -ForegroundColor Green
                } else {
                    Write-Host "  Frontend process is running with PID: $fPid (Ownership: UNVERIFIED/REUSED)" -ForegroundColor Red
                }
            } else {
                Write-Host "  Frontend: Stale PID file found (PID: $fPid, process dead)" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "  Frontend: PID file not found (stopped)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Verification Utilities Check:"
    Write-Host "  Python Executable: $VenvPython " -NoNewline
    if ($VenvPython -ne "python.exe" -and (Test-Path $VenvPython)) {
        Write-Host "[OK]" -ForegroundColor Green
    } else {
        $pyCheck = Get-Command "python" -ErrorAction SilentlyContinue
        if ($pyCheck) { Write-Host "[PATH python]" -ForegroundColor Green } else { Write-Host "[NOT FOUND]" -ForegroundColor Red }
    }
    Write-Host "  Node Executable (npm): " -NoNewline
    $npmCheck = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if ($npmCheck) { Write-Host "[OK]" -ForegroundColor Green } else { Write-Host "[NOT FOUND]" -ForegroundColor Red }
    Write-Host "================================================================" -ForegroundColor Cyan
    Read-Host "Press Enter to return to Dashboard"
}

function Open-URLs {
    while ($true) {
        Clear-Host
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "                       OPEN SERVICE URLS                        " -ForegroundColor Cyan
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "  [1] Backend API Root   (http://127.0.0.1:8000)"
        Write-Host "  [2] Swagger UI         (http://127.0.0.1:8000/docs)"
        Write-Host "  [3] ReDoc              (http://127.0.0.1:8000/redoc)"
        Write-Host "  [4] Frontend           (http://localhost:5173)"
        Write-Host "  [5] RustFS Console     (http://127.0.0.1:9001)"
        Write-Host "  [0] Back"
        Write-Host "================================================================" -ForegroundColor Cyan
        
        $choice = Read-Host "Choice"
        switch ($choice) {
            "1" { Start-Process "http://127.0.0.1:8000" }
            "2" { Start-Process "http://127.0.0.1:8000/docs" }
            "3" { Start-Process "http://127.0.0.1:8000/redoc" }
            "4" { Start-Process "http://localhost:5173" }
            "5" { Start-Process "http://127.0.0.1:9001" }
            "0" { return }
            default { Write-Host "Invalid choice." -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    }
}

function Show-LogFile($relPath) {
    $filePath = Join-Path $RepoRoot $relPath
    Clear-Host
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host " Viewing Log: $relPath" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    if (Test-Path $filePath) {
        Get-Content -Path $filePath -Tail 50 -ErrorAction SilentlyContinue
    } else {
        Write-Host "Log file '$relPath' does not exist yet." -ForegroundColor Yellow
    }
    Write-Host "================================================================" -ForegroundColor Cyan
    Read-Host "Press Enter to return to Logs Menu"
}

function Open-Dir($dirPath) {
    if (Test-Path $dirPath) {
        Start-Process "explorer.exe" $dirPath
    } else {
        Write-Host "Directory '$dirPath' does not exist." -ForegroundColor Red
        Start-Sleep -Seconds 1
    }
}

function View-Logs {
    while ($true) {
        Clear-Host
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "                           VIEW LOGS                            " -ForegroundColor Cyan
        Write-Host "================================================================" -ForegroundColor Cyan
        Write-Host "  [1] View Backend Log (Last 50 lines)"
        Write-Host "  [2] View Frontend Log (Last 50 lines)"
        Write-Host "  [3] Open Application Logs Directory"
        Write-Host "  [4] Open RustFS Logs Directory"
        Write-Host "  [0] Back"
        Write-Host "================================================================" -ForegroundColor Cyan
        
        $choice = Read-Host "Choice"
        switch ($choice) {
            "1" { Show-LogFile "logs\backend.log" }
            "2" { Show-LogFile "logs\frontend.log" }
            "3" { Open-Dir $LogsDir }
            "4" { Open-Dir "E:\Projects\ascendrite-data\rustfs\logs\" }
            "0" { return }
            default { Write-Host "Invalid choice." -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    }
}

# Main event loop
while ($true) {
    $statuses = Get-FullStatus
    Show-Dashboard $statuses
    Write-Host "  [1] Start Application Stack"
    Write-Host "  [2] Start Full Development Stack"
    Write-Host "  [3] Stop Application Stack"
    Write-Host "  [4] Manage Infrastructure"
    Write-Host "  [5] Manage Application"
    Write-Host "  [6] Health and Diagnostics"
    Write-Host "  [7] Open Service URLs"
    Write-Host "  [8] View Logs"
    Write-Host "  [9] Refresh Dashboard"
    Write-Host "  [0] Exit"
    Write-Host "================================================================" -ForegroundColor Cyan
    
    $choice = Read-Host "Choice"
    switch ($choice) {
        "1" { Start-BothApps; Start-Sleep -Seconds 1 }
        "2" { Start-FullStack }
        "3" { Stop-BothApps; Start-Sleep -Seconds 1 }
        "4" { Manage-Infrastructure }
        "5" { Manage-Application }
        "6" { Show-Diagnostics }
        "7" { Open-URLs }
        "8" { View-Logs }
        "9" { # Refresh by continuing loop }
        "0" { exit 0 }
        default { Write-Host "Invalid choice." -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
}
