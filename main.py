import re
import json

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

    all_count = dict(sorted(count_all_letters(text, vowel + consonant).items()))
    
    vowel_vowel = get_combinations(config['letters']['vowel'], config['letters']['vowel'])
    vowel_consonant = get_combinations(config['letters']['vowel'], config['letters']['consonant'])
    consonant_vowel = get_combinations(config['letters']['consonant'], config['letters']['vowel'])
    consonant_consonant = get_combinations(config['letters']['consonant'], config['letters']['consonant'])

    vv_count = {k:v for k, v in sorted(count_all_letters(text, vowel_vowel).items(), key=lambda k: k[1], reverse=True) if v > 0}
    vc_count = {k:v for k, v in sorted(count_all_letters(text, vowel_consonant).items(), key=lambda k: k[1], reverse=True) if v > 0}
    cv_count = {k:v for k, v in sorted(count_all_letters(text, consonant_vowel).items(), key=lambda k: k[1], reverse=True) if v > 0}
    cc_count = {k:v for k, v in sorted(count_all_letters(text, consonant_consonant).items(), key=lambda k: k[1], reverse=True) if v > 0}

    print(vv_count)


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


if __name__ == "__main__":
    main()
