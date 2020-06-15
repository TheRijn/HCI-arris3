import User
import Recipe
import Ingredient

pasta = Ingredient.Ingredient("Pasta", 2.5, 300, 200)
tomatoe = Ingredient.Ingredient("Tomatoe", 1.0, 20, 350)
tuna = Ingredient.Ingredient("Tuna", 3.0, 200, 350)
salad = Ingredient.Ingredient("Salad", 0.5, 10, 200)
dish1 = [pasta, tomatoe, tuna]
dish2 = [pasta, salad]

spaghetti = Recipe.Recipe("Spaghetti", dish1)
pastaSalad = Recipe.Recipe("Pasta Salad", dish2)

eatenToday = [spaghetti, pastaSalad]

Joe = User.User("Joe", 64, 84, 180, True, eatenToday)

print(Joe.get_steps())
print(Joe.get_kcal_consumed())
