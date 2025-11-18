"""
Integration tests for the /productionplan endpoint.
"""
import pytest


class TestProductionPlanEndpoint:
    """Tests for the /productionplan endpoint."""

    @pytest.mark.integration
    def test_endpoint_success_with_valid_input(self, client, multi_plant_power_grid):
        """Test successful production plan calculation with valid input."""
        payload = multi_plant_power_grid.model_dump(by_alias=True)
        print(payload)
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert all("name" in item and "p" in item for item in data)

    @pytest.mark.integration
    def test_endpoint_returns_correct_content_type(self, client, multi_plant_power_grid):
        """Test that endpoint returns JSON content type."""
        payload = multi_plant_power_grid.model_dump(by_alias=True)
        response = client.post("/productionplan", json=payload)
        
        assert response.headers["content-type"] == "application/json"

    @pytest.mark.integration
    def test_endpoint_with_multi_plant_grid(self, client, multi_plant_power_grid):
        """Test endpoint with multiple plant types."""
        payload = multi_plant_power_grid.model_dump(by_alias=True)
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have all three plants
        assert len(data) == 3
        names = [item["name"] for item in data]
        assert "gasfired1" in names
        assert "turbojet1" in names
        assert "windplant1" in names

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_with_infeasible_load(self, client, basic_fuel, basic_gas_plant, basic_turbojet_plant):
        """Test endpoint returns error for infeasible load."""
        from schemas.power_grid_schema import PowerGridSchema
        
        grid = PowerGridSchema(
            load=1000,
            fuels=basic_fuel,
            powerplants=[basic_gas_plant, basic_turbojet_plant]
        )
        payload = grid.model_dump(by_alias=True)
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data or "message" in data or data.get("status_code") == 400

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_missing_load_field(self, client, basic_fuel, basic_gas_plant):
        """Test endpoint validation fails when load is missing."""
        payload = {
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422  # Validation error

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_missing_fuels_field(self, client, basic_gas_plant):
        """Test endpoint validation fails when fuels are missing."""
        payload = {
            "load": 500,
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_empty_powerplants_list(self, client, basic_fuel):
        """Test endpoint validation fails with empty powerplants list."""
        payload = {
            "load": 500,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": []
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422 or response.status_code == 400

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_negative_load(self, client, basic_fuel, basic_gas_plant):
        """Test endpoint validation fails with negative load."""
        payload = {
            "load": -100,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_zero_load(self, client, basic_fuel, basic_gas_plant):
        """Test endpoint validation fails with zero load."""
        payload = {
            "load": 0,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_negative_fuel_price(self, client, basic_gas_plant):
        """Test endpoint validation fails with negative fuel price."""
        payload = {
            "load": 500,
            "fuels": {
                "gas(euro/MWh)": -10,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_wind_percentage_exceeds_100(self, client, basic_gas_plant):
        """Test endpoint validation fails when wind percentage > 100."""
        payload = {
            "load": 500,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 150
            },
            "powerplants": [basic_gas_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_invalid_plant_type(self, client, basic_fuel):
        """Test endpoint validation fails with invalid plant type."""
        payload = {
            "load": 500,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [
                {
                    "name": "invalid",
                    "type": "nuclear",  # Invalid type
                    "efficiency": 0.9,
                    "pmin": 100,
                    "pmax": 500
                }
            ]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_missing_plant_field(self, client, basic_fuel):
        """Test endpoint validation fails when plant field is missing."""
        payload = {
            "load": 500,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [
                {
                    "name": "incomplete",
                    "type": "gasfired"
                    # Missing efficiency, pmin, pmax
                }
            ]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 422

    @pytest.mark.integration
    def test_endpoint_method_not_allowed_get(self, client):
        """Test that GET method is not allowed on /productionplan."""
        response = client.get("/productionplan")
        
        assert response.status_code == 405  # Method Not Allowed

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_with_very_large_load(self, client, basic_fuel):
        """Test endpoint with very large load."""
        from schemas.power_plant_schema import PowerPlantSchema
        
        large_capacity_plant = PowerPlantSchema(
            name="large",
            type="gasfired",
            efficiency=0.5,
            pmin=0,
            pmax=100000
        )
        payload = {
            "load": 50000,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [large_capacity_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        total_production = sum(item["p"] for item in data)
        assert abs(total_production - 50000) < 1.0

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_endpoint_with_very_small_load(self, client, basic_fuel, basic_wind_plant):
        """Test endpoint with very small load."""
        payload = {
            "load": 0.5,
            "fuels": basic_fuel.model_dump(by_alias=True),
            "powerplants": [basic_wind_plant.model_dump()]
        }
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        total_production = sum(item["p"] for item in data)
        assert abs(total_production - 0.5) < 0.1

    @pytest.mark.integration
    def test_endpoint_response_structure(self, client, multi_plant_power_grid):
        """Test that response has correct structure."""
        payload = multi_plant_power_grid.model_dump(by_alias=True)
        response = client.post("/productionplan", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        for item in data:
            assert "name" in item, "Response should contain 'name' field"
            assert "p" in item, "Response should contain 'p' field"
            assert len(item) == 2, "Response should only contain 'name' and 'p' fields"
            assert isinstance(item["name"], str)
            assert isinstance(item["p"], (int, float))
