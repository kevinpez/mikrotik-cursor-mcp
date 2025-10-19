@echo off
REM Quick hardware validation test runner with verbose output

echo Setting MikroTik connection details...
set MIKROTIK_HOST=192.168.88.1
set MIKROTIK_USERNAME=admin
set MIKROTIK_PASSWORD=MaxCr33k420

echo.
echo Running hardware validation tests (VERBOSE MODE)...
echo.

if "%1"=="" (
    python tests\hardware_validation.py --verbose
) else (
    python tests\hardware_validation.py --category %1 --verbose
)

