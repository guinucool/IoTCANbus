from time import time
from zbcan import Agent, Officer, AgentAlreadyInitialized, NoAgentForGivenId
from can.exceptions import CanOperationError
from can.interface import Bus
from can import Message
from math import floor

# Calculation of current timestamp in milliseconds (rounded to the 10ms)
def current_time_milli() -> int:
    return floor(time() *  100)

# Conversion of integers to data bytes
def intToDataBytes(n: int) -> list:
    return list(n.to_bytes((n.bit_length() + 7) // 8, byteorder='big'))

# Conversion of data bytes to integers
def dataBytesToInt(data: list) -> int:
    return int.from_bytes(data, byteorder= 'big')

# Exception in case the ECU finds itself in bus off mode
class ECUInBusOffMode(Exception):
    pass

# Class that defines the emulation of an ECU
class ECU:

    # Constructor of the ECU
    def __init__(self, channel: str, interface: str):

        # Connection of the ECU to the bus socket
        self.__bus = Bus(channel= channel, interface= interface)

        # Error counters for the ECU
        self.__tec = 0
        self.__rec = 0

    # Confirmation if the ECU is bus off mode
    def __isBusOff(self) -> bool:

        # Condition for bus off mode
        return (self.__tec > 127 or self.__rec > 127)

    # Receiving of messages from the bus
    def rcv(self, timeout: float = None) -> None | Message:

        # Confirms if the ECU is bus off
        if self.__isBusOff():
            raise ECUInBusOffMode()

        # Tries to get a message from the bus
        try:

            # Get the message if sucessful
            msg = self.__bus.recv(timeout= timeout)
        
            # Decreases the counter if sucessful
            if self.__rec > 0:
                self.__rec -= 1

            # Return the caught message
            return msg

        except CanOperationError as Err:

            # Increases the error counter if not
            self.__rec += 1

            # Throws the exception back out
            raise Err
        
    # Sending of messages from the bus
    def send(self, msg: Message) -> None:
        
        # Confirms if the ECU is bus off
        if self.__isBusOff():
            raise ECUInBusOffMode()
        
        # Tries to send a message on the bus
        try:

            # Executes the transmission of the message
            self.__bus.send(msg= msg)

            # Decreases the counter if sucessful
            if self.__tec > 0:
                self.__tec -= 1

        except CanOperationError as Err:

            # Increases the error counter in case of error
            self.__tec += 8

            # Throws the exception back out
            raise Err
        
    # Close the bus connection
    def close(self):
        self.__bus.shutdown()

# Class that emulates an ECU which contains the agent software    
class AgentECU(ECU):
    
    # Constructor of the ECU
    def __init__(self, channel: str, interface: str, unique_id: int, agent: Agent):

        # Call for the ECU constructor
        super().__init__(channel, interface)

        # Association of the unique seed broadcast id
        self.__broadcast = unique_id

        # Building of the operating agent
        self.__agent = agent

    # Initialization of the agent node
    def initialize(self) -> None:

        # Initialization of the agent
        seed = self.__agent.initialize()

        # Will keep trying until it can broadcast the seed
        while True:
            
            try:

                # Communication of the seed in the bus
                super().send(Message(arbitration_id= self.__broadcast, data= intToDataBytes(seed)))

                # Stops in case of broadcast
                return

            except CanOperationError:

                # Ignore errors
                pass

    # Send a message to the bus
    def send(self, msg: Message) -> None:

        try:

            # Wait for a message or for clock synch
            super().rcv()

            # Get the current IBN span
            ibn = self.__agent.current(msg.arbitration_id)

            # Wait the time needed without messages to send the messages
            while super().rcv(ibn * 0.01) is not None:
                pass

            # Send the message after confirming the time
            super().send(msg)

        except CanOperationError:

            # Retry in case of failure
            self.send(msg)

# Class that emulates the behaviour of the Officer ECU
class OfficerECU():

    # Constructor of the ECU
    def __init__(self, channel: str, interface: str, agents: list):

        # Constructor of the super class
        self.__ecu = ECU(channel, interface)

        # Building of the operating officer
        self.__officer = Officer(agents)

    # Handling of an incoherent IBN
    def __handler(self, msg: Message) -> None:
        
        # Flag in the console the bad message
        print(f'{msg.arbitration_id}: {msg.data} -> FLAGGED!')

    # Officer opperation
    def operate(self) -> None:

        # In case a general error occurs
        try:

            # Keeps looking as long as the system works
            while True:
                
                # Get the current timestamp before collecting the message
                before = current_time_milli()

                # Waits for a message to verify
                msg = self.__ecu.rcv(1.28)

                # Get the current timestamp after collecting the message
                after = current_time_milli()

                # Checks if the message arrive
                if msg is not None:

                    # In case an attacker tries to forge the initialization
                    try:
                    
                        # Check if message is broadcast
                        if msg.arbitration_id > 9 and msg.arbitration_id < 30:
                            
                            # Initialize the agent with the received broadcast
                            self.__officer.initialize(msg.arbitration_id, dataBytesToInt(msg.data))

                        # Check if message timing is correct
                        else:

                            # Calculate the IBN and check it for message id
                            if not self.__officer.check(msg.arbitration_id, after - before):
                                self.__handler(msg)

                    except NoAgentForGivenId | AgentAlreadyInitialized:

                        # Handle the incoherent message
                        self.__handler(msg)

                # If no message arrive, resets the clock
                else:

                    # Sends the clock reset message
                    self.__ecu.send(Message(arbitration_id= 0, data= [0x00]))

        except CanOperationError:

            # Recall the operate function
            self.operate()

    # Officer shutdown
    def close(self):
        self.__ecu.close()
