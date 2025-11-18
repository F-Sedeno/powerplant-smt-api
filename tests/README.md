# Test Suite Documentation

## Overview
This directory contains a comprehensive test suite for the powerplant-smt-api, including unit tests for the optimization algorithm and integration tests for the API endpoints.

## Test Structure

### Files
- **`conftest.py`**: Pytest configuration and shared fixtures for tests
- **`test_plant_service.py`**: Unit tests for the PlantService algorithm
- **`test_endpoints.py`**: Integration tests for the /productionplan endpoint

### Test Organization
Tests are organized into classes for better readability and grouped by functionality:

- **Unit Tests** (`@pytest.mark.unit`): Test individual functions and methods in isolation
- **Integration Tests** (`@pytest.mark.integration`): Test complete API endpoints with real requests
- **Edge Case Tests** (`@pytest.mark.edge_case`): Test boundary conditions and error scenarios

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_plant_service.py
pytest tests/test_endpoints.py
```

### Run Specific Test Class
```bash
pytest tests/test_endpoints.py::TestProductionPlanEndpoint
```

### Run Specific Test
```bash
pytest tests/test_endpoints.py::TestProductionPlanEndpoint::test_endpoint_success_with_valid_input
```

### Run Tests with Coverage Report
```bash
pytest --cov=. --cov-report=html
```
This generates an HTML coverage report in `htmlcov/index.html`

### Run Only Unit Tests
```bash
pytest -m unit
```

### Run Only Integration Tests
```bash
pytest -m integration
```

### Run Only Edge Case Tests
```bash
pytest -m edge_case
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Output Capture Disabled (see print statements)
```bash
pytest -s
```

## Test Coverage

The test suite includes:

### PlantService Unit Tests (test_plant_service.py)

#### TestGetUnitCost
- Wind turbines have zero cost
- Gas-fired plants include fuel and CO2 costs
- Turbojet plants have fuel cost only
- Zero efficiency plants return infinity cost

#### TestSimpleProductionPlan
- Basic production planning with multiple plant types
- Production totals match the required load
- Production respects plant min/max constraints
- Wind percentage affects production
- Zero wind prevents wind turbine production
- Infeasible loads raise appropriate exceptions
- Algorithm prefers cheapest plants first
- Single plant scenarios work correctly
- Minimum output constraints are respected

#### TestSignificantProductionSteps
- Significant production steps are correctly generated

### Endpoint Integration Tests (test_endpoints.py)

#### TestProductionPlanEndpoint
- Valid input returns successful response
- Correct content type in response headers
- Multiple plant types handled correctly
- Infeasible loads return 400 error
- Missing required fields return 422 validation error
- Empty powerplants list validation
- Negative and zero load validation
- Negative fuel prices validation
- Wind percentage > 100 validation
- Invalid plant types validation
- Missing plant fields validation
- GET method not allowed (405)
- Very large loads handled correctly
- Very small loads handled correctly
- Response structure validation
- Output order matches input order

## Test Fixtures

Fixtures are defined in `conftest.py` and provide:

- **`client`**: TestClient for FastAPI application
- **`basic_fuel`**: Standard fuel prices (60% wind)
- **`basic_gas_plant`**: Gas-fired plant (460 MW max)
- **`basic_wind_plant`**: Wind turbine (100 MW max)
- **`basic_turbojet_plant`**: Turbojet plant (10 MW max)
- **`multi_plant_power_grid`**: Grid with three plant types
- **`low_load_grid`**: Grid with 50 MW load

## Configuration

Test configuration is in `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = --verbose --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=80
```

This configuration:
- Discovers tests in the `tests/` directory
- Requires 80% code coverage minimum
- Generates HTML coverage reports
- Shows all test names and results in verbose mode

## Expected Test Results

When running the full test suite, you should see:
- All tests pass (green checkmarks)
- Coverage report showing > 99% coverage
- No warnings about missing imports (after `pip install -r requirements.txt`)

