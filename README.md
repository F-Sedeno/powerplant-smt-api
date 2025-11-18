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
docker run -p 8888:8888 powerplant-smt-api
```

## Usage

Send a POST request to `/productionplan` with your power plant configuration to receive the optimal production plan.

