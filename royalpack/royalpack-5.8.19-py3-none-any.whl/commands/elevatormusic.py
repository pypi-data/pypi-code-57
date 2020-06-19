from typing import *
import random
import royalnet.commands as rc

from .play import PlayCommand


class ElevatormusicCommand(PlayCommand):
    name: str = "elevatormusic"

    aliases = ["elevator", "em"]

    description: str = "Aggiungi un po' di musica da ascensore alla chat vocale."

    syntax = "[indice]"

    _pool = [
        "https://www.youtube.com/watch?v=_tAcIGhh5Yo",
        "https://www.youtube.com/watch?v=xy_NKN75Jhw",
        "https://www.youtube.com/watch?v=PLRrL9OsAF8",
        "https://www.youtube.com/watch?v=0TmoYBcLul8",
        "https://www.youtube.com/watch?v=9v9-Nw4nAZg",
        "https://www.youtube.com/watch?v=VBlFHuCzPgY",
        "https://www.youtube.com/watch?v=mD3v1B_aXw0",
        "https://www.youtube.com/watch?v=RCSbmSmyAcY",
        "https://www.youtube.com/watch?v=kbdtBLD8Lbg",
        "https://www.youtube.com/watch?v=JjT0p2z4hGg",
        "https://www.youtube.com/watch?v=cc_KpOufpgM",
        "https://www.youtube.com/watch?v=dlNEUYBt7Ls",
        "https://www.youtube.com/watch?v=YVWdQGuE0-E",
        "https://www.youtube.com/watch?v=1nVAg8VujGA",
        "https://www.youtube.com/watch?v=G4mshu6BUio",
        "https://www.youtube.com/watch?v=Y6_Aij3n8hk",
        "https://www.youtube.com/watch?v=SbIaYZEUF1M",
        "https://www.youtube.com/watch?v=Nf8FCLT8S6A",
    ]

    async def get_urls(self, args):
        index = args.optional(0)
        if index is not None:
            try:
                return [self._pool[int(index)]]
            except ValueError:
                raise rc.InvalidInputError("L'indice deve essere un numero.\n"
                                           f"Gli indici delle canzoni iniziano a [c]0[/c] e finiscono a"
                                           f" [c]{len(self._pool) - 1}[/c].")
            except IndexError:
                raise rc.InvalidInputError(f"Indice non valido.\n"
                                           f"Gli indici delle canzoni iniziano a [c]0[/c] e finiscono a"
                                           f" [c]{len(self._pool) - 1}[/c].")
        else:
            return [random.sample(self._pool, 1)[0]]
