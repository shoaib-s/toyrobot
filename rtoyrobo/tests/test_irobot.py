import io

from rtoyrobo.toyrobot.robot import Direction
from rtoyrobo.toyrobot.robot import IressRobot
from rtoyrobo.toyrobot.robot import Position
from rtoyrobo.toyrobot.robot import run_command

test_cases = {
    'LEFT': {
        'input':['PLACE 0,1,NORTH', 'LEFT', 'REPORT'],
        'output':"X=0,Y=1,Facing=WEST"
    },
    'RIGHT': {
        'input': ['PLACE 0,1,NORTH', 'RIGHT', 'REPORT'],
        'output': "X=0,Y=1,Facing=EAST"
    },
    'MOVE': {
        'input': ['PLACE 0,1,NORTH', 'MOVE', 'REPORT'],
        'output': "X=0,Y=2,Facing=NORTH"
    },
    'corner_case_1': {
        'input': ['PLACE 0,5,NORTH', 'MOVE', 'REPORT' ],
        'output': "X=0,Y=5,Facing=NORTH"
    },
    'corner_case_2': {
        'input': ['PLACE 0,1,NORTH', 'LEFT', 'MOVE', 'REPORT' ],
        'output': "X=0,Y=1,Facing=WEST"
    },
    'corner_case_3': {
        'input': ['PLACE 1,0,SOUTH', 'MOVE', 'MOVE', 'REPORT' ],
        'output': "X=1,Y=0,Facing=SOUTH"
    },
    'corner_case_4': {
        'input': ['PLACE 5,0,EAST', 'MOVE', 'REPORT'],
        'output': "X=5,Y=0,Facing=EAST"
    },
    'move_to_center':{
        'input': ['PLACE 0,1,NORTH', 'RIGHT', 'MOVE', 'MOVE', 'LEFT', 'MOVE', 'REPORT' ],
        'output': "X=2,Y=2,Facing=NORTH"
    },
    'test_parser': {
        'input':['MMOVE'],
        'output':"""Invalid command passed.
          Please use one of the following commands: 
          PLACE X,Y,(NORTH|SOUTH|EAST|WEST)
          MOVE
          LEFT
          RIGHT"""
    },

}

def execute_test(test):
    op_file = io.StringIO()
    cmds = "\n".join(test['input'])
    input_file = io.StringIO(cmds)
    expected_res = test['output']
    robot = IressRobot()
    run_command(robot, input_file, op_file)
    x = op_file.getvalue()
    assert expected_res == x.strip()

def test_invalid_positions():
    robot = IressRobot()
    pos = Position(2, 2)
    robot.place(pos, Direction['EAST'])
    res= robot.report()
    assert res == "X=2,Y=2,Facing=EAST"

def test_leftturn():
    tc_l = test_cases['LEFT']
    execute_test(tc_l)

def test_rightturn():
    tc_r = test_cases['RIGHT']
    execute_test(tc_r)

def test_move():
    tc_m= test_cases['MOVE']
    execute_test(tc_m)

def test_corner_case_1():
    tc_m= test_cases['corner_case_1']
    execute_test(tc_m)

def test_corner_case_2():
    tc_m = test_cases['corner_case_2']
    execute_test(tc_m)

def test_corner_case_3():
    tc_m = test_cases['corner_case_3']
    execute_test(tc_m)

def test_corner_case_4():
    tc_m = test_cases['corner_case_4']
    execute_test(tc_m)

def test_move_to_center():
    tc_m= test_cases['move_to_center']
    execute_test(tc_m)

def test_parser():
    tc_m = test_cases['test_parser']
    execute_test(tc_m)



