@echo off
setlocal
cd /d "%~dp0"
set "SCRIPT_DIR=%~dp0"
set "BATCH_PATH=%~f0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = (Get-Content -LiteralPath $env:BATCH_PATH -Raw).Split(@('#PS_' + 'START'), 2, [System.StringSplitOptions]::None); iex $c[1]"
exit /b %errorlevel%
#PS_START
# Ascendrite Platform Manager Polyglot script
# Environment variable SCRIPT_DIR is passed by batch wrapper

$ScriptDir = $env:SCRIPT_DIR
if (-not $ScriptDir) {
    $ScriptDir = (Get-Location).Path
}
$ScriptDir = $ScriptDir.TrimEnd([char]92)

if (Test-Path (Join-Path $ScriptDir "platform")) {
    $RepoRoot = $ScriptDir
    $PlatformDir = Join-Path $ScriptDir "platform"
} else {
    $PlatformDir = $ScriptDir
    $RepoRoot = Split-Path -Parent $PlatformDir
}
$ServerDir = Join-Path $PlatformDir "server"
$ClientDir = Join-Path $PlatformDir "client"
$RuntimeDir = "E:\Projects\ascendrite-data\runtime"
$BackendPidFile = Join-Path $RuntimeDir "backend.pid"
$FrontendPidFile = Join-Path $RuntimeDir "frontend.pid"
$LogsDir = Join-Path $RepoRoot "logs"

# Ensure all runtime and logs directories exist immediately at startup
if (-not (Test-Path $RuntimeDir)) {
    New-Item -ItemType Directory -Path $RuntimeDir -Force | Out-Null
}
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

# Duplicate instance check
$ManagerPidFile = Join-Path $RuntimeDir "platform-manager.pid"
$currentPid = $PID

if (Test-Path $ManagerPidFile) {
    $oldPidVal = Get-Content $ManagerPidFile -Raw -ErrorAction SilentlyContinue
    if ($oldPidVal) {
        $oldPid = [int]($oldPidVal.Trim())
        if ($oldPid -ne $currentPid) {
            $oldProc = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
            if ($oldProc) {
                $oldProcObj = Get-CimInstance Win32_Process -Filter "ProcessId = $oldPid" -ErrorAction SilentlyContinue
                if ($oldProcObj -and $oldProcObj.CommandLine -match "run-ascendrite|platform-manager") {
                    Clear-Host
                    Write-Host "================================================================" -ForegroundColor Red
                    Write-Host "                  DUPLICATE INSTANCE DETECTED                   " -ForegroundColor Red
                    Write-Host "================================================================" -ForegroundColor Red
                    Write-Host " Another instance of Ascendrite Platform Manager is running:"
                    Write-Host "   Process ID: $oldPid"
                    Write-Host "   Start Time: $($oldProc.StartTime)"
                    Write-Host "================================================================" -ForegroundColor Red
                    Write-Host "  [1] Terminate the existing instance and start here"
                    Write-Host "  [2] Keep the existing instance running and exit"
                    Write-Host "  [3] Run anyway (allow concurrent execution)"
                    Write-Host "================================================================" -ForegroundColor Red
                    $dupChoice = Read-Host "Choice"
                    if ($dupChoice -eq "1") {
                        Write-Host "Stopping existing platform manager (PID: $oldPid)..." -NoNewline
                        Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
                        Start-Sleep -Seconds 1
                        Write-Host " [OK]" -ForegroundColor Green
                    } elseif ($dupChoice -eq "2") {
                        exit 0
                    } else {
                        Write-Host "Running concurrent instance..." -ForegroundColor Yellow
                        Start-Sleep -Seconds 1
                    }
                }
            }
        }
    }
}
$currentPid | Out-File -FilePath $ManagerPidFile -Encoding ascii

# Check directory structure
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
    $netstat = netstat -ano | Select-String "LISTENING" | Select-String ":$port\s+"
    return [bool]$netstat
}

