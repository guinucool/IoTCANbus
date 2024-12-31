from random import randint
from zbcan import Agent
from ecu import AgentECU, intToDataBytes, ECUInBusOffMode, OfficerECU
from can import Message
from time import sleep

# List of available agents
agents = [
    Agent(1222848320, [11, 30, 128, 1024, 1025]),
    Agent(1570050167, [10, 31]),
    Agent(896026477, []),
    Agent(466217088, [129]),
    Agent(1460528862, [130]),
    Agent(2102876160, [])
]

# Emulation of the motor termometer
def motorTermo():

    # Creation of the operating ECU
    agent = AgentECU('vcan0', 'socketcan', 10, agents[1])

    # Initialization of the ECU
    agent.initialize()

    try:

        # Simulation of the ECU temperatures (randomly)
        while True:

            # Random range of temperature
            temp = randint(60, 120)

            # Print the temperature reading
            print(f'Current Temp - {temp}ºC')

            # Send the readings to the bus
            agent.send(Message(arbitration_id= 31, data= intToDataBytes(temp)))

            # Delay until the next reading
            sleep(1)

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        agent.close()

# Emulation of the command dashboard
def vehicleController():

    # Creation of the acting ECU agent
    agent = AgentECU('vcan0', 'socketcan', 11, agents[0])

    # Initialization of the ECU
    agent.initialize()

    try:

        # Simulation of the Control Panel
        while True:

            # Wait for command input
            cmd = input('Insert command: ')

            # Check if command is valid
            if cmd in ['A', 'B', 'N', 'L', 'R', 'D', 'F', 'T']:

                # Message placeholder for future message
                msg = None

                # Creates the message based on the command

                if cmd in ['A', 'B', 'N']:

                    # Accelaration, braking or neutral command
                    msg = Message(arbitration_id= 30, data= [ord(cmd)])

                if cmd in ['L', 'R']:

                    # Left and right signal
                    msg = Message(arbitration_id=128, data= [ord(cmd)])

                if cmd == 'D':

                    # Lock or unlock doors
                    msg = Message(arbitration_id=1024, data= [0x00])

                if cmd in ['F', 'T']:

                    # Switch lights for front or back
                    msg = Message(arbitration_id=1025, data= [ord(cmd)])

                # Send the message
                agent.send(msg)

            else:

                # Informs the user of invalid command
                print('Invalid command given!')

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        agent.close()

# Emulation of the officer ECU
def officer():

    # Creation of the operating ECU
    officer = OfficerECU('vcan0', 'socketcan', agents)

    try:

        # Execute the operations of the officer
        officer.operate()

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        officer.close()