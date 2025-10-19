# MikroTik MCP Testing Workflow

## Testing Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MikroTik MCP Testing Suite                      │
└─────────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Set Environment Vars │
                    │  - MIKROTIK_HOST      │
                    │  - MIKROTIK_USER      │
                    │  - MIKROTIK_PASSWORD  │
                    └───────────┬───────────┘
                                │
                ┌───────────────┴────────────────┐
                │                                │
                ▼                                ▼
    ┌───────────────────────┐      ┌────────────────────────┐
    │  Quick Development    │      │  Complete Validation   │
    │       Testing         │      │      Testing          │
    └───────────┬───────────┘      └────────┬───────────────┘
                │                           │
                ▼                           ▼
    ┌───────────────────────┐      ┌────────────────────────┐
    │  Test Specific        │      │  Test All Categories   │
    │  Category             │      │  (451 handlers)        │
    │                       │      │                        │
    │  $ python tests/      │      │  $ python tests/       │
    │    hardware_          │      │    hardware_           │
    │    validation.py      │      │    validation.py       │
    │    --category System  │      │    --report full.json  │
    └───────────┬───────────┘      └────────┬───────────────┘
                │                           │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Connectivity Check  │
                │   to Router           │
                └───────────┬───────────┘
                            │
                ┌───────────┴──────────┐
                │                      │
                ▼                      ▼
        ┌───────────┐          ┌──────────────┐
        │  Success  │          │   Failed     │
        └─────┬─────┘          └──────┬───────┘
              │                       │
              │                       ▼
              │              ┌─────────────────┐
              │              │ Check:          │
              │              │ - Host correct? │
              │              │ - Firewall OK?  │
              │              │ - Credentials?  │
              │              └─────────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Run Tests by        │
              │   Category            │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  Read-Only Tests │    │  Write Tests     │
    │  (Safe)          │    │  (With Cleanup)  │
    │                  │    │                  │
    │  - list commands │    │  - create test   │
    │  - get commands  │    │    objects       │
    │  - monitor       │    │  - verify        │
    │  - check         │    │  - cleanup       │
    └────────┬─────────┘    └─────────┬────────┘
             │                        │
             └────────┬───────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  Real-Time Progress   │
          │                       │
          │  [1/10] cmd1  ✓ PASS │
          │  [2/10] cmd2  ✓ PASS │
          │  [3/10] cmd3  ⊘ SKIP │
          │  [4/10] cmd4  ✗ FAIL │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  Category Summary     │
          │                       │
          │  Passed:  8/10 (80%)  │
          │  Failed:  1           │
          │  Skipped: 1           │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  Final Connectivity   │
          │  Check                │
          └───────────┬───────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    ┌──────────┐          ┌─────────────────┐
    │  Router  │          │  ⚠ WARNING:     │
    │  Still   │          │  Lost           │
    │  OK ✓    │          │  Connectivity   │
    └────┬─────┘          └─────────────────┘
         │
         ▼
┌────────────────────────┐
│  Generate Final Report │
│                        │
│  Overall:              │
│  - Total: 451          │
│  - Passed: 368 (81.6%) │
│  - Failed: 15          │
│  - Skipped: 68         │
│                        │
│  By Category:          │
│  ✓ System: 12/15       │
│  ✓ Firewall: 32/35     │
│  ✓ Routing: 28/42      │
│  ...                   │
└────────┬───────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌──────────────┐
│ CLI   │  │ JSON Report  │
│Output │  │ (Optional)   │
└───┬───┘  └──────┬───────┘
    │             │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │   Review &   │
    │   Fix Issues │
    └──────────────┘
           │
           ▼
         END
```

## Testing Workflow Examples

### Workflow 1: Quick Development Testing

```bash
# You're working on firewall features
1. Make code changes
2. python tests/hardware_validation.py --category Firewall -v
3. Review output, fix issues
4. Repeat until tests pass
5. Run full suite before commit
```

### Workflow 2: Complete System Validation

```bash
# Full hardware validation
1. python tests/hardware_validation.py --report full.json
2. Review overall pass rate
3. Check category-specific results
4. Investigate failures
5. Review skipped tests (expected?)
6. Archive report for comparison
```

### Workflow 3: Regression Testing

```bash
# Before making changes
1. python tests/hardware_validation.py --report before.json

