#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Flappy
# Copyright (C) 2014 Alan Aguiar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar alanjas@hotmail.com

import gtk
import pygame
import sys
import pygame.sprite as sprite
from floor import Floor
from pipe import Pipe_I
from pipe import Pipe_S
from background import make_back
from bird import Bird
from scores import EndScore
from scores import Message
from scores import CurrentScore

GAME_SIZE = (684, 600)
#GAME_SIZE = (1200, 700)

MIN_HEIGHT = 82 * 2 + 160
DIST = 160
PIPE_W = 91
MIN_PIPE_H = 40 + 42
MES_W = 227
MES_H = 251
PIPE_IH = 122
FLOOR_Y = 50

INIT = 0
PLAY = 1
END = 2

class Flappy():

    def __init__(self):
        self.state = INIT
        self.game_w = GAME_SIZE[0]
        self.game_h = GAME_SIZE[1]
        self.floor_y = self.game_h - FLOOR_Y
        self.best = 0
        self.bird_x = self.game_w / 3 - 50
        self.bird_y = self.game_h / 2
        self.pipe_w = PIPE_W
        self.build_y = self.floor_y - 229
        self.mes_x = (self.game_w - MES_W) / 2
        self.mes_y = (self.game_h - MES_H) / 2
        self.game_p = self.game_w - DIST - self.pipe_w
        self.max_s = self.floor_y - MIN_PIPE_H - DIST
        self.min_pipe_h = MIN_PIPE_H
        self.end_s_x = (self.game_w - 139) / 2
        self.sc_x = (self.game_w - 70) / 2

    def increment_score(self):
        self.score = self.score + 1
        self.currentS.set_score(self.score)

    def load_all(self):
        self.score = 0
        self.sprites = pygame.sprite.LayeredUpdates()
        self.tubes = pygame.sprite.LayeredUpdates()
        self.background = make_back(self)
        self.screen.blit(self.background, (0, 0))
        ########################################################################
        self.floor = Floor(0, self.floor_y, self.game_w)
        self.floor.mVel = 0
        self.bird = Bird(self, self.bird_x, self.bird_y)
        self.bird.mAcc = 0
        self.end_scores = EndScore(self.end_s_x, 200)
        self.message = Message(self.mes_x, self.mes_y)
        self.currentS = CurrentScore(self, self.sc_x, 100)
        ########################################################################
        self.sprites.add(self.floor, layer=0)
        self.sprites.add(self.bird, layer=2)
        self.sprites.add(self.message, layer=3)

    def load_game(self):
        pipe1 = Pipe_I(self, self.game_w, PIPE_IH)
        pipe2 = Pipe_S(self, self.game_w, self.floor_y - PIPE_IH - DIST)
        self.sprites.add(pipe1, layer=1)
        self.sprites.add(pipe2, layer=1)
        self.tubes.add(pipe1)
        self.tubes.add(pipe2)
        self.tubes.add(self.floor)
        self.sprites.add(self.currentS, layer=3)
        self.bird.mAcc = 5
        self.bird.count = 20
        self.floor.mVel = -5
        self.sprites.remove(self.end_scores)
        self.sprites.remove(self.message)

    def main(self):
        pygame.display.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(GAME_SIZE)
        pygame.display.set_caption('Flappy')
        self.load_all()
        self.state = INIT
        self.running = True
        while self.running:
            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == INIT:
                        self.state = PLAY
                        self.load_game()
                    elif self.state == PLAY:
                        self.bird.setVel(8)
                    elif self.state == END:
                        self.state = INIT
                        self.load_all()

            self.sprites.clear(self.screen, self.background)
            self.sprites.update()
            self.sprites.draw(self.screen)
           
            col = pygame.sprite.spritecollide(self.bird, self.tubes, False)
            if not(col == []):
                self.state = END
                self.bird.mAcc = 0
                self.bird.count = -99
                self.floor.mVel = 0
                for spr in self.tubes:
                    spr.mVel = 0
                if self.score > self.best:
                    self.best = self.score
                self.end_scores.update_scores(self.score, self.best)
                self.sprites.add(self.end_scores, layer=3)
                self.sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    g = Flappy()
    g.main()

