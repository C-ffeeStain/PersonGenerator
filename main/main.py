from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QDesktopWidget,
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
import random
import json
from typing import Any
from copy import deepcopy
import sys
from pathlib import Path
from appdirs import user_data_dir

app_name = "random_person_generator"
app_author = "c_ffeestain"

data_dir = user_data_dir(app_name, app_author)


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

religions = [
    "Christianity",
    "Islam",
    "Atheism",
    "Hinduism",
    "Buddhism",
    "Sikhism",
    "Other",
]

sexes = ["Male", "Female"]


if hasattr(sys, "_MEIPASS"):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Random Person Generator")
        self.setGeometry(300, 600, 400, 350)
        self.center()
        self.setFont(QFont("Arial", 16))
        self.setWindowIcon(QIcon(str(BASE_DIR / "icon.png")))

        self.person_name_label = QLabel("Name", self)
        self.person_name_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_name_label.adjustSize()
        self.person_name_label.move(20, 10)

        self.person_name = QLabel("John Doe", self)
        self.person_name.adjustSize()
        self.person_name.move(115, 10)

        self.person_age_label = QLabel("Age", self)
        self.person_age_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_age_label.adjustSize()
        self.person_age_label.move(20, 40)

        self.person_age = QLabel("69", self)
        self.person_age.adjustSize()
        self.person_age.move(115, 40)

        self.person_sex_label = QLabel("Sex", self)
        self.person_sex_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_sex_label.adjustSize()
        self.person_sex_label.move(20, 70)

        self.person_sex = QLabel("Male", self)
        self.person_sex.adjustSize()
        self.person_sex.move(115, 70)

        self.person_religion_label = QLabel("Religion", self)
        self.person_religion_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_religion_label.adjustSize()
        self.person_religion_label.move(20, 100)

        self.person_religion = QLabel("Other", self)
        self.person_religion.adjustSize()
        self.person_religion.move(115, 100)

        self.person_job_label = QLabel("Job", self)
        self.person_job_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_job_label.adjustSize()
        self.person_job_label.move(20, 130)

        self.person_job = QLabel("Unemployed", self)
        self.person_job.adjustSize()
        self.person_job.move(115, 130)

        self.person_traits_label = QLabel("Traits", self)
        self.person_traits_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.person_traits_label.adjustSize()
        self.person_traits_label.move(20, 160)

        self.person_traits = QLabel("None", self)
        self.person_traits.adjustSize()
        self.person_traits.move(115, 160)

        self.generate_rnd_person_btn = QPushButton("Random", self)
        self.generate_rnd_person_btn.adjustSize()
        self.generate_rnd_person_btn.move(
            int(self.width() / 2 - self.generate_rnd_person_btn.width() / 2), 300
        )
        self.generate_rnd_person_btn.clicked.connect(self.generate_rnd_person)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def generate_rnd_person(self):
        sex = random.choice(sexes)

        if sex == "male":
            name = [random.choice(first_names["male"]), random.choice(last_names)]
            if name[0].find(";") != -1:
                name[0] = random.choice(name[0].split(";"))
        else:
            name = [random.choice(first_names["female"]), random.choice(last_names)]
            if name[0].find(";") != -1:
                name[0] = random.choice(name[0].split(";"))

        age = random.randint(1, 120)

        special_job = True if random.randint(1, 10) == 1 else False
        if special_job:
            occupation_name = rnd_from_dict(occupations["special"])
            if sex == "female":
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
            if sex == "female":
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

        good_traits = deepcopy(traits["good"])
        bad_traits = deepcopy(traits["bad"])
        opposite_traits = deepcopy(traits["opposite"])

        trait_num = random.randint(1, 5)
        good_trait_num = random.randint(1, trait_num)
        bad_trait_num = trait_num - good_trait_num

        # assign traits
        traits_dict = {"good": [], "bad": []}
        for i in range(good_trait_num):
            try:
                trait = random.choice(good_traits)
                traits_dict["good"].append(trait)
                idx = good_traits.index(trait)
                good_traits.pop(idx)
            except IndexError:
                pass

        for trait in traits_dict["good"]:
            if opposite_traits.get(trait):
                try:
                    bad_traits.pop(bad_traits.index(opposite_traits[trait]))
                except ValueError:
                    pass

        for i in range(bad_trait_num):
            try:
                trait = random.choice(bad_traits)
                traits_dict["bad"].append(trait)
                idx = bad_traits.index(trait)
                bad_traits.pop(idx)
            except IndexError:
                pass

        traits_combined = [
            trait.title() for trait in traits_dict["good"] + traits_dict["bad"]
        ]
        random.shuffle(traits_combined)

        self.person_name.setText(name[0] + " " + name[1])
        self.person_age.setText(str(age))
        self.person_sex.setText(sex)
        self.person_job.setText(occupation.title())
        self.person_religion.setText(random.choice(religions))
        self.person_traits.setText("\n".join(traits_combined))

        self.person_name.adjustSize()
        self.person_age.adjustSize()
        self.person_sex.adjustSize()
        self.person_job.adjustSize()
        self.person_religion.adjustSize()
        self.person_traits.adjustSize()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


app = QApplication([])
gui = GUI()
app.exec_()
