"""
Common test data and scenarios for testing.
Can be used as reference for manual API testing.
"""

# Scenario 1: Basic mixed energy grid (gas + wind)
SCENARIO_BASIC_MIXED = {
    "load": 910,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 60
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "windplant1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 100
        }
    ]
}

# Scenario 2: High wind percentage (reduces reliance on gas)
SCENARIO_HIGH_WIND = {
    "load": 500,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 100
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "windplant1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 300
        }
    ]
}

# Scenario 3: No wind (all energy from conventional sources)
SCENARIO_NO_WIND = {
    "load": 300,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 0
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.30,
            "pmin": 0,
            "pmax": 200
        }
    ]
}

# Scenario 4: Multiple plant types with high load
SCENARIO_MULTI_HIGH_LOAD = {
    "load": 800,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 30
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.30,
            "pmin": 0,
            "pmax": 200
        },
        {
            "name": "windplant1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
        }
    ]
}

# Scenario 5: Low load optimization
SCENARIO_LOW_LOAD = {
    "load": 50,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 80
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.30,
            "pmin": 0,
            "pmax": 200
        },
        {
            "name": "windplant1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 500
        }
    ]
}

# Scenario 6: Expensive kerosine (prefer gas)
SCENARIO_EXPENSIVE_KEROSINE = {
    "load": 400,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 100.0,
        "co2(euro/ton)": 20,
        "wind(%)": 0
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.30,
            "pmin": 0,
            "pmax": 200
        }
    ]
}

# Scenario 7: High CO2 cost (incentivizes lower emissions)
SCENARIO_HIGH_CO2_COST = {
    "load": 500,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 100,
        "wind(%)": 50
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "windplant1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 300
        }
    ]
}

# Scenario 8: Very low efficiency plant
SCENARIO_LOW_EFFICIENCY = {
    "load": 300,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 0
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.25,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.15,
            "pmin": 0,
            "pmax": 200
        }
    ]
}

# Invalid scenarios for error testing
SCENARIO_INVALID_NEGATIVE_LOAD = {
    "load": -100,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 60
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        }
    ]
}

SCENARIO_INVALID_INFEASIBLE = {
    "load": 1000,
    "fuels": {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 0
    },
    "powerplants": [
        {
            "name": "gasfired1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "turbojet1",
            "type": "turbojet",
            "efficiency": 0.30,
            "pmin": 0,
            "pmax": 100
        }
    ]
}

# Expected outputs for reference scenarios
EXPECTED_OUTPUTS = {
    "SCENARIO_BASIC_MIXED": [
        {"name": "gasfired1", "p": 850.0},
        {"name": "windplant1", "p": 60.0}
    ],
    "SCENARIO_HIGH_WIND": [
        {"name": "gasfired1", "p": 0.0},
        {"name": "windplant1", "p": 300.0}  # Wind covers most/all demand
    ],
    "SCENARIO_NO_WIND": [
        {"name": "gasfired1", "p": 300.0},
        {"name": "turbojet1", "p": 0.0}  # Wind is not available
    ],
}

# Endpoints
API_BASE_URL = "http://localhost:8888"
PRODUCTION_PLAN_ENDPOINT = f"{API_BASE_URL}/productionplan"
DOCS_URL = f"{API_BASE_URL}/docs"

# Example curl commands for manual testing
CURL_EXAMPLES = """
# Basic test
curl -X POST "http://localhost:8888/productionplan" \
  -H "Content-Type: application/json" \
  -d '{
    "load": 910,
    "fuels": {
      "gas(euro/MWh)": 13.4,
      "kerosine(euro/MWh)": 50.8,
      "co2(euro/ton)": 20,
      "wind(%)": 60
    },
    "powerplants": [
      {
        "name": "gasfired1",
        "type": "gasfired",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460
      },
      {
        "name": "windplant1",
        "type": "windturbine",
        "efficiency": 1,
        "pmin": 0,
        "pmax": 100
      }
    ]
  }'

# View API documentation
curl -X GET "http://localhost:8888/docs"
"""
