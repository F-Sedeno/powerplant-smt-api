from pydantic import BaseModel, ConfigDict, Field

from schemas.examples import POST_PRODUCTIONPLAN_EXAMPLE
from schemas.power_plant_schema import PowerPlantSchema

class FuelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    gasfired: float = Field(validation_alias="gas(euro/MWh)")
    turbojet: float = Field(validation_alias="kerosine(euro/MWh)")
    co2: float = Field(validation_alias="co2(euro/ton)")
    windturbine: float = Field(validation_alias="wind(%)")

class PowerGridSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_schema_extra=POST_PRODUCTIONPLAN_EXAMPLE)
    load: float
    fuels: FuelSchema
    powerplants: list[PowerPlantSchema]