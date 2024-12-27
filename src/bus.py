import can
import utils

# Bus class to simulate the can bus
class Bus:

    # Constructor of the bus class
    def __init__(self, readChannel, readInterface, writeChannel, writeInterface):

        # Creation of the read and write can bus
        self.__read__ = can.interface.Bus(channel= readChannel, interface= readInterface)
        self.__write__ = can.interface.Bus(channel= writeChannel, interface= writeInterface) 

    # Simulation method
    def simulate(self):

        # Simulate the arbitration behaviour
        while True:

            # Creation of a list to store messages
            arbit = []

            # Wait for a message to arrive
            arbit.append(self.__read__.recv())

            # Get the current timestamp for two variables
            current = utils.current_time_milli()
            after = utils.current_time_milli()

            # Time window for arbitration
            while (current + 10 > after):

                # Collection of messages in the can bus
                arbit.append(self.__read__.recv((current + 10 - after) * 0.001))

                # Get the current timesetamp
                after = utils.current_time_milli()
            