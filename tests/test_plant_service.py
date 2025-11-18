"""
Unit tests for the PlantService optimization algorithm.
"""
from pydantic_core import ValidationError
import pytest
from schemas.power_plant_schema import PowerPlantSchema
from services.plant_service import PlantService
from schemas.power_grid_schema import FuelSchema, PowerGridSchema
from exceptions.unfeasible_exception import UnfeasibleException


class TestGetUnitCost:
    """Tests for the _get_unit_cost method."""

    @pytest.mark.unit
    def test_wind_turbine_unit_cost_is_zero(self, basic_wind_plant, basic_fuel):
        """Wind turbines should have zero unit cost."""
        cost = PlantService._get_unit_cost(basic_wind_plant, basic_fuel)
        assert cost == 0.0

    @pytest.mark.unit
    def test_gas_fired_unit_cost(self, basic_gas_plant, basic_fuel):
        """Gas-fired plants should have positive unit cost including CO2."""
        cost = PlantService._get_unit_cost(basic_gas_plant, basic_fuel)
        # Unit cost = fuel_price / efficiency + co2_emission_per_mwh * co2_price
        # = 13.4 / 0.53 + 0.3 * 20 = 25.28 + 6 = 31.28
        expected_cost = (basic_fuel.gasfired / basic_gas_plant.efficiency) + (0.3 * basic_fuel.co2)
        assert abs(cost - expected_cost) < 0.01

    @pytest.mark.unit
    def test_turbojet_unit_cost(self, basic_turbojet_plant, basic_fuel):
        """Turbojet plants should have positive unit cost without CO2."""
        cost = PlantService._get_unit_cost(basic_turbojet_plant, basic_fuel)
        # Unit cost = fuel_price / efficiency
        expected_cost = basic_fuel.turbojet / basic_turbojet_plant.efficiency
        assert abs(cost - expected_cost) < 0.01

    @pytest.mark.unit
    def test_zero_efficiency_raises_error(self, basic_fuel):
        """Plants with zero efficiency should return infinity cost."""
        from schemas.power_plant_schema import PowerPlantSchema
        with pytest.raises(ValidationError) as exc_info:
            plant = PowerPlantSchema(
                name="broken",
                type="gasfired",
                efficiency=0,
                pmin=0,
                pmax=100
            )

