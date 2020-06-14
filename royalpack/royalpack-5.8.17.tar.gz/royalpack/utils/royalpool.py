import logging
from typing import Optional, List, AsyncGenerator, Tuple, Any, Dict
from royalnet.bard.discord import YtdlDiscord
from royalnet.serf.discord import Playable
import discord
import random


log = logging.getLogger(__name__)


class RoyalPool(Playable):
    """A pool of :class:`YtdlDiscord` that will be played in a loop."""
    def __init__(self, start_with: Optional[List[YtdlDiscord]] = None):
        super().__init__()
        self.full_pool: List[YtdlDiscord] = []
        self.remaining_pool: List[YtdlDiscord] = []
        self.now_playing: Optional[YtdlDiscord] = None
        if start_with is not None:
            self.full_pool = [*self.full_pool, *start_with]
        log.debug(f"Created new {self.__class__.__qualname__} containing: {self.full_pool}")

    async def _generator(self) \
            -> AsyncGenerator[Optional["discord.AudioSource"], Tuple[Tuple[Any, ...], Dict[str, Any]]]:
        yield
        while True:
            if len(self.remaining_pool) == 0:
                if len(self.full_pool) == 0:
                    log.debug(f"Nothing in the pool, yielding None...")
                    yield None
                    continue
                else:
                    self.remaining_pool = self.full_pool.copy()
                    random.shuffle(self.remaining_pool)
            log.debug(f"Dequeuing an item...")
            # Get the first YtdlDiscord of the queue
            self.now_playing: YtdlDiscord = self.remaining_pool.pop(0)
            log.debug(f"Yielding FileAudioSource from: {self.now_playing}")
            # Create a FileAudioSource from the YtdlDiscord
            # If the file hasn't been fetched / downloaded / converted yet, it will do so before yielding
            async with self.now_playing.spawn_audiosource() as fas:
                # Yield the resulting AudioSource
                yield fas

    async def destroy(self):
        for file in self.full_pool:
            log.debug(f"Deleting: {file}")
            await file.delete_asap()
            log.debug(f"Deleting: {file.ytdl_file}")
            await file.ytdl_file.delete_asap()
            log.debug(f"Deleted successfully!")
        self.full_pool = []
        self.remaining_pool = []
        self.now_playing = None
