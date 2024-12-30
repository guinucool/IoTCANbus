

# Priority levels cap
caps = [128, 1024]

# Agreed official offset
offset = 10

# Agreed pseudo random function
def prf(key: int, seed: int) -> int:
    pass

# Agreed IBN span
span = [32, 64, 128]

# Class that defines the acting agent
class Agent:

    # Constructor of the acting agent
    def __init__(self, key: int, ids: set = set()):

        # Secret IBN defining key
        self.__key__ = key

        # Random seed use for IBN generation
        self.__seed__ = None

        # Session key for the agent
        self.__session__ = None

        # Set of ids this agent is allowed to send
        self.__ids__ = ids

        # Dictionary of sequence ids for each id
        self.__seq__ = dict()

        # Index of the current IBN
        self.__index__ = 0

    # Definition of all the necessary information for the sequence
    def initialize(self, seed: int = None) -> int:
        pass

    # Refreshing of the sequence
    def refresh(self) -> None:
        pass

    # Get the current IBN and update the index
    def current(self, key: int) -> int:
        pass

    # Check if the current IBN checks out and update the index
    def check(self, key: int, ibn: int) -> bool:
        pass

    # Check if an id belongs to the agent
    def hasId(self, key: int) -> bool:
        pass

# Class that defines the acting officer
class Officer:

    # Constructor of the acting officer
    def __init__(self):
        pass