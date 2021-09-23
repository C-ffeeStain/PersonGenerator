import json
import logging
import os
import random as rnd
from typing import Any

import discord
import discord.ext.commands as commands
from dotenv import load_dotenv

from errors import *

load_dotenv()

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="main.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


def rnd_from_dict(d):
    """
    Randomly select a key from a dictionary.
    """
    return rnd.choice(list(d.keys()))


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

religions = [
    "Christianity",
    "Islam",
    "Atheism",
    "Hinduism",
    "Buddhism",
    "Sikhism",
    "Other",
]
biological_genders = ["male", "female"]

bot_token = os.environ["BOT_TOKEN"]
bot = commands.Bot(command_prefix="rp;")


@bot.event
async def on_ready():
    logger.log(logging.INFO, "logged in as {}!".format(bot.user))


def random_person(gender=None):
    if gender:
        biological_gender = gender.lower()
    else:
        biological_gender = rnd.choice(biological_genders)

    if biological_gender == "male":
        name = [rnd.choice(first_names["male"]), rnd.choice(last_names)]
        if name[0].find(";") != -1:
            name[0] = rnd.choice(name[0].split(";"))
    elif biological_gender == "female":
        name = [rnd.choice(first_names["female"]), rnd.choice(last_names)]
        if name[0].find(";") != -1:
            name[0] = rnd.choice(name[0].split(";"))
    else:
        return

    age = rnd.randint(1, 120)

    religion = rnd.choices(
        religions, [31.11, 24.9, 15.58, 15.16, 5.06, 0.3, 7.89], k=1
    )[0]

    traits_clone = traits.copy()

    trait_num = rnd.randint(1, 5)
    good_trait_num = rnd.randint(1, trait_num)
    bad_trait_num = trait_num - good_trait_num

    # assign traits
    traits_dict = {"good": [], "bad": []}
    for i in range(good_trait_num):
        trait = rnd.choice(traits_clone["good"])
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
        trait = rnd.choice(traits["bad"])
        traits_dict["bad"].append(trait)
        idx = traits_clone["bad"].index(trait)
        traits_clone["bad"].pop(idx)

    special_job = True if rnd.randint(1, 10) == 1 else False
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
                "Retired " + occupation if rnd.randint(0, 1) == 1 else occupation
            )
    if age < 18:
        occupation = "School"

    if age > 50:
        if rnd.randint(0, 2) == 1:
            death_cause = "Complications from Old Age"
    if rnd.randint(1, 4) == 1:
        death_cause = None
    else:
        death_cause = rnd.choice(death_causes["death_causes"]["normal"])

    return {
        "name": name,
        "age": age,
        "gender": biological_gender,
        "religion": religion,
        "occupation": occupation,
        "traits": traits_dict,
        "death_cause": death_cause,
    }


@bot.command()
async def random(ctx, gender: str = "rnd"):
    embed = discord.Embed(title="Random Person", color=0x00FF00)

    if gender != "rnd":
        person = random_person(gender)
    else:
        person = random_person()

    if person["gender"] not in biological_genders:
        await ctx.send(f"'{person['gender']}' is not a valid gender.")
        return

    embed.add_field(
        name="Name", value=person["name"][0] + " " + person["name"][1], inline=False
    )
    embed.add_field(name="Age", value=person["age"], inline=False)
    embed.add_field(name="Occupation", value=person["occupation"].title(), inline=False)
    embed.add_field(name="Sex", value=person["gender"].title())
    embed.add_field(name="Religion", value=person["religion"], inline=False)
    embed.add_field(
        name="Traits",
        value=", ".join(person["traits"]["good"] + person["traits"]["bad"]),
        inline=False,
    )
    if person["death_cause"]:
        embed.add_field(
            name="Cause of Death", value=person["death_cause"], inline=False
        )

    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")
    elif isinstance(error, InvalidGender):
        await ctx.send("That is not a valid gender. Please specify 'male' or 'female'.")


bot.run(bot_token)
