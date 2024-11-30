class Fluid:
    def __init__(self, volume: int | float = 0,
                 nicotine_concentration: int | float = 0,
                 name: str = 'fluid',
                 taste: str = 'tasteless'):
        self.volume = volume
        self.nicotine_concentration = nicotine_concentration
        self.name = name
        self.taste = taste

    def __str__(self):
        return f'{self.name};{self.volume}ml;{self.nicotine_concentration}(mg/ml);{self.taste}'


class TargetMix(Fluid):
    def __init__(self, target_volume: int | float = 0,
                 error_margin: float = 0.1,
                 target_concentration: int | float = 0,
                 milliliter_step: int | float = 1):
        super().__init__(target_volume)
        self.taste_set = set()
        self.fluid_list = []
        self.total_volume = 0
        self.error_margin = error_margin
        self.target_concentration = target_concentration
        self.milliliter_step = milliliter_step

    def add_fluid(self, fluid: Fluid):
        if type(fluid) is not Fluid:
            raise Exception('Wrong type of fluid!')
        self.taste_set.add(fluid.taste)
        self.fluid_list.append(fluid)
        self.total_volume += fluid.volume
        return self
    # -1 -> too small concentration
    # 0 -> exactly right concentration
    # 1 -> too big concentration

    def calculate(self, index: int,
                  total_conc: float,
                  total_v: float,
                  ingredients: list,
                  dp: dict):
        key = (index, format(total_conc, '.3f'), format(total_v, '.3f'))
        if key in dp:
            return dp[key]
        if index >= len(self.fluid_list) or total_v >= self.volume:
            if abs(total_conc-self.target_concentration) <= self.error_margin \
                    and abs(total_v-self.volume) <= self.error_margin:
                dp[key] = 0
                return 0
            else:
                if total_conc > self.target_concentration:
                    dp[key] = 1
                    return 1
                else:
                    dp[key] = -1
                    return -1
        curr_fluid = self.fluid_list[index]
        curr_conc = curr_fluid.nicotine_concentration
        v_r = min(self.volume-total_v, curr_fluid.volume)+self.milliliter_step
        v_l = self.milliliter_step
        prev_conc = total_conc
        while v_l <= v_r:
            choose_v = (v_l+v_r)/2
            total_conc = (prev_conc*total_v + curr_conc *
                          choose_v)/(total_v+choose_v)
            ret = self.calculate(index+1, total_conc,
                                 total_v+choose_v, ingredients, dp)
            if ret == 0:
                ingredients.append((index, choose_v))
                dp[key] = 0
                return 0
            elif ret == 1:  # concentration too large
                if curr_conc > self.target_concentration:
                    v_r = choose_v - self.milliliter_step
                else:
                    v_l = choose_v + self.milliliter_step
            elif ret == -1:  # concentration too small
                if curr_conc > self.target_concentration:
                    v_l = choose_v + self.milliliter_step
                else:
                    v_r = choose_v - self.milliliter_step
        if curr_conc > self.target_concentration:
            dp[key] = 1
            return 1
        else:
            dp[key] = -1
            return -1

    def get_mix(self):
        ingredients = []
        dp = {}
        self.calculate(0, 0, 0, ingredients, dp)
        if len(ingredients) == 0:
            return ['Such mix is impossible.']
        step_list = []
        for fluid_index, amount in ingredients:
            fluid_name = self.fluid_list[fluid_index].name
            step_list.append(f'Add {amount} ml of {fluid_name}.')
        return step_list


soczek = Fluid(5, 4, 'dark labs green', 'green tea')
herbata = Fluid(5, 4, 'dark labs oranhe', 'orange')
pizza = Fluid(5, 2, 'dark labs pizza', 'pizza')
baza = Fluid(10, 18, 'nicotex')
cat = Fluid(5, 0, 'dark labs cat', 'cat')
dog = Fluid(20,3,'dark labs dog', 'dog poo')
target = TargetMix(15, 0.1, 12, 0.1)
target.add_fluid(soczek)
target.add_fluid(baza)
target.add_fluid(herbata)
target.add_fluid(pizza)
target.add_fluid(cat)
target.add_fluid(dog)
print(target.get_mix())
