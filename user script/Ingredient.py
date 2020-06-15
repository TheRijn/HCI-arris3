import math

class Ingredient:
    def __init__(self, name, cost, kCalPerHundred, grams):
        self.name = name
        self.cost = cost
        self.kCalPerHundred = kCalPerHundred
        self.grams = grams

    def k_cal(self):
        return math.ceil(self.grams * self.kCalPerHundred / 100)
