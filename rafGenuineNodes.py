import can
import threading
import time

def send_genuine_frames(interface, node_id, interval, arbitration_id):
    """
    Sends periodic CAN frames to simulate a genuine node.
    """
    bus = can.Bus(interface, bustype="socketcan")
    print(f"Genuine node {node_id} sending frames with ID={hex(arbitration_id)} every {interval} seconds...")

    while True:
        try:
            msg = can.Message(arbitration_id=arbitration_id, data=[node_id] * 8, is_extended_id=False)
            bus.send(msg)
            print(f"Node {node_id} sent: {msg}")
            time.sleep(interval)
        except can.CanError as e:
            print(f"Error sending message: {e}")
            break

def main():
    interface = "vcan0"

    # Start a thread for the genuine node
    threading.Thread(
        target=send_genuine_frames, args=(interface, 1, 0.5, 0x100), daemon=True
    ).start()  # Node 1 with 500ms interval

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
