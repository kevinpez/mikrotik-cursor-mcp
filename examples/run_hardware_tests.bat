@echo off
REM
REM Example script for running MikroTik MCP hardware validation tests (Windows)
REM This demonstrates various ways to use the hardware validation suite
REM

echo MikroTik MCP Hardware Validation Examples
echo ==========================================
echo.

REM Check if environment variables are set
if "%MIKROTIK_HOST%"=="" (
    echo ERROR: MIKROTIK_HOST environment variable not set
    echo.
    echo Please set your MikroTik connection details:
    echo   set MIKROTIK_HOST=192.168.88.1
    echo   set MIKROTIK_USER=admin
    echo   set MIKROTIK_PASSWORD=your-password
    echo.
    exit /b 1
)

echo Router: %MIKROTIK_HOST%
echo User: %MIKROTIK_USER%
echo.

REM Create reports directory
if not exist test_reports mkdir test_reports

REM Example 1: Quick system check
echo Example 1: Quick System Health Check
echo --------------------------------------
python tests\hardware_validation.py --category System
echo.

REM Example 2: Test firewall with verbose output
echo Example 2: Detailed Firewall Testing
echo -------------------------------------
python tests\hardware_validation.py --category Firewall -v
echo.

REM Example 3: Full validation with report
echo Example 3: Complete Hardware Validation
echo ----------------------------------------
python tests\hardware_validation.py --report test_reports\full_validation.json
echo.

REM Example 4: Test critical categories
echo Example 4: Test Critical Categories
echo ------------------------------------
for %%c in (System Interfaces Firewall Routing) do (
    echo Testing %%c...
    python tests\hardware_validation.py --category %%c --report test_reports\%%c_results.json
)
echo.

echo All examples completed!
echo Reports saved to test_reports\
dir test_reports

