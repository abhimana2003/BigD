import random
import requests

API_URL = "http://localhost:8000/profiles"


genders = ["female", "male", "other"]

goals = ["weight loss", "maintenance", "high protein", "gluten free"]

dietary_options = ["vegetarian", "vegan", "pescaterian", "low carb", "keto"]

allergy_options = ["nuts", "dairy", "gluten", "soy", "eggs"]

medical_options = ["diabetes", "hypertension", "celiac", "high cholesterol"]

budget_levels = ["low", "medium", "high"]

cooking_times = [
    "short (<30 mins)",
    "medium (30-60 min)",
    "long(>60 mins)"
]


def random_subset(options):
    """Return a random subset (possibly empty)."""
    k = random.randint(0, len(options))
    return random.sample(options, k)


def generate_random_user():
    return {
        "age": random.randint(18, 75),
        "height_cm": round(random.uniform(150, 195), 1),
        "weight_kg": round(random.uniform(50, 110), 1),
        "gender": random.choice(genders),
        "goal": random.choice(goals),
        "dietary_preferences": random_subset(dietary_options),
        "allergies": random_subset(allergy_options),
        "medical_conditions": random_subset(medical_options),
        "budget_level": random.choice(budget_levels),
        "cooking_time": random.choice(cooking_times),
    }


def seed_users(n=20):
    success = 0

    for i in range(n):
        user = generate_random_user()

        try:
            r = requests.post(API_URL, json=user)
            r.raise_for_status()
            success += 1
            print(f"Created user {i+1}")
        except requests.exceptions.HTTPError as e:
            print(f"Failed user {i+1}: {r.text}")

    print(f"\nFinished. Successfully created {success}/{n} users.")


if __name__ == "__main__":
    seed_users(30)  
