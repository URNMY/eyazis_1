import os


FILES_DIR = "files/"
REFACTOR_QUERY_DICT = {
    "all_in": ("Выведи мне документы, в которых есть все",
               "Выдай мне документы, в которых присутствуют все",
               "Дай мне документы, содержащие все"),
    "at_least_one_in": ("Выведи мне документы, в которых есть хотя бы одно",
                        "Покажи мне документы, в которых содержатся одно или более",
                        "Выдай мне документы, которые содержат по меньшей мере одно"),
    "noone_in": ("Верни мне документы, которые не содержат всех",
                 "Выдай документы, не содержащие всех"),
}


def get_words_from_expression(query_expression):
    return set(word for word in query_expression.split("'") if word.isalpha())


def check_words_in_text(text, words):
    word_booleans = {}
    for word in words:
        word_booleans[word] = word in text
    return word_booleans


def replace_with_boolean(query_expression, words_booleans):
    for word, is_in_text in words_booleans.items():
        query_expression = query_expression.replace(f"'{word}'", str(is_in_text))
    return query_expression


def is_text_appropriate_to_query(line_generator, query_expression):
    words_in_query_expression = get_words_from_expression(query_expression)
    previous_line_appearance = dict.fromkeys(words_in_query_expression, False)
    for line in line_generator:
        current_line_appearance = check_words_in_text(line, words_in_query_expression)
        previous_line_appearance = {key: max(value, current_line_appearance[key])
                                    for key, value in previous_line_appearance.items()}
    return eval(replace_with_boolean(query_expression, previous_line_appearance)), previous_line_appearance


def refactor_query(query_expression):
    if any(query_expression.startswith(sentence) for sentence in REFACTOR_QUERY_DICT["all_in"]):
        query_expression = query_expression[query_expression.index(":") + 1::].replace(" ", "")
        words = [f"'{item}'" for item in query_expression.split(",")]
        query_expression = " and ".join(words)
    elif any(query_expression.startswith(sentence) for sentence in REFACTOR_QUERY_DICT["at_least_one_in"]):
        query_expression = query_expression[query_expression.index(":") + 1::].replace(" ", "")
        words = [f"'{item}'" for item in query_expression.split(",")]
        query_expression = " or ".join(words)
    elif any(query_expression.startswith(sentence) for sentence in REFACTOR_QUERY_DICT["noone_in"]):
        query_expression = query_expression[query_expression.index(":") + 1::].replace(" ", "")
        words = [f"(not '{item}')" for item in query_expression.split(",")]
        query_expression = " and ".join(words)
    return query_expression


def search(query_expression):
    query_expression = refactor_query(query_expression)
    appropriate_file_descriptions = []
    for filename in os.listdir(FILES_DIR):
        with open(FILES_DIR + filename, "r") as file:
            line_generator = file.readlines()
        file_result = is_text_appropriate_to_query(line_generator, query_expression)
        if file_result[0]:
            appropriate_file_descriptions.append(
                (
                    os.path.abspath(FILES_DIR) + "\\" + filename,
                    file_result[1],
                    filename
                )
            )
    return appropriate_file_descriptions


if __name__ == "__main__":
    pass
