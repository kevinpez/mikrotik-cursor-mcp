# MikroTik MCP Test Suite

Comprehensive testing for the MikroTik Cursor MCP server.

---

## Test Structure

```
tests/
├── README.md                      # This file
├── hardware_validation.py         # ⭐ NEW: Complete hardware validation suite
├── HARDWARE_TESTING_GUIDE.md      # Complete guide for hardware testing
├── test_core.py                   # Core functionality tests
├── test_comprehensive.py          # Comprehensive integration tests
├── run_tests.py                   # Test runner with options
├── unit/                          # Unit tests (future)
│   └── .gitkeep
└── integration/                   # Integration tests
    ├── test_integration_runner.py
    ├── test_all_handlers.py
    ├── comprehensive_test_suite.py
    └── test_simple_integration.py
```

---

## Running Tests

### ⭐ NEW: Hardware Validation (Recommended)

**Test ALL commands against your actual MikroTik hardware with detailed CLI feedback:**

```bash
# Test everything - see what works and what fails on your hardware
python tests/hardware_validation.py

# Test specific category with detailed output
python tests/hardware_validation.py --category System -v

# Save detailed results to JSON
python tests/hardware_validation.py --report results.json

# List all available categories
python tests/hardware_validation.py --list-categories
```

**Features:**
- ✅ Tests EVERY MCP command (400+ handlers)
- ✅ Real-time progress with color-coded results
- ✅ Shows exactly what works and what fails on your router
- ✅ Safe execution with automatic rollback
- ✅ Detailed JSON reports for CI/CD
- ✅ Category-based testing (System, Firewall, Routing, etc.)

**See [HARDWARE_TESTING_GUIDE.md](HARDWARE_TESTING_GUIDE.md) for complete documentation.**

### Quick Test
```bash
# Run core tests only
python tests/test_core.py

# Run comprehensive tests
python tests/test_comprehensive.py
```

### Using Test Runner
```bash
# Run all tests
python run_tests.py all

# Run specific test suite
python run_tests.py core
python run_tests.py comprehensive
python run_tests.py integration

# Run with verbose output
python run_tests.py all --verbose
```

### Using pytest
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=src/mcp_mikrotik

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_core.py::test_function_name
```

---

## Test Types

### Core Tests (`test_core.py`)
- ✅ Connection management
- ✅ SSH client functionality
- ✅ Basic RouterOS commands
- ✅ Error handling
- ✅ Configuration validation

**Purpose:** Verify fundamental MCP server functionality

### Comprehensive Tests (`test_comprehensive.py`)
- ✅ All MCP tools (426+ actions)
- ✅ Category-based tool organization
- ✅ Tool handler registration
- ✅ Schema validation
- ✅ End-to-end workflows

**Purpose:** Ensure complete feature coverage

### Hardware Validation Tests (`hardware_validation.py`) - ⭐ NEW
- ✅ Tests ALL 400+ MCP handlers against real hardware
- ✅ Real-time CLI feedback with color-coded results
- ✅ Category-based testing (25+ categories)
- ✅ Detailed per-command pass/fail reporting
- ✅ JSON report generation for CI/CD
- ✅ Safe execution with automatic cleanup

**Purpose:** Comprehensive validation that every command works on your actual router

### Integration Tests (`integration/`)
- ✅ Real router connectivity (if available)
- ✅ Command execution on live devices
- ✅ Multi-router scenarios
- ✅ Performance testing

**Purpose:** Validate against actual MikroTik hardware

### Unit Tests (`unit/`) - *Coming Soon*
- Isolated scope module testing
- Tool definition validation
- Utility function testing
- Mock-based testing

---

## Test Configuration

### Environment Variables
```bash
# For integration tests with real router
MIKROTIK_TEST_HOST=192.168.88.1
MIKROTIK_TEST_USERNAME=admin
MIKROTIK_TEST_PASSWORD=test-password
# Configure your MikroTik router credentials
```

### Test Data
- Test configurations in `tests/fixtures/`
- Mock responses in `tests/mocks/`
- Sample RouterOS outputs for validation

---

## Test Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Core Connection | 100% | ✅ 100% |
| MCP Tools | 95% | ✅ 100% |
| Scope Modules | 90% | 🔄 TBD |
| Safety Features | 100% | ✅ 100% |
| Error Handling | 95% | ✅ 95% |

---

## Writing Tests

### Test Naming Convention
```python
# File: test_<module>.py
# Class: Test<Feature>
# Method: test_<specific_behavior>

def test_firewall_filter_rule_creation():
    """Test creating a firewall filter rule."""
    pass
```

### Using Fixtures
```python
import pytest

@pytest.fixture
def mock_router():
    """Provide a mock MikroTik router connection."""
    # Setup
    yield mock_connection
    # Teardown
```

### Assertions
```python
# Use descriptive assertions
assert result is not None, "Expected result, got None"
assert "success" in response.lower(), f"Unexpected response: {response}"
```

---

## CI/CD Integration

Tests run automatically on:
- Every push to main branch
- Pull request creation
- Release tagging

See `.github/workflows/` for CI configuration.

---

## Troubleshooting Tests

### Common Issues

**Import Errors**
```bash
# Ensure virtual environment is activated
# Ensure package is installed in development mode
pip install -e .
```

**Connection Timeouts**
```bash
# Check router is accessible
# Verify firewall rules allow SSH
# Increase timeout in test configuration
```

**Test Failures After Changes**
```bash
# Clear pytest cache
pytest --cache-clear

# Run specific failing test with verbose output
pytest tests/test_core.py::test_name -vv
```

---

## Contributing Tests

When adding new features:
1. ✅ Write tests first (TDD)
2. ✅ Ensure tests pass locally
3. ✅ Add integration tests for router interaction
4. ✅ Update this README if adding new test types
5. ✅ Maintain 90%+ code coverage

---

## Resources

- **pytest Documentation:** https://docs.pytest.org/
- **Testing Best Practices:** See `docs/testing/`
- **MCP Testing Guide:** See MCP SDK documentation

