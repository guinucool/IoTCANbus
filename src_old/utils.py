import time

# Calculation of current timestamp in milliseconds
def current_time_milli() -> int:
    return round(time.time() *  1000)