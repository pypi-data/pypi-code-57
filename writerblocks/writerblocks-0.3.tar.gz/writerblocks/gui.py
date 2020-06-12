"""Kivy-based GUI for writerblocks."""

import yaml

from argparse import Namespace
from copy import deepcopy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from typing import Optional

from writerblocks.common import options, INI_FILENAME
from writerblocks.backend import split_tags, full_path, parse_options, run


_settings_json = """[
    {
        "type": "bool",
        "title": "New project",
        "desc": "Create a new project with default contents.",
        "section": "options",
        "key": "new_project"
    },
    {
        "type": "path",
        "title": "Project directory",
        "desc": "Directory in which project files are stored.",
        "section": "options",
        "key": "base_dir"
    },
    {
        "type": "string",
        "title": "Index file",
        "desc": "Index filename to use.",
        "section": "options",
        "key": "index_file"
    },
    {
        "type": "string",
        "title": "Input format",
        "desc": "Text file format.",
        "section": "options",
        "key": "in_fmt"
    },
    {
        "type": "string",
        "title": "Output format",
        "desc": "File format to export projects to.",
        "section": "options",
        "key": "out_fmt"
    },
    {
        "type": "string",
        "title": "Output filename",
        "desc": "Output file name, including extension.",
        "section": "options",
        "key": "out_file"
    },
    {
        "type": "string",
        "title": "Tags",
        "desc": "Ignore text files that don't have these tags (comma-separated.)",
        "section": "options",
        "key": "tags"
    },
    {
        "type": "bool",
        "title": "All tags",
        "desc": "Use only files that match all specified tags.",
        "section": "options",
        "key": "all_tags"
    },
    {
        "type": "string",
        "title": "Tag blacklist",
        "desc": "Ignore text files that have these tags (comma-separated.)",
        "section": "options",
        "key": "blacklist_tags"
    },
    {
        "type": "string",
        "title": "Pandoc arguments",
        "desc": "Additional options to pass through to pandoc.",
        "section": "options",
        "key": "pandoc_args"
    }
]"""


def exit_pretty(*_):
    """Wrapper to exit() for callbacks."""
    print("Be seeing you.")
    exit(0)


class WriterBlocks(App):
    def __init__(self):
        super(WriterBlocks, self).__init__()

        opts = deepcopy(vars(options))
        self.options = Namespace(**opts)
        if isinstance(self.options.tags, list):
            self.options.tags = ','.join(self.options.tags)
        if isinstance(self.options.blacklist_tags, list):
            self.options.blacklist_tags = ','.join(self.options.blacklist_tags)
        self.title = 'WriterBlocks GUI'
        self.main = BoxLayout(orientation='vertical')
        self.buttons = BoxLayout(size_hint=(1, .1))
        self.output = Label()

    def set_opts_from_config(self) -> None:
        """Be sure options are set correctly."""
        opts = vars(self.options)
        for opt in opts:
            opts[opt] = yaml.safe_load(self.config['options'][opt])
            
    def get_application_config(self, defaultpath: Optional[str] =None):
        """Override to set the config file path to project dir."""
        return full_path(INI_FILENAME)

    def build(self) -> BoxLayout:
        def run_callback(_):
            return self.run_backend()

        run_btn = Button(text='Run')
        run_btn.bind(on_press=run_callback)
        settings_btn = Button(text='Settings')
        settings_btn.bind(on_press=self.open_settings)
        exit_btn = Button(text='Quit')
        exit_btn.bind(on_press=exit_pretty)
        self.buttons.add_widget(settings_btn)
        self.buttons.add_widget(run_btn)
        self.buttons.add_widget(exit_btn)
        self.main.add_widget(self.buttons)
        self.main.add_widget(self.output)
        return self.main

    def run_backend(self) -> None:
        self.set_opts_from_config()
        parse_options(self.options, [])
        self.main.remove_widget(self.output)
        try:
            output = run()
        except FileNotFoundError:
            output = "Error: index file {} not found.".format(options.index_file)
        self.output = Label(text=output)
        self.main.add_widget(self.output)

    def build_settings(self, settings):
        settings.add_json_panel("WriterBlocks", config=self.config, data=_settings_json)
        return settings

    def build_config(self, config):
        opts = vars(self.options)
        config.setdefaults("options", opts)

    def on_config_change(self, config, section, key, value):
        opts = vars(options)
        if key in ['tags', 'blacklist_tags']:
            opts[key] = split_tags(value)
        else:
            opts[key] = value


def main():
    """Run the GUI writerblocks tool."""
    app = WriterBlocks()
    try:
        app.run()
    except KeyboardInterrupt:
        exit_pretty()


if __name__ == '__main__':
    main()
