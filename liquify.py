import argparse
from functools import cache


class Fluid:
    def __init__(self, volume: int | float = 0,
                 nicotine_concentration: int | float = 0,
                 name: str = 'tasteless'):
        self.volume = volume
        self.nicotine_concentration = nicotine_concentration
        self.name = name


class TargetMix(Fluid):
    def __init__(self, target_volume: int | float = 0,
                 error_margin: float = 0.1,
                 target_concentration: int | float = 0):
        super().__init__(target_volume)
        self.taste_set = set()
        self.fluid_list = []
        self.total_volume = 0
        self.error_margin = error_margin
        self.target_concentration = target_concentration

    def add_fluid(self, fluid: Fluid):
        if type(fluid) is not Fluid:
            raise Exception('Wrong type of fluid!')
        self.taste_set.add(fluid.name)
        self.fluid_list.append(fluid)
        self.total_volume += fluid.volume
        return self
