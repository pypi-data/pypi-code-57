def read_selection(options, message):
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter, Completer, Completion
    from prompt_toolkit.shortcuts import CompleteStyle

    opts_list = list(options)

    completer = WordCompleter(opts_list)
    while True:
        result = prompt(f"{message} (Tab to autocomplete): \n> ",
                        completer=completer,
                        complete_style=CompleteStyle.MULTI_COLUMN,
                        complete_while_typing=True)
        if result not in opts_list:
            print("Selection not recognized. Please select from the given options.")
        else:
            break
    return {
        "selection": result
    }
