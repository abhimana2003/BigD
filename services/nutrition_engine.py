from storage.recipe_store import RecipeStore

store = RecipeStore()
results = store.search_recipes(max_calories=500, dietary_preferences=["vegan"])
recipe = store.get_recipe(1)