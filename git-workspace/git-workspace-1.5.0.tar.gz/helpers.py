def read_selection(options, message):
    from PyInquirer import prompt
    question = {
        "type": "list",
        "name": "selection",
        "message": message,
        "choices": options
    }

    return prompt([question])