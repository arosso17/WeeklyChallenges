import sys
from pathlib import Path

try:
    import wclib
except ImportError:
    # wclib may not be in the path because of the architecture
    # of all the challenges and the fact that there are many
    # way to run them (through the showcase, or on their own)

    ROOT_FOLDER = Path(__file__).absolute().parent.parent.parent
    sys.path.append(str(ROOT_FOLDER))
    import wclib

# This line tells python how to handle the relative imports
# when you run this file directly.
__package__ = "03-buttons." + Path(__file__).absolute().parent.name

# ---- Recommended: don't modify anything above this line ---- #

# Metadata about your submission
__author__ = "treehuggerbear1#2361"  # Put yours!
__achievements__ = [  # Uncomment the ones you've done
    "Casual",
    "Ambitious",
    # "Adventurous",
]

import pygame

# To import the modules in yourname/, you need to use relative imports,
# otherwise your project will not be compatible with the showcase.
# noinspection PyPackages
from .utils import *

BACKGROUND = 0x0F1012


# This is a suggestion of the interface of the button class.
# There are many other ways to do it, but I strongly suggest to
# at least use a class, so that it is more reusable.


class Light:
    def __init__(self, pos, color='yellow'):
        self.pos = pos
        self.on = -1
        self.color = color

    def flip(self):
        self.on *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, 'grey', self.pos, 20)
        if self.on > 0:
            pygame.draw.circle(screen, self.color, self.pos, 25)
            pygame.draw.circle(screen, "green", self.pos, 25, 3)


class Button:
    def __init__(self, position, color,  content: str, size=None, link=[None]):
        self.position = position
        self.size = size
        self.color = color
        self.content = content
        self.t = text(self.content, "red")
        if self.size is None:
            self.size = (int(self.t.get_width() + 20), int(self.t.get_height() + 20))
        self.surf = pygame.Surface([self.size[0]+20, self.size[1]+20])
        self.surf.set_colorkey('black')
        self.rect = [[10, 10], self.size]
        self.hovered = False
        self.held = False
        self.link = link
        self.click_count = 0
        self.timer = 0

    def handle_event(self, event: pygame.event.Event):
        # Use this to update the state of the button according to user inputs.
        # It is usually a good idea to have this separated from the rest according
        # to the principle of separation of concerns.
        ...
        if event.type == 1024:
            rec = [self.rect[0][0] + self.position[0], self.rect[0][1] + self.position[1]]
            if pygame.Rect([rec, self.size]).collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False
                self.held = False
        if event.type == 1025:
            rec = [self.rect[0][0] + self.position[0], self.rect[0][1] + self.position[1]]
            if pygame.Rect([rec, self.size]).collidepoint(event.pos):
                self.held = True
        if event.type == 1026:
            self.held = False
            rec = [self.rect[0][0] + self.position[0], self.rect[0][1] + self.position[1]]
            if pygame.Rect([rec, self.size]).collidepoint(event.pos):
                self.click_count += 1
                self.timer = 20

    def draw(self, screen: pygame.Surface):
        if self.click_count > 0:
            self.timer -= 1
        if self.timer == 1:
            if self.click_count <= len(self.link):
                if self.link[self.click_count - 1]:
                    if type(self.link[self.click_count - 1]) == list:
                        for i in self.link[self.click_count - 1]:
                            i.flip()
                    else:
                        self.link[self.click_count-1].flip()
            self.click_count = 0
            self.timer = 0
        color = self.color
        rect = [self.rect[0][0], self.rect[0][1], self.rect[1][0], self.rect[1][1] - 2]
        pos = [20, 20]
        bcolor = 'white'#[color[0] * (3 / 5), color[1] * (3 / 5), color[2] * (3 / 5)]
        bbcolor = [color[0] * (4 / 5), color[1] * (4 / 5), color[2] * (4 / 5)]
        if self.hovered:
            bcolor = "blue"
        if self.held:
            color = [color[0] * (4/5), color[1] * (4/5), color[2] * (4/5)]
            # rect = [rect[0], rect[1]+2, rect[2], rect[2]-2]
            pos = [pos[0], pos[1]+2]
        pygame.draw.rect(self.surf, bcolor, [self.rect[0][0]-2, self.rect[0][1]-2, self.rect[1][0]+4, self.rect[1][1]+6], border_radius=10)
        pygame.draw.rect(self.surf, bbcolor, [rect[0], rect[1]+4, rect[2], rect[3]], border_radius=10)
        pygame.draw.rect(self.surf, color, rect, border_radius=10)
        self.surf.blit(self.t, pos)
        screen.blit(self.surf, self.position)


def mainloop():
    pygame.init()
    links = [Light([300, 40]), Light([300, 100], 'purple'), Light([350, 40], 'orange'), Light([350, 100], 'blue'), Light([400, 40], "red"), Light([400, 100], 'cyan')]
    buttons = [
        Button((20, 20), (240, 172, 34), "I do things...", link=[links[0], links[2], links[4]]),
        Button((20, 75), (240, 172, 34), "I do things too...", link=[links[1], links[3], links[5]]),
        Button((20, 130), (240, 172, 34), "I do other things...", link=[links])
    ]

    clock = pygame.time.Clock()
    while True:
        screen, events = yield
        for event in events:
            if event.type == pygame.QUIT:
                return

            for button in buttons:
                button.handle_event(event)

        screen.fill(BACKGROUND)
        for link in links:
            link.draw(screen)
        for button in buttons:
            button.draw(screen)

        clock.tick(60)


if __name__ == "__main__":
    wclib.run(mainloop())
