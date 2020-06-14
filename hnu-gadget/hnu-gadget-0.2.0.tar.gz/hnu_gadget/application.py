import webbrowser
import tkinter as tk

from . import hackernews


class Story:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def on_click_url(self):
        webbrowser.open(self.url, autoraise=True)


def windows_tk(stories):
    window = tk.Tk()

    window.rowconfigure(5, minsize=100, weight=1)
    window.columnconfigure([0], minsize=50, weight=1)
    u = 0
    for i in stories:
        story = hackernews.story(i)
        story = Story(story['title'], story['url'])
        btn = tk.Button(master=window,
                        text=f"{story.name}",
                        command=story.on_click_url)
        btn.grid(row=u, column=0)
        u += 1

    return window


def run():
    stories = hackernews.stories_id()
    window = windows_tk(stories[:4])
    window.mainloop()

#    story = hackernews.story(stories[0])
#    title = story['title']
#    url = story['url']
#    click.secho(title, fg="green")
#    click.secho(url)
