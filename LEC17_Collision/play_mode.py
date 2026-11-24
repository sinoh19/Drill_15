import random
import os
import sys

from pico2d import *

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Labs.LEC17_Collision.zombie import Zombie
from ball import Ball
import game_world
import game_framework
from boy import Boy
from grass import Grass
from zombie import Zombie

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    balls = [Ball(random.randint(100, 1600-100), 60, 0) for _ in range(30)]
    for ball in balls:
        game_world.add_oject(ball, 1)

    game_world.add_collision_pair('grass:ball', grass, None)
    game_world.add_collision_pair('boy:ball', boy, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)
        game_world.add_collision_pair('ball:zombie', ball, None)

    zombies = [Zombie() for _ in range(4)]
    game_world.add_collision_pair('boy:zombie', boy, None)
    for zombie in zombies:
        game_world.add_oject(zombie, 1)
        game_world.add_collision_pair('boy:zombie', None, zombie)

def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()
    game_world.handle_collisions()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()






