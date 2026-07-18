@echo off
echo Starting RustFS for Ascendrite...
echo.

:: Detect rustfs.exe in PATH, or fallback to known D:\ location
set RUSTFS_EXE=rustfs.exe
where %RUSTFS_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    if exist "D:\RustFS\Service\rustfs.exe" (
        set RUSTFS_EXE="D:\RustFS\Service\rustfs.exe"
    ) else (
        echo [ERROR] rustfs.exe not found in PATH or at D:\RustFS\Service\rustfs.exe.
        exit /b 1
    )
)

%RUSTFS_EXE% server "G:\Projects\ascendrite-data\rustfs\data" --address 127.0.0.1:9000 --console-enable --console-address 127.0.0.1:9001 --access-key-file "G:\Projects\ascendrite-private\secrets\rustfs-access-key.txt" --secret-key-file "G:\Projects\ascendrite-private\secrets\rustfs-secret-key.txt" --region ap-south-1 --buffer-profile GeneralPurpose
