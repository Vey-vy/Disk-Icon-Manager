@echo off
title Disk Icon Maker - Build

echo.
echo ==============================
echo     Disk Icon Maker Build
echo ==============================
echo.

echo [1/3] Cleaning old build files...

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Disk Icon Maker.spec" del /q "Disk Icon Maker.spec"

echo.
echo [2/3] Building EXE...

python -m PyInstaller ^
    --clean ^
    --onefile ^
    --windowed ^
    --name "Disk Icon Maker" ^
    --icon "assets\app.ico" ^
    src/app.py

if errorlevel 1 (
    echo.
    echo ==============================
    echo BUILD FAILED
    echo ==============================
    echo.
    pause
    exit /b 1
)

echo.
echo ==============================
echo BUILD SUCCESSFUL
echo ==============================
echo.
echo EXE:
echo dist\Disk Icon Maker.exe
echo.

echo [3/3] Opening dist folder...

explorer "dist"

pause