function Get-PortOccupyingPID($port) {
    $netstat = netstat -ano | Select-String "LISTENING" | Select-String ":$port\s+"
    if ($netstat) {
        $line = $netstat | Select-Object -First 1 | ForEach-Object { $_.Line.Trim() }
        $parts = $line.Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)
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

    $launcherProc = Get-Process -Id $launcherPid -ErrorAction SilentlyContinue
    if (-not $launcherProc) {
        return $false
    }

    $treePids = @($launcherPid)
    $treePids += Get-ProcessDescendants $launcherPid

    $portPidVal = Get-PortOccupyingPID $port
    if ($portPidVal) {
        $portPid = [int]$portPidVal
        if ($treePids -contains $portPid) {
            return $true
        }
    }

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
    $status = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if (-not $status) {
        return "OFFLINE"
    }
    $serviceRunning = $status.Status -eq "Running"
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

function Get-AppStatus($pidFile, $port, $url) {
    if (Test-Path $pidFile) {
        $launcherPid = Get-Content -Path $pidFile -Raw -ErrorAction SilentlyContinue
        if ($launcherPid) {
            $launcherPid = $launcherPid.Trim()
            $proc = Get-Process -Id $launcherPid -ErrorAction SilentlyContinue
            if ($proc) {
                if (Test-ManagedOwnership $pidFile $port) {
                    if (Test-PortConnection $port) {
                        return "ONLINE"
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
    return [PSCustomObject]@{
        Postgres       = Get-ServiceState "postgresql-x64-18" 5432
        MongoDB        = Get-ServiceState "MongoDB" 27017
        Redis          = Get-ServiceState "Memurai" 6379
        RustFS_S3      = Get-ServiceState "AscendriteRustFS" 9000
        RustFS_Console = Get-ServiceState "AscendriteRustFS" 9001
        Backend        = Get-AppStatus $BackendPidFile 8000 "http://127.0.0.1:8000"
        Frontend       = Get-AppStatus $FrontendPidFile 5173 "http://localhost:5173"
    }
}

function Write-StatusLabel($label, $status) {
    Write-Host "   $($label.PadRight(15)): " -NoNewline
    if ($status -eq "ONLINE") {
        Write-Host "[ONLINE]" -ForegroundColor Green
    } elseif ($status -eq "OFFLINE") {
        Write-Host "[OFFLINE]" -ForegroundColor Gray
    } else {
        Write-Host "[$status]" -ForegroundColor Yellow
    }
}

function Show-Dashboard($statuses) {
    Clear-Host
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                  ASCENDRITE PLATFORM MANAGER                   " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host " Infrastructure:" -ForegroundColor Gray
    Write-StatusLabel "PostgreSQL" $statuses.Postgres
    Write-StatusLabel "MongoDB" $statuses.MongoDB
    Write-StatusLabel "Memurai (Redis)" $statuses.Redis
    Write-StatusLabel "RustFS S3" $statuses.RustFS_S3
    Write-StatusLabel "RustFS Console" $statuses.RustFS_Console
    Write-Host " Applications:" -ForegroundColor Gray
    Write-StatusLabel "Backend API" $statuses.Backend
    Write-StatusLabel "Frontend SPA" $statuses.Frontend
    Write-Host "================================================================" -ForegroundColor Cyan
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
                    Write-Host "[ERROR] Admin privileges required to start '$svc'." -ForegroundColor Red
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
                        Write-Host "[ERROR] Admin privileges required to stop '$svc'." -ForegroundColor Red
                    }
                }
            }
        }
        Start-Sleep -Seconds 2
    }
}

function Start-BackendApp {
    Write-Host "Verifying infrastructure requirements..."
    $statuses = Get-FullStatus
    if ($statuses.Postgres -ne "ONLINE" -or $statuses.MongoDB -ne "ONLINE" -or $statuses.Redis -ne "ONLINE") {
        Write-Host "[WARN] Infrastructure services are not fully online. Starting in degraded mode." -ForegroundColor Yellow
    }

    if ($VenvPython -eq "python.exe") {
        $pyCheck = Get-Command "python" -ErrorAction SilentlyContinue
        if (-not $pyCheck) {
            Write-Host "[ERROR] Python not found." -ForegroundColor Red
            Read-Host "Press Enter to continue"
            return $false
        }
    }

    Write-Host "Testing python interpreter and uvicorn availability..."
    $output = & $VenvPython -c "import uvicorn; print('OK')" 2>$null
    if ($output) {
        $output = ($output -join "").Trim()
    }
    if ($output -ne "OK") {
        Write-Host "[ERROR] Selected Python interpreter ($VenvPython) cannot import 'uvicorn'." -ForegroundColor Red
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
        Write-Host "[ERROR] Port 8000 occupied by unmanaged process (PID: $occupyPid)." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    if (Test-Path $BackendPidFile) {
        Remove-Item $BackendPidFile -Force -ErrorAction SilentlyContinue
    }

    Write-Host "Starting Backend API Server..."
    $logPath = Join-Path $LogsDir "backend.log"
    
    try {
        $cmdLine = "/c $VenvPython -m uvicorn main:app --host 127.0.0.1 --port 8000 >> $logPath 2>&1"
        $proc = Start-Process -FilePath "cmd.exe" -ArgumentList $cmdLine -WorkingDirectory $ServerDir -PassThru -NoNewWindow
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
        Write-Host "[ERROR] Failed to start Backend: $_" -ForegroundColor Red
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

function Start-FrontendApp {
    $npmCheck = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if (-not $npmCheck) {
        Write-Host "[ERROR] npm not found in PATH." -ForegroundColor Red
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
        Write-Host "[ERROR] Port 5173 occupied by unmanaged process (PID: $occupyPid)." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return $false
    }

    if (Test-Path $FrontendPidFile) {
        Remove-Item $FrontendPidFile -Force -ErrorAction SilentlyContinue
    }

    Write-Host "Starting Frontend Server..."
    $logPath = Join-Path $LogsDir "frontend.log"
    
    try {
        $cmdLine = "/c npm run dev >> $logPath 2>&1"
        $proc = Start-Process -FilePath "cmd.exe" -ArgumentList $cmdLine -WorkingDirectory $ClientDir -PassThru -NoNewWindow
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
        Write-Host "[ERROR] Failed to start Frontend: $_" -ForegroundColor Red
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
    Start-BothApps
}

function Stop-FullStack {
    Write-Host "Stopping Full Stack..."
    Stop-BothApps
    Stop-AllInfra
}

function Show-Diagnostics {
    Clear-Host
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "                       SYSTEM DIAGNOSTICS                       " -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "Port Occupancy Check:"
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
    Write-Host "Environment Checks:"
    Write-Host "  Python: $VenvPython"
    Write-Host "  Admin role: $isAdmin"
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
        Write-Host "  [3] Open Logs Directory"
        Write-Host "  [0] Back"
        Write-Host "================================================================" -ForegroundColor Cyan
        $choice = Read-Host "Choice"
        switch ($choice) {
            "1" { Show-LogFile "logs\\backend.log" }
            "2" { Show-LogFile "logs\\frontend.log" }
            "3" { Open-Dir $LogsDir }
            "0" { return }
        }
    }
}

function Exit-PlatformManager {
    $ManagerPidFile = Join-Path $RuntimeDir "platform-manager.pid"
    if (Test-Path $ManagerPidFile) {
        $myPidVal = Get-Content $ManagerPidFile -Raw -ErrorAction SilentlyContinue
        if ($myPidVal -and [int]($myPidVal.Trim()) -eq $PID) {
            Remove-Item $ManagerPidFile -Force -ErrorAction SilentlyContinue
        }
    }
    exit 0
}

# Main event loop
while ($true) {
    $statuses = Get-FullStatus
    Show-Dashboard $statuses
    Write-Host "  [1] Start Applications (Backend + Frontend)"
    Write-Host "  [2] Stop Applications"
    Write-Host "  [3] Start Full Stack   (Infrastructure + Apps)"
    Write-Host "  [4] Stop Full Stack    (Infrastructure + Apps)"
    Write-Host "  [5] View Logs          (Backend & Frontend)"
    Write-Host "  [6] Open Service URLs"
    Write-Host "  [7] Run Diagnostics"
    Write-Host "  [0] Exit"
    Write-Host "================================================================" -ForegroundColor Cyan
    
    $choice = Read-Host "Choice"
    switch ($choice) {
        "1" { Start-BothApps; Start-Sleep -Seconds 1 }
        "2" { Stop-BothApps; Start-Sleep -Seconds 1 }
        "3" { Start-FullStack; Start-Sleep -Seconds 1 }
        "4" { Stop-FullStack; Start-Sleep -Seconds 1 }
        "5" { View-Logs }
        "6" { Open-URLs }
        "7" { Show-Diagnostics }
        "0" { Exit-PlatformManager }
    }
}
