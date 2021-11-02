"""
Define robot functionality
"""
from abc import ABC, abstractmethod
from enum import Enum, unique

import shlex
import re
import sys

from rtoyrobo.toyrobot import config

@unique
class Direction(Enum):
    """
    Enum for directions.
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

ROBO_MOVE_1_UNIT = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0)
}

class Position:
    """To maintain position of a robot."""
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, x_y_move: list) -> "Position":
        x: int = self.x + x_y_move[0]
        y: int = self.y + x_y_move[1]
        return Position(x, y)

    def is_on_table(self) -> bool:
        """Validate if robot is on the table.

        :return:
        boolean: to determine if it's on the table or not.
        """
        return 0 <= self.x <= config.SIZE_TABLE_X and 0 <= self.y <= config.SIZE_TABLE_Y

class MoveRobot(ABC):
    """Interface to move robot"""
    @abstractmethod
    def move(self):
        pass

class MoveOneUnit(MoveRobot):
    """Move robot by one unit"""
    def __init__(self, robot):
        self.robot = robot

    def move(self) -> None:
        res_pos = self.robot.pos.__add__(ROBO_MOVE_1_UNIT[self.robot.direction])
        if res_pos.is_on_table():
            self.robot.pos = res_pos
        else:
            print("Robot can't be moved in {} direction.".format(self.robot.direction.name))


class TurnRobo(ABC):
    """
    Interface to turn robot
    """
    @abstractmethod
    def turn(self) -> None:
        pass

class Left(TurnRobo):
    """
    Implement Left turn
    """
    def __init__(self, robot):
        self.robot = robot

    def turn(self) -> None:
        self.robot.direction = Direction((self.robot.direction.value - 1)  % len(Direction))


class Right(TurnRobo):
    """
    Implement Right turn
    """
    def __init__(self, robot):
        self.robot = robot

    def turn(self) -> None:
        self.robot.direction = Direction((self.robot.direction.value + 1) % len(Direction))

class Robot:
    """
    Base Robot class.
    """
    def __init__(self):
        self.direction: Direction
        self.pos: Position

    @abstractmethod
    def place(self, pos: Position, direction: Direction) -> None:
        pass

    def perform_turn(self, turn_robo: TurnRobo) -> None:
        turn_robo.turn()

    def move(self, move_robo: MoveRobot) -> None:
        move_robo.move()

    def report(self, output_file=sys.stdout) -> str:
        res: str = f"X={self.pos.x},Y={self.pos.y},Facing={self.direction.name}"
        print(res, file=output_file)
        return res


class IressRobot(Robot):
    """
    Iress robot
    """
    def __init__(self):
        super().__init__()
        self.direction: Direction = Direction.NORTH  # default.
        self.pos: Position = Position(0, 0)

    def __str__(self):
        return f"X={self.pos.x},Y={self.pos.y},Facing={self.direction.name}"
        # .format(self.pos.x, self.pos.y, self.direction.name))

    def place(self, pos: Position, direction: Direction) -> None:
        if pos.is_on_table():
            self.direction = direction
            self.pos = pos
        else:
            print("Invalid position. Max allowed position is 5X5")


def usage(output_file) -> None:
    print("""\nInvalid command passed.
          Please use one of the following commands: 
          PLACE X,Y,(NORTH|SOUTH|EAST|WEST)
          MOVE
          LEFT
          RIGHT""", file=output_file)


def run_command(robot, input_file=sys.stdin, output_file=sys.stdout) -> None:
    first_entry = True
    reg_ex = re.compile(r'(\d+),(\d+),(NORTH$|SOUTH$|EAST$|WEST$)')

    for l in input_file:
        cmd, *arguments = shlex.split(l.strip())
        if cmd != 'PLACE' and first_entry:
            sys.exit()
        first_entry = False

        if cmd == 'PLACE' and arguments:
            match = reg_ex.match(*arguments)
            if match:
                x, y, direction = match.groups()
                pos = Position(int(x), int(y))
                robot.place(pos, Direction[direction.upper()])
            else:
                usage(output_file)
        elif cmd == 'MOVE':
            robot.move(MoveOneUnit(robot))
        elif cmd == 'LEFT':
            robot.perform_turn(Left(robot))
        elif cmd == 'RIGHT':
            robot.perform_turn(Right(robot))
        elif cmd == 'REPORT':
            robot.report(output_file)
        elif cmd == 'EXIT':
            sys.exit()
        else:
            usage(output_file)

def main():
    robot = IressRobot()
    run_command(robot)

if __name__ == '__main__':
    main()