class TestSimpleProductionPlan:
    """Tests for the simple_production_plan method."""

    @pytest.mark.unit
    def test_basic_production_plan(self, multi_plant_power_grid):
        """Test basic production plan with gas and wind plants."""
        result = PlantService.simple_production_plan(multi_plant_power_grid)

        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == len(multi_plant_power_grid.powerplants)

        # Verify all plants are in result
        names = [plant["name"] for plant in result]
        for p in multi_plant_power_grid.powerplants:
            assert p.name in names

        # Verify each result has required fields
        for plant in result:
            assert "name" in plant
            assert "p" in plant
            assert isinstance(plant["p"], float)
            assert plant["p"] >= 0

    @pytest.mark.unit
    def test_production_plan_matches_load(self, multi_plant_power_grid):
        """Total production should approximately match the load."""
        result = PlantService.simple_production_plan(multi_plant_power_grid)
        total_production = sum(plant["p"] for plant in result)

        # Allow small rounding error
        assert abs(total_production - multi_plant_power_grid.load) < 1.0

    @pytest.mark.unit
    def test_production_respects_plant_constraints(self, multi_plant_power_grid):
        """Production should respect minimum and maximum constraints."""
        result = PlantService.simple_production_plan(multi_plant_power_grid)
        sorted_powerplants = PlantService()._sort_powerplants_by_cost(multi_plant_power_grid)
        
        for i, plant_result in enumerate(result):
            original_plant = sorted_powerplants[i]
            production = plant_result["p"]
            
            # Production should be between pmin and pmax or zero
            if production > 0:
                assert production >= original_plant.pmin, \
                    f"Production {production} is below minimum {original_plant.pmin}"
                assert production <= original_plant.pmax, \
                    f"Production {production} exceeds maximum {original_plant.pmax}"
    
    @pytest.mark.unit
    def test_significant_step_lower_than_production(self, multi_plant_power_grid):
        """Fixture for covering line 85: production + max_prod_units < stopping_point condition."""
        fuel = FuelSchema(**{"gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 95}
        )
        wind_plant_1 = PowerPlantSchema(
            name="windplant1",
            type="windturbine",
            efficiency=1,
            pmin=0,
            pmax=100
        )
        wind_plant_2 = PowerPlantSchema(
            name="windplant2",
            type="windturbine",
            efficiency=1,
            pmin=0,
            pmax=10
        )
        gas_plant = PowerPlantSchema(
            name="gasfired1",
            type="gasfired",
            efficiency=0.53,
            pmin=10,
            pmax=460
        )
        grid = PowerGridSchema(
            load=100,
            fuels=fuel,
            powerplants=[wind_plant_1, wind_plant_2, gas_plant]
        )

        result = PlantService().simple_production_plan(grid)

        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == len(multi_plant_power_grid.powerplants)

        # Verify all plants are in result
        names = [plant["name"] for plant in result]
        for p in grid.powerplants:
            assert p.name in names

        # Verify each result has required fields
        for plant in result:
            assert "name" in plant
            assert "p" in plant
            assert isinstance(plant["p"], float)
            assert plant["p"] >= 0


    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_wind_affects_production(self, basic_fuel, basic_gas_plant, basic_wind_plant):
        """Wind percentage should affect wind turbine production."""
        grid_low_wind = PowerGridSchema(
            load=100,
            fuels=basic_fuel,
            powerplants=[basic_gas_plant, basic_wind_plant]
        )
        result_low = PlantService.simple_production_plan(grid_low_wind)
        wind_production_low = [p["p"] for p in result_low if p["name"] == "windplant1"][0]
        
        high_wind_fuel = basic_fuel.model_copy()
        high_wind_fuel.windturbine = 100
        print(high_wind_fuel)
        grid_high_wind = PowerGridSchema(
            load=100,
            fuels=high_wind_fuel,
            powerplants=[basic_gas_plant, basic_wind_plant]
        )
        result_high = PlantService.simple_production_plan(grid_high_wind)
        wind_production_high = [p["p"] for p in result_high if p["name"] == "windplant1"][0]
        
        # Higher wind should produce more from wind turbine
        assert wind_production_high > wind_production_low

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_zero_wind_production(self, basic_fuel, basic_gas_plant, basic_wind_plant):
        """With zero wind, wind turbines should not produce."""
        no_wind_fuel = basic_fuel.model_copy()
        no_wind_fuel.windturbine = 0
        grid = PowerGridSchema(
            load=300,
            fuels=no_wind_fuel,
            powerplants=[basic_gas_plant, basic_wind_plant]
        )
        result = PlantService.simple_production_plan(grid)
        wind_production = [p["p"] for p in result if p["name"] == "windplant1"][0]
        
        assert wind_production == 0.0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_low_load_requires_single_plant(self, low_load_grid):
        """With very low load, not all plants need to be used."""
        result = PlantService.simple_production_plan(low_load_grid)
        
        # Only wind turbine should produce (cheaper than gas)
        total_production = sum(plant["p"] for plant in result)
        assert abs(total_production - low_load_grid.load) < 1.0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_infeasible_load_raises_exception(self, basic_gas_plant, basic_turbojet_plant, basic_fuel):
        """Infeasible load should raise UnfeasibleException."""
        # Create a grid where total capacity is less than load
        grid = PowerGridSchema(
            load=1000,  # Demand exceeds total capacity
            fuels=basic_fuel,
            powerplants=[
                basic_gas_plant,  # pmax=460
                basic_turbojet_plant  # pmax=10
            ]
        )
        
        with pytest.raises(UnfeasibleException) as exc_info:
            PlantService.simple_production_plan(grid)
        
        assert "No feasible solution" in str(exc_info.value.detail)

    @pytest.mark.unit
    def test_algorithm_prefers_cheapest_plants(self, multi_plant_power_grid):
        """Algorithm should prefer cheaper plants (wind > gas > turbojet in cost)."""
        result = PlantService.simple_production_plan(multi_plant_power_grid)
        
        # Convert to dict for easier access
        production_dict = {p["name"]: p["p"] for p in result}
        
        # Wind should produce at least what it can (free)
        wind_max = multi_plant_power_grid.powerplants[2].pmax * multi_plant_power_grid.fuels.windturbine / 100
        assert production_dict["windplant1"] > 0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_production_plan_with_single_plant(self, basic_fuel, basic_gas_plant):
        """Test production plan with only one plant."""
        grid = PowerGridSchema(
            load=300,
            fuels=basic_fuel,
            powerplants=[basic_gas_plant]
        )
        result = PlantService.simple_production_plan(grid)
        
        assert len(result) == 1
        assert result[0]["name"] == "gasfired1"
        assert abs(result[0]["p"] - 300) < 1.0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_production_respects_minimum_output(self, basic_fuel):
        """Plants with pmin > 0 should respect minimum output when used."""
        high_pmin_plant = basic_fuel.model_copy()
        plant = {
            "name": "high_pmin",
            "type": "gasfired",
            "efficiency": 0.5,
            "pmin": 200,
            "pmax": 400
        }
        
        from schemas.power_plant_schema import PowerPlantSchema
        plant_obj = PowerPlantSchema(**plant)
        
        grid = PowerGridSchema(
            load=100,  # Load is less than pmin
            fuels=high_pmin_plant,
            powerplants=[plant_obj]
        )
        
        # Should raise exception as load < pmin
        with pytest.raises(UnfeasibleException):
            PlantService.simple_production_plan(grid)


class TestSignificantProductionSteps:
    """Tests for the _get_significant_production_steps method."""

    @pytest.mark.unit
    def test_significant_steps_generation(self, multi_plant_power_grid):
        """Test that significant production steps are correctly generated."""
        result = PlantService._get_significant_production_steps(
            multi_plant_power_grid.powerplants,
            granularity=0.1
        )

        assert isinstance(result, list)
        assert len(result) == len(multi_plant_power_grid.powerplants)

        # Each plant should have at least some steps
        for steps in result:
            assert isinstance(steps, list)
            assert len(steps) > 0
            assert all(isinstance(step, int) for step in steps)

