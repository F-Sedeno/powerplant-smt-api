from fastapi import APIRouter

from schemas.power_grid_schema import PowerGridSchema
from schemas.power_plant_schema import PowerPlantResponseSchema
from services.plant_service import PlantService

#should be /plant, but to comply with the challenge requirements, it is left empty
router = APIRouter(prefix="")

@router.post(
    "/productionplan",
    summary="Get best production plan for a list of powerplants",
    response_model=list[PowerPlantResponseSchema]  
)
async def get_production_plan(power_grid: PowerGridSchema):
    response = PlantService().simple_production_plan(power_grid)
    return response