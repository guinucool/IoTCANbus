from random import randint
from zbcan import Agent
from ecu import AgentECU, intToDataBytes, ECUInBusOffMode, OfficerECU, ECU, ClockECU, dataBytesToInt
from can import Message
from time import sleep

# List of available agents
agents = [
    Agent(1222848320, [11, 30, 128, 1024, 1025]),
    Agent(1570050167, [10, 31]),
    Agent(896026477, [13]),
    Agent(466217088, [12, 129]),
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
            sleep(5)

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
            if cmd in ['A', 'B', 'L', 'R', 'D', 'F', 'T']:

                # Message placeholder for future message
                msg = None

                # Creates the message based on the command

                if cmd in ['A', 'B']:

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

# Emulation of the wheels
def wheels():

    # Creation of the operating ECU
    agent = AgentECU('vcan0', 'socketcan', 12, agents[3])

    # Initialization of the ECU
    agent.initialize()

    # Velocity of the wheels
    vel = 0

    try:

        # Simulation of the wheels velocity
        while True:

            # Wait for an instruction
            msg = agent.rcv()

            # Evaluate the instruction
            if msg is not None and msg.arbitration_id == 30:

                # Change the state to the state of the instruction
                state = chr(msg.data[0])

                # Depending on the state update the velocity

                if state == 'A' and vel < 200:

                    # Generate a random accelaration
                    a = randint(0, 10)

                    # Association of this accelaration to the velocity
                    vel += a

                if state == 'B' and vel > 0:

                    # Generate a random braking
                    b = randint(0, 10)

                    # Association of this breaking to the velocity
                    vel -= a

                    # Check if velocity is above 0
                    if vel < 0:
                        vel = 0

                # Print the temperature reading
                print(f'Current Velocity - {vel} km/h')

                # Send the velocity to the dashboard
                agent.send(Message(arbitration_id= 129, data= intToDataBytes(vel)))

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        agent.close()

# Emulation of the cooling system for the motor
def cooler():

    # Creation of the operating ECU
    agent = AgentECU('vcan0', 'socketcan', 13, agents[2])

    # Initialization of the ECU
    agent.initialize()

    try:

        # Simulation of the cooler system
        while True:

            # Wait for an instruction
            msg = agent.rcv()

            # Evaluate the instruction
            if msg is not None and msg.arbitration_id == 31:

                # Check the temperature of the instruction
                temp = dataBytesToInt(msg.data)

                # Depending on the temperature update the system

                if temp > 90:

                    # Start cooling (simulated)
                    print('Cooling down!')

                else:

                    # Stop cooling (simulated)
                    print('Stop cooling...')

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        agent.close()

# Emulation of a termometer attacker
def attacker():

    # Creation of the ECU
    ecu = ECU('vcan0', 'socketcan')

    try:

        # Simulation of the ECU temperatures (randomly)
        while True:

            # Send the attack to the bus
            ecu.send(Message(arbitration_id= 31, data= [0x00]))

            # Print the attack message
            print(f'Attack sent!')

            # Delay until the next attack
            sleep(1)

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        ecu.close()

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

# Emulation of the clock
def clock():

    # Creation of the operating ECU
    clock = ClockECU('vcan0', 'socketcan')

    try:

        # Execute the operations of the officer
        clock.operate()

    except KeyboardInterrupt:

        # Information of normal closing
        print('The ECU finished normally!')

    except ECUInBusOffMode:

        # In case of failure of the ECU
        print('The ECU crashed into Bus Off Mode!')

    finally:

        # Closing of the ECU connection to the CAN bus
        clock.close()