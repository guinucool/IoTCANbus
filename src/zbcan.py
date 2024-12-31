from random import randint
from math import log2

# Priority levels cap
caps = [128, 1024]

# Agreed official offset
offset = 284935

# Agreed IBN span
span = [0, 32, 64, 128]

# Agreed pseudo random function
def prf(key: int, seed: int) -> int:
    
    # Mix the two integers
    mixed = (key * 0x5DEECE66D + seed) & 0xFFFFFFFFFFFF

    # Generate the new integer
    return (mixed ^ (mixed >> 16))

# Get id priority level
def getPriority(id: int) -> int:

    # Get the legnth of the priority caps
    length = len(caps)

    # Decise the priority level
    for i in range(0, length):

        # Check if id is in this priority level
        if id < caps[i]:
            return i
        
    # If no priority was found, return lowest priority
    return length

# Extract the desired bits from an integer
def extractBits(number: int, bits: int, index: int) -> int:

    # Shift the desired number to the desired index
    shift = number >> index

    # Mask to extract only the desired bits
    mask = (1 << bits) - 1

    # Return the desired number
    return shift & mask

# Exception that sinalizes a missing id on the officer
class NoAgentForGivenId(Exception):
    pass

# Exception that sinalizes a already initialized agent
class AgentAlreadyInitialized(Exception):
    pass

# Exception that sinalizes an id not present in an agent
class NoIdInAgent(Exception):
    pass

# Class that defines the acting agent
class Agent:

    # Constructor of the acting agent
    def __init__(self, key: int, ids: set):

        # Secret IBN defining key
        self.__key = key

        # Random seed use for IBN generation
        self.__seed = None

        # Session key for the agent
        self.__session = None

        # Set of ids this agent is allowed to send
        self.__ids = ids

        # Dictionary of sequence ids for each id
        self.__seq = dict()

        # Index of the current IBN
        self.__index = dict()

    # Definition of all the necessary information for the sequence
    def initialize(self, seed: int = None) -> int:

        # Check if the agent is already not initialized
        if self.__seed is not None:
            raise AgentAlreadyInitialized()
        
        # Check if the seed was given for initialization
        if seed is None:
            seed = randint(0, 2147483647)

        # Associate the seed with the property
        self.__seed = seed

        # Generate the session key
        self.__session = prf(self.__key, self.__seed)

        # Counter of ids
        i = 1

        # Populate the dictionary with the sequences
        for id in self.__ids:

            # Create the seed for every id
            self.__seq[id] = prf(self.__session, self.__seed + (i * offset))

            # Increase the counter of ids
            i += 1

            # Create the index of the id
            self.__index[id] = 0

        # Return the used seed
        return self.__seed

    # Refreshing of the sequence
    def __refresh(self, id: int) -> None:

        # Create the seed for the specified id
        self.__seq[id] = prf(self.__session, self.__seq[id])
        
        # Reset the index for the specified id
        self.__index[id] = 0

    # Update the index
    def __upIndex(self, id: int) -> None:
        
        # Check if index has reached maximum value
        if self.__index[id] == 32:
            self.__refresh(id)

        # If not, increase by one
        else:
            self.__index[id] += 1

    # Get the current IBN
    def __getCurrent(self, id: int) -> int:
        
        # Get the priority level of the id
        priority = getPriority(id)

        # Check the span of the priority
        prioSpan = span[priority + 1] - span[priority]

        # Get the extract for the calculation of the sequence
        extract = extractBits(self.__seq[id], int(log2(prioSpan)), self.__index[id])

        # Calculate the desired IBN
        return span[priority] + extract

    # Get the current IBN and update the index
    def current(self, id: int) -> int:

        # Check for existence of the asked id
        if not self.hasId(id):
            raise NoIdInAgent()
        
        # Calculate the current IBN
        ibn = self.__getCurrent(id)

        # Increase the index
        self.__upIndex(id)

        # Return the IBN
        return ibn

    # Check if the current IBN checks out and update the index
    def check(self, id: int, ibn: int) -> bool:

        # Check for existence of the asked id
        if not self.hasId(id):
            raise NoIdInAgent()
        
        # Get the current IBN
        current = self.__getCurrent(id)
        
        # Check if the IBN does not check out (because of the ms, it may happen a delay)
        if ibn != current and ibn != current + 1:
            return False
        
        # Update the index in case it does
        self.__upIndex(id)

        # Return true in positive case
        return True

    # Check if an id belongs to the agent
    def hasId(self, id: int) -> bool:
        return (id in self.__ids)

# Class that defines the acting officer
class Officer:

    # Constructor of the acting officer
    def __init__(self, agents: list):

        # List of agents known to the acting officer
        self.__agents = agents

    # Get agent of given id or none in case of none existence
    def __getAgent(self, id: int) -> Agent | None:

        # Check which agent has the requested id
        for ag in self.__agents:

            # Check if the agent has the request id
            if ag.hasId(id):
                return ag
            
        # In case there is no agent with the given id
        return None

    # Initialization of an agent of the list
    def initialize(self, id: int, seed: int) -> None:

        # Get the agent associated to the id
        ag = self.__getAgent(id)

        # Check if it exists
        if ag is None:
            raise NoAgentForGivenId()
        
        # Initialization of the agent
        ag.initialize(seed)
    
    # Check if the received id checks out with the correspondent IBN
    def check(self, id: int, ibn: int) -> bool:

        # Get the agent for the given id
        ag = self.__getAgent(id)

        # Check if the id is associated to any agent
        if ag is None:
            return False
        
        # Check if the IBN checks out
        return ag.check(id, ibn)
    
# Emulator of a global clock for the whole channel
class Clock:

    # Constructor of the clock
    def __init__(self):
        
        # Define the current timer
        self.__time = 0

    # Increase the timer of the clock
    def tick(self):

        # Increase timer
        self.__time += 1

        # Check if the limit is reached
        self.__time = self.__time % span[-1]

    # Get the current timer
    def time(self):
        return self.__time
    
    # Reset the timer
    def reset(self):
        self.__time = 0

