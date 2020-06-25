import requests
import pyperclip
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from unicode_write.utils import UnicodeWriter


class RemoteUnicodeWriter(UnicodeWriter):
    def __init__(self, url):
        self.url = url

    def __call__(self, string):
        return requests.post(f"{self.url}/unicode", json={"codepoint": string}).json()["unicode"]


class RemoteSearchCompleter(Completer):
    def __init__(self, url: str):
        self.url = url

    def get_completions(self, document, complete_event):
        if complete_event.completion_requested:
            for match in requests.post(f"{self.url}/search", json={"query": document.text}).json():
                yield Completion(match.ljust(document.cursor_position), start_position=-document.cursor_position)


def main():
    url = "http://localhost:5000"
    writer = RemoteUnicodeWriter(url)
    text = prompt("> ", completer=RemoteSearchCompleter(url), complete_while_typing=False)
    print(writer(text))
    pyperclip.copy(writer(text))


if __name__ == "__main__":
    main()
