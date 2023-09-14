import re
import json

from jinja2 import Template

def main():
    f = open("input.txt", 'r', encoding="UTF-8")
    lines = []

    with open("config.json", 'r', encoding="UTF-8") as conf_f:
        config = json.load(conf_f)

    for line in f.readlines():
        line = line.replace('\n', '').replace('\r', '').strip()
        line = re.sub(r" +", ' ', line)
        lines.append(line)

    text = process_text(lines, config['patterns']['sp'])
    letters_count = all_letters_count(text, config['patterns']['no_sp'])

    vowel = config['letters']['vowel']
    consonant = config['letters']['consonant']

    all_freq = dict(sorted(count_all_letters(text, vowel + consonant).items()))
    
    vowel_vowel = get_combinations(config['letters']['vowel'], config['letters']['vowel'])
    vowel_consonant = get_combinations(config['letters']['vowel'], config['letters']['consonant'])
    consonant_vowel = get_combinations(config['letters']['consonant'], config['letters']['vowel'])
    consonant_consonant = get_combinations(config['letters']['consonant'], config['letters']['consonant'])

    vv_count = {k:v for k, v in sorted(count_all_letters(text, vowel_vowel).items(), key=lambda k: k[1], reverse=True) if v > 0}
    vc_count = {k:v for k, v in sorted(count_all_letters(text, vowel_consonant).items(), key=lambda k: k[1], reverse=True) if v > 0}
    cv_count = {k:v for k, v in sorted(count_all_letters(text, consonant_vowel).items(), key=lambda k: k[1], reverse=True) if v > 0}
    cc_count = {k:v for k, v in sorted(count_all_letters(text, consonant_consonant).items(), key=lambda k: k[1], reverse=True) if v > 0}

    # Templates

    with open("document.xml", 'r', encoding="UTF-8") as f:
        template  = Template(f.read())
    with open("out/document.xml", 'w', encoding="UTF-8") as f:
        f.write(template.render(
            student = "студент",
            group = "СИБ201",
            name ="Иванос Акышва Фыты",
            year = 2023,

            text_name = "какой-то текст который мне скинул Ванёк",
            text = lines,

            letters_count = letters_count,
            vv_count = len(vv_count),
            vc_count = len(vc_count),
            cv_count = len(cv_count),
            cc_count = len(cc_count),

            table_1 = get_ltrs_freq_table(all_freq, letters_count, config['precision']),
            
            table_2 = get_bigrams_table(vv_count),
            table_3 = get_bigrams_table(vc_count),
            table_4 = get_bigrams_table(cv_count),
            table_5 = get_bigrams_table(cc_count),
        ))


def process_text(lines: list[str], pattern: str) -> str:
    text = re.sub(re.compile(pattern), ' ', ' '.join(lines).lower())
    return re.sub(r" +", ' ', text)


def all_letters_count(text: str, pattern: str) -> int:
    all_letters = re.sub(re.compile(pattern), '', text)
    return len(all_letters)


def count_all_letters(text: str, letters: list[str]) -> dict[str, int]:
    count = {}
    for letter in letters:
        count [letter] = text.count(letter)
    return count


def get_combinations(arr1: list[str], arr2: list[str]) -> list[str]:
    combinations = []
    for item1 in arr1:
        for item2 in arr2:
            combinations.append(item1 + item2)
    return combinations


def get_ltrs_freq_table(all_freq: dict[str, int], letters_count: int, precision: int) -> list[list[list[str]]]:
    items = []
    
    freq_items = list(all_freq.items())
    half_len = len(freq_items) // 2
    for i in range(0, half_len):
        ltr, cnt = freq_items[i]
        left = [ltr.upper(), cnt, round((cnt / letters_count), precision) if cnt > 0 else "–"]
        if i < len(freq_items):
            ltr, cnt = freq_items[half_len + i]
            right = [ltr.upper(), cnt, round((cnt / letters_count), precision) if cnt > 0 else "–"]
        else:
            right = ["", "", ""]
        items.append([left, right])

    return items


def get_bigrams_table(bigrams_freq: dict[str, int]) -> list[list[list[str]]]:
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


if __name__ == "__main__":
    main()
