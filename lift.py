import time
from enum import Enum
import sys
from math import ceil, floor


class Direction(Enum):
    UP = 0
    DOWN = 1
    STATIONARY = 2


class Lift2:
    def __init__(self, number_of_floors):
        self.number_of_floors = number_of_floors
        self.current = 0
        self.direction = Direction.STATIONARY

    def current_floor(self):
        return float(self.current)

    def press_button(self, floor_number, direction):
        print('pressed', floor_number, direction)

    def tick(self):
        self.current = (self.current + 1) % self.number_of_floors

class Lift:
    def __init__(self, num_floors):
        self.num_floors = num_floors
        self.direction = Direction.UP
        self._current_floor = .0
        self._down_pushes = [0] * num_floors
        self._up_pushes = [0] * num_floors

    def current_floor(self):
        return round(self._current_floor, 1)

    def press_button(self, floor_number, direction=None):
        if direction == Direction.UP:
            self._up_pushes[floor_number] += 1
        elif direction == Direction.DOWN:
            self._down_pushes[floor_number] += 1
        else:
            self._up_pushes[floor_number] += 1
            self._down_pushes[floor_number] += 1

    def _clear(self, floor, direction):
        if direction == Direction.DOWN:
            self._down_pushes[floor] = 0
        elif direction == Direction.UP:
            self._up_pushes[floor] = 0

    def tick(self):
        """
        Update internal state of the lift to the next tick
        """
        # if any(self._up_puhes) or any(self.down_pushes):
        if self.direction == Direction.UP:
            floor_above = ceil(self.current_floor())    # factor out
            if any(self._up_pushes[floor_above:]):
                self._current_floor += 0.2     # Travel up
                if self.current_floor() == floor_above:
                    self._clear(floor_above, self.direction)
            else:
                self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            floor_below = floor(self.current_floor())
            if any(self._down_pushes[:floor_below + 1]):    # Could use [:floor_above] here
                self._current_floor -= 0.2    # Travel down
                if self.current_floor() == floor_below:
                    self._clear(floor_below, self.direction)
            else:
                self.direction = Direction.UP
        else:
            raise Exception("This should never happen")

def padding():
    for i in range(100):
        print()


def display(lift):
    for i in range(25 - int(lift.current_floor())):
        print()
    print(int(lift.current_floor()))
    for i in range(int(lift.current_floor())):
        print()


normal_floors = '0123456789'
ups = 'pqwertyuio'
downs = ';asdfghjkl'


import termios
import os
import atexit

old_settings=None

def init_anykey():
   global old_settings
   old_settings = termios.tcgetattr(sys.stdin)
   new_settings = termios.tcgetattr(sys.stdin)
   new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
   new_settings[6][termios.VMIN] = 0  # cc
   new_settings[6][termios.VTIME] = 0 # cc
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

@atexit.register
def term_anykey():
   global old_settings
   if old_settings:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def anykey():
   ch_set = []
   ch = os.read(sys.stdin.fileno(), 1)
   while ch != None and len(ch) > 0:
      ch_set.append(chr(ch[0]))
      ch = os.read(sys.stdin.fileno(), 1)
   return ch_set;



def main():
    init_anykey()
    # number_of_floors = input('How many floors in your lift: ')
    number_of_floors = 10

    lift = Lift(int(number_of_floors))

    while True:
        padding()
        display(lift)

        for pressed_floor in anykey():
            if pressed_floor in normal_floors:
                lift.press_button(int(pressed_floor), None)
            elif pressed_floor in ups:
                lift.press_button(ups.index(pressed_floor), Direction.UP)
            elif pressed_floor in downs:
                lift.press_button(downs.index(pressed_floor), Direction.DOWN)


        lift.tick()
        time.sleep(0.25)

main()