# Make your changes

# After changes
2. python tests/hardware_validation.py --report after.json

# Compare
3. diff before.json after.json
4. Investigate any new failures
```

### Workflow 4: CI/CD Pipeline

```bash
# Automated pipeline
1. Code pushed to repository
2. CI triggers test job
3. python tests/hardware_validation.py --report ci.json
4. Exit code checked (0=pass, 1=fail)
5. Report uploaded as artifact
6. Pass/fail status shown in PR
```

## Test Category Selection Guide

### When to Test Specific Categories

**System** - After RouterOS upgrade, system config changes
```bash
python tests/hardware_validation.py --category System
```

**Firewall** - After firewall changes, security updates
```bash
python tests/hardware_validation.py --category Firewall
```

**Routing** - After route changes, BGP/OSPF config
```bash
python tests/hardware_validation.py --category Routing
```

**Interfaces** - After interface config, bridge changes
```bash
python tests/hardware_validation.py --category Interfaces
```

**All Categories** - Before release, after major changes
```bash
python tests/hardware_validation.py
```

## Understanding Results

### High Pass Rate (>90%)
```
✅ Excellent - System is working well
   Action: None, continue development
```

### Medium Pass Rate (70-90%)
```
⚠ Good - Some issues need attention
   Action: Review failed tests, check compatibility
```

### Low Pass Rate (<70%)
```
❌ Needs Investigation
   Action: 
   1. Check RouterOS version compatibility
   2. Verify hardware capabilities
   3. Review configuration
   4. Check logs
```

## Test Output Interpretation

### Status Symbols

```
✓ PASS  → Command executed successfully
✗ FAIL  → Command returned error, needs investigation
⊘ SKIP  → Expected skip (not supported/dangerous)
```

### Category Results

```
Results by Category:
  ✓ System          : 12/15 (80.0%) [F:1 S:2]
     │   │    │      │  │      └─ Skipped: 2
     │   │    │      │  └──────── Failed: 1  
     │   │    │      └─────────── Pass rate
     │   │    └────────────────── Total tests
     │   └─────────────────────── Passed tests
     └─────────────────────────── Status (✓/⚠/✗)
```

## Safety Checkpoints

The test suite includes multiple safety checkpoints:

```
Before Tests:
  ✓ Verify connectivity
  ✓ Get router identity
  ✓ Check environment setup

During Tests:
  ✓ Skip dangerous operations
  ✓ Protect critical resources
  ✓ Use test object prefixes
  ✓ Track created objects

After Tests:
  ✓ Final connectivity check
  ✓ Cleanup test objects
  ✓ Report warnings
```

## Troubleshooting Decision Tree

```
Test Failed?
    │
    ├─ Connection Error?
    │   ├─ Yes → Check host/firewall/credentials
    │   └─ No → Continue
    │
    ├─ "Not Supported" Error?
    │   ├─ Yes → Expected, router lacks feature
    │   └─ No → Continue
    │
    ├─ Permission Error?
    │   ├─ Yes → Check user permissions
    │   └─ No → Continue
    │
    └─ Command Error?
        ├─ Check RouterOS version
        ├─ Review command syntax
        ├─ Check router logs
        └─ Report bug if unexpected
```

## Integration Points

### Development
```
Code Change → Category Test → Fix → Full Test → Commit
```

### CI/CD
```
Push → CI Trigger → Full Test → Report → Pass/Fail Status
```

### Release
```
Pre-release → Full Test → Review → Fix Issues → Release
```

### User Validation
```
Install → Configure → Run Tests → Verify → Use
```

## Best Practices

1. **Start Small** - Test one category first
2. **Use Verbose** - When debugging specific issues
3. **Save Reports** - For historical comparison
4. **Regular Testing** - After changes and upgrades
5. **Review Skips** - Ensure they're expected
6. **CI Integration** - Automate validation
7. **Document Failures** - Note router-specific issues

## Conclusion

This workflow ensures:
- ✅ Comprehensive testing coverage
- ✅ Real hardware validation
- ✅ Clear feedback and reporting
- ✅ Safe execution
- ✅ Easy integration into development
- ✅ Continuous quality assurance

