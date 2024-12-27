import can

def send_malformed_frame():
    bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=100)
    
    # Create a malformed message with invalid DLC (e.g., greater than 8 bytes)
    malformed_message = can.Message(
        arbitration_id=0x123,
        data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],  # 9 bytes, which is invalid
        is_extended_id=False,
        is_error_frame=True
    )

    try:
        bus.send(malformed_message, 1)
        print(f"Malformed message sent: {malformed_message}")
    except can.CanError as e:
        print(f"Failed to send malformed message: {e}")

if __name__ == "__main__":
    send_malformed_frame()
