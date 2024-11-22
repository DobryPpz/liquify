import argparse


class Fluid:
    def __init__(self, volume: int | float = 0):
        self.volume = volume


class Base(Fluid):
    def __init__(self, nicotine_concentration: int | float, volume: int | float = 0):
        super().__init__(volume)
        self.nicotine_concentration = nicotine_concentration


class Taste(Fluid):
    def __init__(self, name: str = 'tasteless', volume: int | float = 0):
        super().__init__(volume)
        self.name = name


class TargetMix(Fluid):
    def __init__(self, volume: int | float = 0,
                 error_margin: float = 0.1,
                 target_concentration: int | float = 12):
        super().__init__(volume)
        self.taste_list = []
        self.base_list = []
        self.error_margin = error_margin
        self.target_concentration = target_concentration

    def add_taste(self, taste: Taste):
        if type(taste) is not Taste:
            raise Exception('Wrong type of taste!')
        self.taste_list.append(taste)
        return self

    def add_base(self, base: Base):
        if type(base) is not Base:
            raise Exception('Wrong type of base!')
        self.base_list.append(base)
        return self
