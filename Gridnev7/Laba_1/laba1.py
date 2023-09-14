import os
import json
import re

from word4univer.Word.rels import Image
from word4univer import (
    Lab,
    LabInfo,
    SubjectInfo,
    FullName,
    StudentInfo,
    TitlePages,
    Path,
)


def get_file(path: str = "") -> str:
    return os.path.join(os.path.dirname(__file__), path)


class Laba1(Lab):
    info = LabInfo(
        name="Лабораторная работа",
        index=1,
        theme="Исследование моделей открытых сообщений",
        subject=SubjectInfo(
            name="Криптографические методы защиты информации",
            teacher=FullName("Гриднев", "Виктор", "Алексеевич"),
        ),
    )

    def __init__(self, input_filename: str, student: StudentInfo, **params):
        super().__init__(
            self.info,
            student,
            parts_folder=get_file("docparts"),
            style=Path.get_src("styles/tstu.xml"),
            **params
        )

        with open(get_file(get_file("config.json")), "r", encoding="UTF-8") as conf_f:
            self.config = json.load(conf_f)

        self.lines = []
        with open("input.txt", "r", encoding="UTF-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "").replace("\r", "").strip()
                line = re.sub(r" +", " ", line)
                self.lines.append(line)

        self.text = self.process_text(self.lines)
        self.letters_count = self.all_letters_count(self.text)

        vowel = self.config["letters"]["vowel"]
        consonant = self.config["letters"]["consonant"]

        self.all_freq = dict(
            sorted(self.count_all_letters(self.text, vowel + consonant).items())
        )

        vowel_vowel = self.get_combinations(vowel, vowel)
        vowel_consonant = self.get_combinations(vowel, consonant)
        consonant_vowel = self.get_combinations(consonant, vowel)
        consonant_consonant = self.get_combinations(consonant, consonant)

        self.vv_count = {
            k: v
            for k, v in sorted(
                self.count_all_letters(self.text, vowel_vowel).items(),
                key=lambda k: k[1],
                reverse=True,
            )
            if v > 0
        }
        self.vc_count = {
            k: v
            for k, v in sorted(
                self.count_all_letters(self.text, vowel_consonant).items(),
                key=lambda k: k[1],
                reverse=True,
            )
            if v > 0
        }
        self.cv_count = {
            k: v
            for k, v in sorted(
                self.count_all_letters(self.text, consonant_vowel).items(),
                key=lambda k: k[1],
                reverse=True,
            )
            if v > 0
        }
        self.cc_count = {
            k: v
            for k, v in sorted(
                self.count_all_letters(self.text, consonant_consonant).items(),
                key=lambda k: k[1],
                reverse=True,
            )
            if v > 0
        }

        top_letters = [
            k
            for k, v in sorted(self.all_freq.items(), key=lambda k: k[1], reverse=True)
            if v > 0
        ]
        self.top_letters = top_letters[
            : min(self.config["max_top_letters"], len(top_letters))
        ]
        self.missing_letters = [k for k, v in self.all_freq.items() if v == 0]

    def run(self):
        TitlePages.tstu(self.document)

        diagram_style = {"width": 266, "height": 230}
        diagram_img = Image(Path.get_path(get_file("diagram.png")), style=diagram_style)
        diagram_img.id = self.document.add_relation(diagram_img)

        context = {
            "text_name": "какой-то текст который мне скинул Ванёк",
            "text": self.lines,
            "top_letters": self.top_letters,
            "missing_letters": self.missing_letters,
            "letters_count": self.letters_count,
            "vv_count": sum(self.vv_count.values()),
            "vc_count": len(self.vc_count.values()),
            "cv_count": len(self.cv_count.values()),
            "cc_count": len(self.cc_count.values()),
            "diagram": diagram_img,
            "table_1": self.get_ltrs_freq_table(self.all_freq, self.letters_count),
            "table_2": self.get_bigrams_table(self.vv_count),
            "table_3": self.get_bigrams_table(self.vc_count),
            "table_4": self.get_bigrams_table(self.cv_count),
            "table_5": self.get_bigrams_table(self.cc_count),
        }

        self.document.add_step("main", **context)

    def process_text(self, lines: list[str]) -> str:
        text = re.sub(
            re.compile(self.config["patterns"]["sp"]), " ", " ".join(lines).lower()
        )
        return re.sub(r" +", " ", text)

    def all_letters_count(self, text: str) -> int:
        all_letters = re.sub(re.compile(self.config["patterns"]["no_sp"]), "", text)
        return len(all_letters)

    def count_all_letters(self, text: str, letters: list[str]) -> dict[str, int]:
        count = {}
        for letter in letters:
            count[letter] = text.count(letter)
        return count

    def get_combinations(self, arr1: list[str], arr2: list[str]) -> list[str]:
        combinations = []
        for item1 in arr1:
            for item2 in arr2:
                combinations.append(item1 + item2)
        return combinations

    def get_ltrs_freq_table(
        self, all_freq: dict[str, int], letters_count: int
    ) -> list[list[list[str]]]:
        items = []

        freq_items = list(all_freq.items())
        half_len = len(freq_items) // 2
        for i in range(0, half_len):
            ltr, cnt = freq_items[i]
            left = [
                ltr.upper(),
                cnt,
                round((cnt / letters_count), self.config["precision"])
                if cnt > 0
                else "–",
            ]
            if i < len(freq_items):
                ltr, cnt = freq_items[half_len + i]
                right = [
                    ltr.upper(),
                    cnt,
                    round((cnt / letters_count), self.config["precision"])
                    if cnt > 0
                    else "–",
                ]
            else:
                right = ["", "", ""]
            items.append([left, right])

        return items

    def get_bigrams_table(self, bigrams_freq: dict[str, int]) -> list[list[list[str]]]:
        items = []

        freq_items = list(bigrams_freq.items())
        quad_len = len(bigrams_freq) // 4
        for i in range(0, quad_len):
            line = []
            for j in range(4):
                index = quad_len * j + i
                if index < len(freq_items):
                    line.append(list(freq_items[index]))
                else:
                    line.append(["", ""])
            items.append(line)
        return items
