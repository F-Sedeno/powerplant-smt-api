POST_PRODUCTIONPLAN_EXAMPLE = {
        "example1": {
            "value": {
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
                        "pmax": 460,
                    },
                    {
                        "name": "windplant1",
                        "type": "windturbine",
                        "efficiency": 1,
                        "pmin": 0,
                        "pmax": 100,
                    }
                ]
            }
        }
    }
