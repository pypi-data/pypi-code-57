from typing import *
import collections
import click
import os
from .data import from_file


@click.group()
def main():
    pass


data_folder_option = click.option("-d", "--data-folder", type=click.Path(exists=True, file_okay=False), prompt=True)

Actor = collections.namedtuple("Actor", ["id", "name"])


@main.command()
@data_folder_option
@click.option("-i", "--include-ids", default=False)
def count(data_folder, include_ids):
    data = from_file(os.path.join(data_folder, "result.json"))
    chats: List = data["chats"]["list"]

    for chat in chats:
        counts = {}
        messages = chat.get("messages", [])
        name = chat.get("name", "Unknown")

        with click.progressbar(messages, label=name) as bar:
            for message in bar:
                actor = Actor(
                    id=message.get("actor_id") or message.get("from_id"),
                    name=message.get("actor") or message.get("from")
                )
                if actor not in counts:
                    counts[actor] = 0
                counts[actor] += 1

        # Order counts
        counts_list = list(sorted(counts.items(), key=lambda item: item[1], reverse=True))

        click.echo(name)
        for actor, actor_count in counts_list:
            if include_ids:
                click.echo(f"({actor.id}) {actor.name}: {actor_count} message{'s' if actor_count != 0 else ''}")
            else:
                click.echo(f"{actor.name}: {actor_count} message{'s' if actor_count != 0 else ''}")

        click.echo()


if __name__ == "__main__":
    main()
