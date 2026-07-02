@echo off
setlocal enabledelayedexpansion

:: ============================================================
::  Ascendrite Platform Manager
::  Manages backend (FastAPI :8000) and frontend (Vite :5173)
:: ============================================================

set "PLATFORM_DIR=%~dp0"
set "BACKEND_PORT=8000"
set "FRONTEND_PORT=5173"
set "BACKEND_PY=python-venv-3.10.11\Scripts\python.exe"

:: ─────────────────────────────────────────────────────────────
:menu
cls
echo.
echo  ================================================================
echo          Ascendrite Platform Manager
echo  ================================================================
echo.

:: ── Backend Status ──────────────────────────────────────────
call :check_port %BACKEND_PORT% BACKEND_RUNNING
if !BACKEND_RUNNING! equ 1 (
    echo   [RUNNING]  Backend   ^|  http://127.0.0.1:%BACKEND_PORT%
) else (
    echo   [STOPPED]  Backend   ^|  port %BACKEND_PORT%
)

:: ── Frontend Status ─────────────────────────────────────────
call :check_port %FRONTEND_PORT% FRONTEND_RUNNING
if !FRONTEND_RUNNING! equ 1 (
    echo   [RUNNING]  Frontend  ^|  http://localhost:%FRONTEND_PORT%
) else (
    echo   [STOPPED]  Frontend  ^|  port %FRONTEND_PORT%
)

echo.
echo  ================================================================
echo    1.  Turn on  Backend
echo    2.  Turn on  Frontend
echo    3.  Turn off Backend
echo    4.  Turn off Frontend
echo    5.  Turn off Both ^& Exit
echo  ================================================================
echo.

set "choice="
set /p choice="  Choice (1-5): "
echo.

if "%choice%"=="1" goto action_backend_on
if "%choice%"=="2" goto action_frontend_on
if "%choice%"=="3" goto action_backend_off
if "%choice%"=="4" goto action_frontend_off
if "%choice%"=="5" goto action_exit_all

echo   [ERROR]  Invalid choice. Please enter 1-5.
timeout /t 2 >nul
goto menu

:: ─────────────────────────────────────────────────────────────
:action_backend_on
if !BACKEND_RUNNING! equ 1 (
    echo   [INFO]  Backend is already running on http://127.0.0.1:%BACKEND_PORT%
) else (
    echo   Starting backend...
    start /b "" cmd /c "cd /d "%PLATFORM_DIR%server" && "%BACKEND_PY%" -m uvicorn main:app --host 127.0.0.1 --port %BACKEND_PORT% >> backend.log 2>&1"
    call :wait_for_port %BACKEND_PORT% 10 STARTED
    if !STARTED! equ 1 (
        echo   [OK]  Backend is ON  --  http://127.0.0.1:%BACKEND_PORT%
    ) else (
        echo   [WARN]  Backend may still be starting. Check server\backend.log
    )
)
timeout /t 2 >nul
goto menu

:: ─────────────────────────────────────────────────────────────
:action_frontend_on
if !FRONTEND_RUNNING! equ 1 (
    echo   [INFO]  Frontend is already running on http://localhost:%FRONTEND_PORT%
) else (
    echo   Starting frontend...
    start /b "" cmd /c "cd /d "%PLATFORM_DIR%client" && npm run dev >> frontend.log 2>&1"
    call :wait_for_port %FRONTEND_PORT% 15 STARTED
    if !STARTED! equ 1 (
        echo   [OK]  Frontend is ON  --  http://localhost:%FRONTEND_PORT%
    ) else (
        echo   [WARN]  Frontend may still be starting. Check client\frontend.log
    )
)
timeout /t 2 >nul
goto menu

:: ─────────────────────────────────────────────────────────────
:action_backend_off
if !BACKEND_RUNNING! equ 0 (
    echo   [INFO]  Backend is already stopped.
) else (
    echo   Stopping backend...
    call :kill_port %BACKEND_PORT%
    echo   [OK]  Backend is OFF.
)
timeout /t 2 >nul
goto menu

:: ─────────────────────────────────────────────────────────────
:action_frontend_off
if !FRONTEND_RUNNING! equ 0 (
    echo   [INFO]  Frontend is already stopped.
) else (
    echo   Stopping frontend...
    call :kill_port %FRONTEND_PORT%
    echo   [OK]  Frontend is OFF.
)
timeout /t 2 >nul
goto menu

:: ─────────────────────────────────────────────────────────────
:action_exit_all
echo   Shutting everything down...
if !BACKEND_RUNNING! equ 1 (
    call :kill_port %BACKEND_PORT%
    echo   - Backend stopped.
) else (
    echo   - Backend was already stopped.
)
if !FRONTEND_RUNNING! equ 1 (
    call :kill_port %FRONTEND_PORT%
    echo   - Frontend stopped.
) else (
    echo   - Frontend was already stopped.
)
echo.
echo   Goodbye.
timeout /t 2 >nul
exit /b 0

:: ─────────────────────────────────────────────────────────────
:: :check_port <port> <outVar>
::   Sets outVar to 1 if something is LISTENING on <port>, else 0.
:check_port
set "%~2=0"
for /f "tokens=*" %%L in ('netstat -ano ^| findstr "LISTENING" ^| findstr /r ":%~1 "') do (
    set "%~2=1"
)
exit /b

:: ─────────────────────────────────────────────────────────────
:: :kill_port <port>
::   Kills all PIDs listening on <port>.
:kill_port
for /f "tokens=5" %%P in ('netstat -ano ^| findstr "LISTENING" ^| findstr /r ":%~1 "') do (
    taskkill /f /pid %%P >nul 2>&1
)
exit /b

:: ─────────────────────────────────────────────────────────────
:: :wait_for_port <port> <maxSeconds> <outVar>
::   Polls every second until port is LISTENING or timeout.
:wait_for_port
set "%~3=0"
set /a "_tries=%~2"
:_wait_loop
call :check_port %~1 _up
if !_up! equ 1 (
    set "%~3=1"
    exit /b
)
set /a "_tries=_tries-1"
if !_tries! leq 0 exit /b
timeout /t 1 >nul
goto _wait_loop
