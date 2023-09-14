from word4univer import StudentInfo

import Gridnev7


def main():
    laba = Gridnev7.Laba1("input.txt", StudentInfo("Иванос Акышва Фыты", "СИБ201", 1))
    laba.run()
    laba.save_to_file()


if __name__ == "__main__":
    main()
