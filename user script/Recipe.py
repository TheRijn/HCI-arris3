import Ingredient

class Recipe:

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients


    def cost(self):
        cost = 0
        for i in self.ingredients:
            cost += i.cost
        return cost

    def k_cal(self):
        kCal = 0
        for i in self.ingredients:
            kCal += i.k_cal()
        return kCal
