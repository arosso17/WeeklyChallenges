from random import uniform
import random
import pygame


class Particle:
    PARTICLES = []
    DEL = []

    def __init__(self, pos, color, size, shape="circle", vel=False):
        if vel and shape == "fire":
            velx, vely = vel
            velx *= -0.8
            vely *= -0.8
            fac = 4 * (305 - color[1]) / 250
            vel = [velx + uniform(-fac, fac), vely + uniform(-fac, fac)]
        # elif vel:
        #     velx, vely = vel
        if not vel:
            vel = [uniform(-7, 7), uniform(-7, 7)]
        self.shape = shape
        self.pos = pos
        self.color = color
        self.size = uniform(1, size)
        if self.size > 70:
            self.size = 70
        self.vel = vel
        if self.shape == "fire":
            self.a = self.size/4
        if self.shape == "fragment":
            self.a = random.randint(0, int(self.size))
            self.b = random.randint(0, int(self.size))
            self.c = random.randint(0, int(self.size))
            self.d = random.randint(0, int(self.size))
        Particle.PARTICLES.append(self)

    def logic(self):
        # self.pos = [x + y for x, y in zip(self.pos, self.vel)]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.shape == "fire":
            self.a *= 0.97
            self.size *= 0.9
        self.size *= 0.9
        if self.shape == "fragment":
            self.a *= 0.98
            self.b *= 0.98
            self.c *= 0.98
            self.d *= 0.98
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98
        if self.size <= 0.0005:
            Particle.DEL.append(self)

    def draw(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, self.pos, self.size)
        if self.shape == "fire":
            pygame.draw.circle(screen, self.color, self.pos, self.a)
        if self.shape == "fragment":
            pygame.draw.polygon(screen, self.color, (self.pos, [self.pos[0] + self.a, self.pos[1]], [self.pos[0] + self.b, self.pos[1] + self.c], [self.pos[0], self.pos[1] + self.d]))
