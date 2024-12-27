import logging
import can
import time

# Enable logging for the CAN library
logging.basicConfig(level=logging.DEBUG)

def listen_to_can():
    try:
        bus = can.interface.Bus(interface='socketcan', channel='vcan0')
        print(bus.state)
        print("Listening to the CAN bus...")
        while True:
            message = bus.recv()
            time.sleep(1)
            message = can.Message(arbitration_id=0x123, data=[0, 0, 0], is_extended_id=False)
            bus.send(message)
            if message:
                print(f"Received: {message}")
    except KeyboardInterrupt:
        print("\nStopped listening.")
    except can.CanError as e:
        print(f"CAN Error encountered: {e}")

if __name__ == "__main__":
    listen_to_can()
