import random
import Recipe

class User:
    def __init__(self, name, age, weightInKg, heightInCm, sex, consumedFoods):
        self.name = name
        self.age = age
        self.weight = weightInKg
        self.height = heightInCm
        self.sex = sex
        self.consumedFoods = consumedFoods

    def get_steps(self):
        return random.randint(300,20000)

    def get_kcal_consumed(self):
        kCal = 0
        for food in self.consumedFoods:
            kCal += food.k_cal()
        return kCal

    def calories_burned(self):
        caloriesBurned = 0
        calories = self.get_steps
