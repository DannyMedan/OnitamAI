
FREEPIK = '<a href="https://www.freepik.com/vectors/background">' \
          'Background vector created by rawpixel.com - www.freepik.com</a>'

# Visualization data
BOARD_WIDTH = BOARD_HEIGHT = 325
DIMENSION = 5
SQ_SIZE = BOARD_HEIGHT // DIMENSION
BORDER_TOP_BOTTOM = int(3 * SQ_SIZE)
BORDER_SIDES = int(2.5 * SQ_SIZE)
TOTAL_WIDTH = BORDER_SIDES * 2 + BOARD_WIDTH
TOTAL_HEIGHT = BORDER_TOP_BOTTOM * 2 + BOARD_HEIGHT
MAX_FPS = 15
BACKGROUND = 'background'

CARD_WIDTH = 3 * SQ_SIZE
CARD_HEIGHT = 2 * SQ_SIZE
CARD_LOCATIONS = {
    "UPPER_LEFT": (0.5*SQ_SIZE, SQ_SIZE),
    "UPPER_RIGHT": (0.5*SQ_SIZE, 0.5*TOTAL_WIDTH + SQ_SIZE),
    "LOWER_LEFT": (BORDER_TOP_BOTTOM + BOARD_HEIGHT + 0.5*SQ_SIZE, SQ_SIZE),
    "LOWER_RIGHT": (BORDER_TOP_BOTTOM + BOARD_HEIGHT + 0.5*SQ_SIZE, 0.5*TOTAL_WIDTH + SQ_SIZE),
    "SIDE": (BORDER_TOP_BOTTOM + SQ_SIZE, BORDER_SIDES + BOARD_WIDTH + 0.25*SQ_SIZE)
}

# Color coding
BOARD_LIGHT = '#faedcd'
BOARD_DARK = '#d4a373'
BOARD_HIGHLIGHT_LIGHT = '#9ECE9A'
BOARD_HIGHLIGHT_DARK = '#61AF5A'
BOARD_RED = '#bb3e03'
BOARD_BLUE = '#0A9396'
BLUE_CARD_BG = "#86BBD8"
RED_CARD_BG = '#9E2B25'
BLACK = '#070707'

IMAGES = {}


# Board is 5x5 2d list, for each value:
#   first char represents color
#   second char represents role
#   '--' represents empty space

EMPTY = '--'
BLUE_PUPIL = 'BP'
BLUE_SENSEI = 'BS'
RED_PUPIL = 'RP'
RED_SENSEI = 'RS'

BLUE = "B"
RED = "R"
BLUE_DOJO = (4, 2)
RED_DOJO = (0, 2)

STARTING_BOARD = [
    [RED_PUPIL, RED_PUPIL, RED_SENSEI, RED_PUPIL, RED_PUPIL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [BLUE_PUPIL, BLUE_PUPIL, BLUE_SENSEI, BLUE_PUPIL, BLUE_PUPIL]
]

"""
For each card, the available move-set is a (row, col) relative to the position.
Meaning (x, y) means moving x rows (UP/DOWN) and y cols (LEFT/RIGHT)  
"""
CARDS = {
    'BOAR': {
        'MOVES': [(-1, 0), (0, -1), (0, 1)],
        'IMAGE_PATH': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'COBRA': {
        'MOVES': [(-1, 1), (0, -1), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'CRAB': {
        'MOVES': [(-1, 0), (0, -2), (0, 2)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'CRANE': {
        'MOVES': [(-1, 0), (1, -1), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'DRAGON': {
        'MOVES': [(-1, -2), (-1, 2), (1, -1), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'EEL': {
        'MOVES': [(-1, -1), (0, 1), (1, -1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'ELEPHANT': {
        'MOVES': [(-1, -1), (-1, 1), (0, -1), (0, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'FROG': {
        'MOVES': [(-1, -1), (0, -2), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'GOOSE': {
        'MOVES': [(-1, -1), (0, -1), (0, 1), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'HORSE': {
        'MOVES': [(-1, 0), (0, -1), (1, 0)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'MANTIS': {
        'MOVES': [(-1, -1), (-1, 1), (1, 0)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'MONKEY': {
        'MOVES': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'OX': {
        'MOVES': [(-1, 0), (0, 1), (1, 0)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'RABBIT': {
        'MOVES': [(-1, 1), (0, 2), (1, -1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    },
    'ROOSTER': {
        'MOVES': [(-1, 1), (0, -1), (0, 1), (1, -1)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': RED
    },
    'TIGER': {
        'MOVES': [(-2, 0), (1, 0)],
        'IMAGE': '',
        'QUOTE': 'Lorem ipsum dolor sit amet',
        'COLOR': BLUE
    }
}
