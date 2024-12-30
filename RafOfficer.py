import can
import time

def monitor_and_detect(interface):
    """
    Monitors the CAN bus for timing anomalies and disables attackers.
    """
    bus = can.Bus(interface, bustype="socketcan")
    print("Officer monitoring the CAN bus for timing anomalies...")

    # Define the expected timing for genuine nodes
    expected_interval = 0.5  # Expected interval for ID 0x100
    tolerance = 0.1  # Allowable deviation in seconds

    # Track the last timestamp for each monitored CAN ID
    last_seen_timestamps = {}

    while True:
        msg = bus.recv(timeout=1)
        if msg is None:
            continue

        current_time = time.time()
        arbitration_id = msg.arbitration_id

        if arbitration_id == 0x100:  # We're monitoring ID 0x100
            if arbitration_id in last_seen_timestamps:
                # Calculate the time difference since the last message
                delta_time = current_time - last_seen_timestamps[arbitration_id]

                # Detect if the interval deviates from the expected interval
                if abs(delta_time - expected_interval) > tolerance:
                    print(f"Timing anomaly detected for ID={hex(arbitration_id)}! Delta: {delta_time:.2f}s")
                    print("Injecting error frames to disable the attacker...")

                    # Inject error frames to force bus-off
                    for _ in range(32):  # 32 collisions
                        error_frame = can.Message(
                            arbitration_id=0x20000000,  # Error frame identifier
                            is_error_frame=True
                        )
                        bus.send(error_frame)
                        time.sleep(0.001)  # Small delay between error frames

                    print(f"Attacker with ID={hex(arbitration_id)} forced into bus-off state.")
                    break

            # Update the last seen timestamp
            last_seen_timestamps[arbitration_id] = current_time
            print(f"Valid frame received from ID={hex(arbitration_id)} at {current_time:.2f}s")

if __name__ == "__main__":
    monitor_and_detect("vcan0")
