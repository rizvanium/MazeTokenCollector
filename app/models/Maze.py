import enum


class MazeItems(enum.Enum):
    PATH = 0
    WALL = -1
    TOKEN_COMMON = 1
    TOKEN_RARE = 2
    TOKEN_UNIQUE = 5
    TOKEN_LEGENDARY = 10
