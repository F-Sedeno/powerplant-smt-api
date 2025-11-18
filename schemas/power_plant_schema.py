from typing_extensions import Literal
from pydantic import BaseModel, ConfigDict

class PowerPlantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    type: Literal["gasfired", "turbojet", "windturbine"]
    efficiency: float
    pmax: int
    pmin: int
    

class PowerPlantResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    p: float