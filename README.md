# powerplant-smt-api

Coding Challenge for ENGIE Application by Francisco José Sedeño Guerrero.

## Overview

The API provides an endpoint that calculates the optimal production configuration for a list of power plants, minimizing operational costs based on plant specifications (costs, minimum and maximum output).

## Deployment

The API is deployed at `localhost:8888/productionplan`

## Installation

### Manual Setup

1. Create virtual environment: `python -m venv env`
2. Activate environment: `env/scripts/activate`
3. Install dependencies: `pip install -r requirements.txt --no-cache-dir`
4. Run application: `python main.py`

### Docker Setup

Build and run the Docker container for automatic deployment:

```bash
# Build the Docker image
docker build -t powerplant-smt-api .

# Run the container
docker run --name powerplant-smt-api -p 8888:8888 powerplant-smt-api
```

## Usage

Send a POST request to `localhost:8888/productionplan` with your power plant configuration to receive the optimal production plan.

Access `localhost:8888/docs` to see OpenAPI 3.1 specification of the endpoints with body examples and return types

## Testing

A comprehensive test suite is included covering unit tests and integration tests.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run specific test file
pytest tests/test_plant_service.py
```

For detailed test documentation, see [tests/README.md](tests/README.md)

### Test Coverage

The test suite includes:
- **Unit Tests**: 20+ tests for the PlantService optimization algorithm
- **Integration Tests**: 25+ tests for the /productionplan endpoint
- **Edge Cases**: Comprehensive boundary condition testing
- **Validation**: Input validation and error handling tests

Current coverage target: **99%+**