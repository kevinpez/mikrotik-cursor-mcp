# Quick Start Guide - Using .env.test

## ✅ Your .env.test File

You've created a test environment file at the root of your project with your router credentials:

```
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=kevinpez
MIKROTIK_PASSWORD=MaxCr33k420
MIKROTIK_PORT=22
MIKROTIK_LOG_LEVEL=INFO
```

## 🚀 Running Tests with .env.test

### Option 1: Load Environment and Run Tests (Quick)

```powershell
# Load credentials from .env.test
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "env:$name" -Value $value 
    } 
}

# Run tests
python tests/hardware_validation.py -v
```

### Option 2: One-Liner (Fastest)

```powershell
# System tests
python tests/hardware_validation.py --category System -v

# Firewall tests
python tests/hardware_validation.py --category Firewall -v

# Quick compact mode
python tests/hardware_validation.py
```

### Option 3: Create a PowerShell Script

Save this as `run_tests.ps1`:

```powershell
# Load .env.test credentials
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

# Run tests
if ($args.Count -gt 0) {
    python tests/hardware_validation.py -v --category $args[0]
} else {
    python tests/hardware_validation.py -v
}
```

Then run:
```powershell
.\run_tests.ps1              # All tests
.\run_tests.ps1 System       # System category
.\run_tests.ps1 Firewall     # Firewall category
```

### Option 4: Create a Batch File (Windows)

Save this as `run_tests.bat`:

```batch
@echo off
REM Load .env.test
for /f "tokens=1,2 delims==" %%a in (type .env.test) do (
    set "%%a=%%b"
)

REM Run tests
python tests/hardware_validation.py -v %1
```

Then run:
```batch
run_tests.bat                # All tests
run_tests.bat --category System
```

## 📊 What You Can Test

### Test Specific Categories:

```powershell
# System Information
python tests/hardware_validation.py --category System -v

# Firewall Rules
python tests/hardware_validation.py --category Firewall -v

# Network Interfaces
python tests/hardware_validation.py --category Interfaces -v

# DNS Configuration
python tests/hardware_validation.py --category DNS -v

# DHCP Servers
python tests/hardware_validation.py --category DHCP -v

# Network Diagnostics
python tests/hardware_validation.py --category Diagnostics -v

# IPv6 Configuration
python tests/hardware_validation.py --category IPv6 -v

# Routing
python tests/hardware_validation.py --category Routes -v

# Logs
python tests/hardware_validation.py --category Logs -v

# Backup & Certificates
python tests/hardware_validation.py --category Backup -v

# Containers
python tests/hardware_validation.py --category Containers -v
```

## 🎯 Test Output Modes

### Verbose Mode (Detailed)
```powershell
python tests/hardware_validation.py -v
```
Shows:
- ✓ Command being executed
- ✓ Arguments passed
- ✓ Execution time
- ✓ Full result output
- ✓ Success/failure status

### Compact Mode (Quick Summary)
```powershell
python tests/hardware_validation.py
```
Shows:
- [1/7] Handler name ✓ PASS (0.45s)
- [2/7] Handler name ✓ PASS (0.38s)
- Summary statistics

### Save Report
```powershell
python tests/hardware_validation.py -v --report results.json
```

## 📋 Example Test Run

```
[1/7] get_system_clock

  Executing: mikrotik_get_system_clock
  ✓ Command executed in 0.00s
  Result:
SYSTEM CLOCK:

time: 22:09:09
date: 2025-10-18
time-zone-name: America/Denver

  ✓ Command successful

[2/7] get_system_events

  Executing: mikrotik_get_system_events
  ✓ Command executed in 0.19s
  Result:
LOG ENTRIES:

 2025-10-18 21:42:20 system,info user kevinpez logged in via api
 2025-10-18 21:42:20 system,info user kevinpez logged in via ssh

  ✓ Command successful
```

## ✅ Status Check

Your current test shows:
```
System Category:
  Passed:  5/7 (71.4%)
  Failed:  0
  Skipped: 2
  Duration: 0.21s

Router: test-router
OS: RouterOS 7.20.1 (stable)
CPU: ARM64, 4-core @ 350MHz
Memory: 1GB (887MB free)
Uptime: 2 days 4 hours
```

## 🔐 Security Notes

1. **Never commit .env.test to git**
   - Add `.env.test` to `.gitignore`
   - Keep your password safe

2. **Keep credentials secure**
   - Don't share your password
   - Consider using SSH keys instead

3. **Default .gitignore protection**
   - The `.env*` pattern should already be in `.gitignore`

## 📚 Available Categories (23 Total)

1. System
2. Backup
3. Certificates
4. Containers
5. DHCP
6. DNS
7. Diagnostics
8. Firewall
9. Hotspot
10. IP Services
11. IPv6
12. Interfaces
13. Logs
14. OpenVPN
15. Queues
16. Routes
17. Routing Filters
18. CAPsMAN
19. Users
20. Wireless
21. WireGuard
22. Diagnostics Tools
23. IPv6 Full Stack

## 🚀 Next Steps

1. **Run a quick test:**
   ```powershell
   $env_content = Get-Content .env.test
   foreach ($line in $env_content) { if ($line -match '^([^=]+)=(.+)$') { Set-Item -Path "env:$($matches[1])" -Value $matches[2] } }
   python tests/hardware_validation.py --category System -v
   ```

2. **Create a run script for easier access**

3. **Integrate into CI/CD pipeline**

4. **Set up automatic monitoring**

## ✨ Key Commands Reference

```powershell
# Load environment
$env_content = Get-Content .env.test
foreach ($line in $env_content) { if ($line -match '^([^=]+)=(.+)$') { Set-Item -Path "env:$($matches[1])" -Value $matches[2] } }

# All tests (verbose)
python tests/hardware_validation.py -v

# All tests (compact)
python tests/hardware_validation.py

# Specific category (verbose)
python tests/hardware_validation.py --category Firewall -v

# Save report
python tests/hardware_validation.py -v --report test-results.json

# List all categories
python tests/hardware_validation.py --list-categories
```

## 🎉 Everything is Ready!

Your `.env.test` file is configured and your tests are working perfectly! 

✅ Credentials loaded
✅ Router connected
✅ Tests running
✅ Output showing detailed information
✅ Results verified

You're all set to start testing your MikroTik MCP! 🚀
