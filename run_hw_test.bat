@echo off
REM Quick hardware validation test runner
REM Sets environment variables and runs tests

echo Setting MikroTik connection details...
set MIKROTIK_HOST=192.168.88.1
set MIKROTIK_USERNAME=admin
set MIKROTIK_PASSWORD=MaxCr33k420

echo.
echo Running hardware validation tests...
echo.

REM Run with the category specified as first argument, or all tests if no argument
if "%1"=="" (
    python tests\hardware_validation.py
) else (
    python tests\hardware_validation.py --category %1 %2 %3 %4
)

