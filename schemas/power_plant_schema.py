from typing_extensions import Literal
from pydantic import BaseModel, ConfigDict, Field

class PowerPlantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    type: Literal["gasfired", "turbojet", "windturbine"]
    efficiency: float = Field(gt=0)
    pmax: int = Field(gt=0)
    pmin: int = Field(ge=0)
    

class PowerPlantResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    p: float