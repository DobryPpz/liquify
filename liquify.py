"""
    Liquify: An e-liquid mixer
    Copyright (C) 2024  Aleksander Modzelewski

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import random
random.seed()


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

    def evaluate_mix(self, mix: list[tuple]):
        total_amount = 0
        total_nicotine = 0
        wrongness = 0
        for fluid_index, amount in mix:
            total_amount += amount
            current_fluid = self.fluid_list[fluid_index]
            total_nicotine += current_fluid.nicotine_concentration*amount
            if amount > current_fluid.volume or amount <= 0:
                wrongness += 1
        return wrongness + abs(self.volume-total_amount) + \
            abs(self.target_concentration-(total_nicotine/total_amount))

    def generate_mix(self):
        mix = []
        for i in range(len(self.fluid_list)):
            current_fluid = self.fluid_list[i]
            min_volume_step = 1
            max_volume_step = int(current_fluid.volume/self.milliliter_step)
            step = random.randint(min_volume_step, max_volume_step)
            volume = step*self.milliliter_step
            mix.append((i, volume))
        return mix

    def random_crossover(self, parent_a, parent_b):
        crosspoint = random.randint(1, len(self.fluid_list)-1)
        child_a = [*parent_a[:crosspoint], *parent_b[crosspoint:]]
        child_b = [*parent_b[:crosspoint], *parent_a[crosspoint:]]
        return child_a, child_b

    def mutate(self, mix: list[tuple]):
        mutate_point = random.randrange(0, len(self.fluid_list))
        index, amount = mix[mutate_point]
        if random.random() > 0.5:
            amount += self.milliliter_step
        else:
            amount -= self.milliliter_step
        mix[mutate_point] = (index, amount)

    def calculate(self):
        P = 20*len(self.fluid_list)
        population = []
        offspring = []
        for _ in range(P):
            population.append(self.generate_mix())
        best_fitness = float('inf')
        best_solution = None
        non_improve_counter = 0
        while best_fitness > 0 and non_improve_counter < 20:
            population.sort(key=lambda pop: self.evaluate_mix(pop))
            population = population[:len(population)//2]
            while len(offspring) < P:
                parent_a, parent_b = random.choices(population, k=2)
                offspring.extend(self.random_crossover(parent_a, parent_b))
            has_improved = False
            for child in offspring:
                fitness = self.evaluate_mix(child)
                if fitness < best_fitness:
                    has_improved = True
                    best_fitness = fitness
                    best_solution = child[:]
            for child in offspring:
                self.mutate(child)
            population = offspring
            offspring = []
            if has_improved:
                non_improve_counter = 0
            else:
                non_improve_counter += 1
        return best_solution

    def get_mix(self):
        ingredients = self.calculate()
        if len(ingredients) == 0:
            return ['We couldn\'t find the desired mix.']
        step_list = []
        for fluid_index, amount in ingredients:
            fluid_name = self.fluid_list[fluid_index].name
            step_list.append(f'Add {amount} ml of {fluid_name}.')
        return step_list
