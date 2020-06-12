"""
GMLP.game
=========
"""
from __future__ import absolute_import

import configparser
import io
import json
import os
import time


class Setup:
    """
    ``WARNING THIS FEATURE IS IN DEVELOPMENT!``
    GMLP 0.2 Setup. With Setup there are a few keywords that go with Setup.
    \nTo print the keywords type ``print(Setup.keywords)`` and it will print the keywords.

    Here's an example ->

    game = Setup(
        name='Window',
        bg=(0, 0, 0),
        width=500,
        height=600,
        objects=['snake', 'food']
    )

    parser = configparser.ConfigParser()
    parser.read("test.ini")
    parser.get('IMAGE1', 'x')
    parser.set('IMAGE1', 'x', str(100))
    with open("test.ini", 'w') as f:
        parser.write(f)

    with open("test.ini", 'r') as r:
        read = r.read()
        game.View(read)
    """
    keywords = ['height', 'width', 'bg', 'name', 'objects']

    def __init__(self, **settings):
        for i in settings:
            if 'name' in settings:
                self.name = settings["name"]
            else:
                self.name = 'Window'

            if 'bg' in settings:
                self.bg = settings['bg']
            else:
                self.bg = (0, 0, 0)

            if 'height' in settings:
                self.h = settings['height']
            else:
                self.h = 0

            if 'width' in settings:
                self.w = settings['width']
            else:
                self.w = 0

            if 'objects' in settings:
                self.objects = settings['objects']
            else:
                self.objects = None


    def View(self, imgpos=None):

        import pygame
        from pygame.locals import QUIT
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.h, self.w))
        pygame.display.set_caption(self.name)

        self.closed = False
        while not self.closed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.closed = True
                    pygame.quit()
                    quit()
            self.gameDisplay.fill(self.bg)
            if self.objects != None:
                for i in self.objects:
                    self.cfg = imgpos
                    self.config = configparser.ConfigParser()
                    self.values = self.config.read_file(io.StringIO(self.cfg))
                    self.sections = self.config.sections()
                    for j in range(len(self.sections)):
                        if self.sections[j] in f'IMAGE{j+1}':
                            self.x = json.loads(self.config.get(f"IMAGE{j+1}", "x"))
                            self.y = json.loads(self.config.get(f"IMAGE{j+1}", "y"))
                            self.image = self.config.get(f"IMAGE{j+1}", "image")
                            try:
                                self.size = json.loads(self.config.get(f"IMAGE{j+1}", "size"))
                                self.img = pygame.image.load(self.image)
                                self.img = pygame.transform.scale(self.img, tuple(self.size))
                                self.gameDisplay.blit(self.img, (self.x, self.y))
                            except Exception as e:
                                self.gameDisplay.blit(pygame.image.load(self.image), (self.x, self.y))
                                pass
                            
            pygame.display.update()
