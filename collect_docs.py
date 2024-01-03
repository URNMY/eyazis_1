import os
import json
import string


first_path = os.getcwd()
path = first_path + "\\files"


def collect(link, name):
    os.chdir(path)
    name += ".txt"

    with open(link, "r") as read_from:
        inner_string = read_from.read()

    with open(name, "w", encoding="utf-8") as write_to:
        write_to.write(os.path.abspath(name) + "\n" + inner_string)

    with open(name, "r") as for_index:
        file_index = {}
        for index, line in enumerate(for_index):
            if index == 0:
                continue
            for word in str.translate(line, string.punctuation).split(" "):
                if word in file_index:
                    file_index[word] += 1
                else:
                    file_index[word] = 1
        with open("../index/" + name[:-4] + ".json", "w") as as_index:
            json.dump(file_index, as_index, indent=5)

    result = []
    for root, dirs, files in os.walk(path, topdown=False):
        for index, name in enumerate(files, start=1):
            result.append(f"{index}) {name.capitalize()}")
    os.chdir(first_path)
    return result


if __name__ == '__main__':
    pass
