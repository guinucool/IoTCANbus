import can
import time

def write_to_can():
    try:
        # Create a CAN bus instance
        bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

        for i in range(5):
            try:
                # Construct and send a message
                while True:
                    message = can.Message(arbitration_id=0x123, data=[i+1, i+2, i+3], is_extended_id=False)
                    bus.send(message)
                    print(f"Message sent: {message}")
                    time.sleep(1)
            except can.CanError as e:
                print(f"CAN Error while sending message: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    write_to_can()