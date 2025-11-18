from pydantic import BaseModel, ConfigDict, Field

from schemas.examples import POST_PRODUCTIONPLAN_EXAMPLE
from schemas.power_plant_schema import PowerPlantSchema

class FuelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    gasfired: float = Field(alias="gas(euro/MWh)", gt=0)
    turbojet: float = Field(alias="kerosine(euro/MWh)", gt=0)
    co2: float = Field(alias="co2(euro/ton)", gt=0)
    windturbine: float = Field(alias="wind(%)", ge=0, le=100)

class PowerGridSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_schema_extra=POST_PRODUCTIONPLAN_EXAMPLE)
    load: float = Field(gt=0)
    fuels: FuelSchema
    powerplants: list[PowerPlantSchema]