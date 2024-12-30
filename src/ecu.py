from can.exceptions import CanOperationError
from can.interface import Bus
from can import Message

# Exception in case the ECU finds itself in bus off mode
class ECUInBusOffMode(Exception):
    pass

# Class that defines the emulation of an ECU
class ECU:

    # Constructor of the ECU
    def __init__(self, channel: str, interface: str):

        # Connection of the ECU to the bus socket
        self.__bus__ = Bus(channel= channel, interface= interface)

        # Error counters for the ECU
        self.__tec__ = 0
        self.__rec__ = 0

    # Confirmation if the ECU is bus off mode
    def __isBusOff__(self) -> bool:

        # Condition for bus off mode
        return (self.__tec__ > 127 or self.__rec__ > 127)

    # Receiving of messages from the bus
    def rcv(self, timeout: int) -> None | Message:

        # Confirms if the ECU is bus off
        if self.__isBusOff__:
            raise ECUInBusOffMode()

        # Tries to get a message from the bus
        try:

            # Get the message if sucessful
            msg = self.__bus__.recv(timeout= timeout)
        
            # Decreases the counter if sucessful
            if self.__rec__ > 0:
                self.__rec__ -= 1

            # Return the caught message
            return msg

        except CanOperationError as Err:

            # Increases the error counter if not
            self.__rec__ += 1

            # Throws the exception back out
            raise Err
        
    # Sending of messages from the bus
    def send(self, msg: Message) -> None:
        
        # Confirms if the ECU is bus off
        if self.__isBusOff__:
            raise ECUInBusOffMode()
        
        # Tries to send a message on the bus
        try:

            # Executes the transmission of the message
            self.__bus__.send(msg= msg)

            # Decreases the counter if sucessful
            if self.__tec__ > 0:
                self.__tec__ -= 1

        except CanOperationError as Err:

            # Increases the error counter in case of error
            self.__tec__ += 8

            # Throws the exception back out
            raise Err
