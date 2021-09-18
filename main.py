import random
import json
from typing import Any


def rnd_from_dict(d):
    """
    Randomly select a key from a dictionary.
    """
    return random.choice(list(d.keys()))


with open("information/first_names.json") as f:
    first_names: dict[str, list[str]] = json.load(f)

with open("information/last_names.txt") as f:
    last_names = [name.title().replace("\n", "") for name in f.readlines()]

with open("information/occupations.json") as f:
    occupations: dict[str, dict[str, dict[str, Any]]] = json.load(f)

with open("information/char_traits.json") as f:
    traits: dict[str, list[str]] = json.load(f)

with open("information/promotions.json") as f:
    promotions: dict[str, list[str]] = json.load(f)

with open("information/death_causes.json") as f:
    death_causes: dict[str, dict[str, dict[str, list]]] = json.load(f)
biological_genders = ["male", "female"]

biological_gender = random.choice(biological_genders)

if biological_gender == "male":
    name = [random.choice(first_names["male"]), random.choice(last_names)]
    if name[0].find(";") != -1:
        name[0] = random.choice(name[0].split(";"))
else:
    name = [random.choice(first_names["female"]), random.choice(last_names)]
    if name[0].find(";") != -1:
        name[0] = random.choice(name[0].split(";"))

age = random.randint(1, 120)

religions = [
    "Christianity",
    "Islam",
    "Atheism",
    "Hinduism",
    "Buddhism",
    "Sikhism",
    "Other",
]
religion = random.choices(religions, [31.11, 24.9, 15.58, 15.16, 5.06, 0.3, 7.89], k=1)[
    0
]

traits_clone = traits.copy()

trait_num = random.randint(1, 5)
good_trait_num = random.randint(1, trait_num)
bad_trait_num = trait_num - good_trait_num

# assign traits
traits_dict = {"good": [], "bad": []}
for i in range(good_trait_num):
    trait = random.choice(traits_clone["good"])
    traits_dict["good"].append(trait)
    idx = traits_clone["good"].index(trait)
    traits_clone["good"].pop(idx)

# remove opposites from bad traits
for trait in traits_dict["good"]:
    if traits_clone["opposite"].get(trait):
        traits_clone["bad"].pop(
            traits_clone["bad"].index(traits_clone["opposite"][trait])
        )


for i in range(bad_trait_num):
    trait = random.choice(traits["bad"])
    traits_dict["bad"].append(trait)
    idx = traits_clone["bad"].index(trait)
    traits_clone["bad"].pop(idx)

special_job = True if random.randint(1, 10) == 1 else False
if special_job:
    occupation_name = rnd_from_dict(occupations["special"])
    if biological_gender == "female":
        female_name = occupations["special"][occupation_name].get("female_name")
        occupation = (
            occupations["special"][occupation_name]["female_name"]
            if female_name
            else occupation_name
        )
    else:
        occupation = occupation_name
else:
    occupation_name = rnd_from_dict(occupations["normal"])
    occupation_obj = occupations["normal"][occupation_name]
    if biological_gender == "female":
        female_name = occupations["normal"][occupation_name].get("female_name")
        occupation = (
            occupations[occupation_name]["female_name"]
            if female_name
            else occupation_name
        )
    else:
        occupation = occupation_name
    if age >= 65:
        occupation = (
            "Retired " + occupation if random.randint(0, 1) == 1 else occupation
        )
if age < 18:
    occupation = "School"

if age > 50:
    if random.randint(0, 2) == 1:
        death_cause = "Complications from Old Age"
if random.randint(1, 4) == 1:
    death_cause = None
else:
    death_cause = random.choice(death_causes["death_causes"]["normal"])

print("Name:", name[0], name[1])
print("Age:", age)
print("Religion:", religion)
print("Occupation:", occupation.title())
if death_cause:
    print("Death Cause:", death_cause)
print("Character Traits")
for trait in traits_dict["good"]:
    print("-", trait)
for trait in traits_dict["bad"]:
    print("-", trait)
