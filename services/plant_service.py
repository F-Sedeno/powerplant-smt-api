from exceptions.unfeasible_exception import UnfeasibleException
from schemas.power_grid_schema import PowerGridSchema
import math

class PlantService():
    
    @staticmethod
    def _get_unit_cost(plant, fuels):
        if plant.type == "windturbine":
            return 0.0
        fuel_price = getattr(fuels, plant.type)
        if plant.efficiency == 0:
            return float("inf")
        
        fuel_total_cost = fuel_price / plant.efficiency
        if plant.type == "gasfired":
            co2_price = fuels.co2
            co2_emission_per_mwh = 0.3  
            fuel_total_cost += co2_emission_per_mwh * co2_price
        return fuel_total_cost
    
    @staticmethod
    def _get_significant_production_steps(powerplants, granularity):
        significant_production_steps = [[] for _ in range(len(powerplants))]
        for plant_index in reversed(range(len(powerplants))):
            powerplant = powerplants[plant_index]
            pmin_adjusted = int(math.ceil(powerplant.pmin / granularity))
            if plant_index == len(powerplants)-1:
                significant_production_steps[plant_index] = [0, pmin_adjusted]
            else:
                for element in significant_production_steps[plant_index+1]:
                    significant_production_steps[plant_index].extend([element, element + pmin_adjusted])
            significant_production_steps[plant_index] = list(set(significant_production_steps[plant_index]))
            significant_production_steps[plant_index].sort()
            significant_production_steps[plant_index].reverse()
        return significant_production_steps

    @staticmethod
    def simple_production_plan(power_grid: PowerGridSchema):

        granularity = 0.1  
        LOAD = int(round(power_grid.load / granularity))
        n = len(power_grid.powerplants)

        INF = float("inf")
        production_costs = {0: 0}

        prevs = [] # list of dicts to reconstruct allocation

        powerplants_greedy = [powerplant for powerplant in sorted(
            power_grid.powerplants,
            key=lambda p: PlantService._get_unit_cost(p, power_grid.fuels)
        )]

        significant_production_steps = PlantService()._get_significant_production_steps(powerplants_greedy, granularity)

        #For each powerplant, calculate possible productions
        for index, powerplant in enumerate(powerplants_greedy):

            unit_cost = PlantService._get_unit_cost(powerplant, power_grid.fuels)

            # If wind turbine, pmax depends on wind
            if powerplant.type == "windturbine":
                max_units = powerplant.pmax * getattr(power_grid.fuels, "windturbine") / 100.0
            else:
                max_units = powerplant.pmax

            min_units = int(math.ceil(powerplant.pmin / granularity)) if powerplant.pmin is not None else 0

            max_units = int(math.floor(max_units / granularity)) if max_units is not None else LOAD

            # maximum producible units for this plant (bounded by total demand D)
            max_prod_units = LOAD if max_units is None else min(max_units, LOAD)

            # get significant stopping points for this plant
            stopping_points = []
            if min_units <= max_prod_units:
                stopping_points.extend([LOAD-step for step in significant_production_steps[index] if max_prod_units-step >= min_units])

            # new layer starts from no production from this plant
            prev = {key:key for key in production_costs}
            new_production_costs = production_costs.copy()

            # for each previous production, try to add production from this plant based on significant production stopping points
            for production in production_costs:
                for stopping_point in stopping_points:
                    if stopping_point < production:
                        continue
                    if production + max_prod_units < stopping_point:
                        new_production = production + max_prod_units
                    else:
                        new_production = stopping_point
                    cost = math.floor(production_costs[production] + (new_production-production) * unit_cost)
                    if new_production not in production_costs or cost < production_costs[new_production]:
                        new_production_costs[new_production] = cost
                        prev[new_production] = production

            production_costs = new_production_costs
            prevs.append(prev)

        # if target load has not been reached, raise exception
        if LOAD not in production_costs:
            raise UnfeasibleException("No feasible solution for the requested load.")

        # reconstruct allocation by backtracking through prevs
        alloc = [0] * n
        acc_load = LOAD
        for i in range(n - 1, -1, -1):
            stopping_point = prevs[i][acc_load]
            units_produced = acc_load - stopping_point
            if stopping_point is INF:
                stopping_point = 0
            alloc[i] = units_produced
            acc_load -= units_produced

        # convert allocations back to MW and produce result list
        result = []
        for fac, mw_units in zip(powerplants_greedy, alloc):
            result.append({"name": fac.name, "p": round(mw_units * granularity, 1)})

        return result