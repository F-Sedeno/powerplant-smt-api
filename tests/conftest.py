"""
Pytest configuration and fixtures for the powerplant-smt-api tests.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from schemas.power_grid_schema import PowerGridSchema, FuelSchema
from schemas.power_plant_schema import PowerPlantSchema


@pytest.fixture
def client():
    """Fixture providing a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def basic_fuel():
    """Fixture providing basic fuel prices."""
    return FuelSchema(
        **{
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        }
    )


@pytest.fixture
def basic_gas_plant():
    """Fixture providing a basic gas-fired power plant."""
    return PowerPlantSchema(
        name="gasfired1",
        type="gasfired",
        efficiency=0.53,
        pmin=100,
        pmax=460
    )


@pytest.fixture
def basic_wind_plant():
    """Fixture providing a basic wind turbine plant."""
    return PowerPlantSchema(
        name="windplant1",
        type="windturbine",
        efficiency=1,
        pmin=0,
        pmax=100
    )


@pytest.fixture
def basic_turbojet_plant():
    """Fixture providing a basic turbojet power plant."""
    return PowerPlantSchema(
        name="turbojet1",
        type="turbojet",
        efficiency=0.30,
        pmin=0,
        pmax=10
    )



@pytest.fixture
def multi_plant_power_grid(basic_fuel, basic_gas_plant, basic_wind_plant, basic_turbojet_plant):
    """Fixture providing a power grid with multiple types of plants."""
    return PowerGridSchema(
        load=500,
        fuels=basic_fuel,
        powerplants=[basic_gas_plant, basic_turbojet_plant, basic_wind_plant]
    )


@pytest.fixture
def low_load_grid(basic_fuel, basic_gas_plant, basic_wind_plant):
    """Fixture providing a grid with low load."""
    return PowerGridSchema(
        load=50,
        fuels=basic_fuel,
        powerplants=[basic_gas_plant, basic_wind_plant]
    )
