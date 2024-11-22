import argparse


class Fluid:
    def __init__(self, volume: int | float = 0, nicotine_concentration: int | float = 0, name: str = 'tasteless'):
        self.volume = volume
        self.nicotine_concentration = nicotine_concentration
        self.name = name


class TargetMix(Fluid):
    def __init__(self, volume: int | float = 0,
                 error_margin: float = 0.1,
                 target_concentration: int | float = 0):
        super().__init__(volume)
        self.taste_list = []
        self.base_list = []
        self.error_margin = error_margin
        self.target_concentration = target_concentration

    def add_taste(self, taste: Fluid):
        if type(taste) is not Fluid:
            raise Exception('Wrong type of taste!')
        self.taste_list.append(taste)
        return self

    def add_base(self, base: Fluid):
        if type(base) is not Fluid:
            raise Exception('Wrong type of base!')
        self.base_list.append(base)
        return self
