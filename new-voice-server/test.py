
import psutil
 
# Calling psutil.cpu_precent() for 4 seconds
print('The CPU usage is: ', psutil.cpu_percent(1))
print('memory % used:', psutil.virtual_memory()[2])

import os
import psutil
from time import sleep

# Getting loadover15 minutes
load1, load5, load15 = psutil.getloadavg()
 
cpu_usage = (load15/os.cpu_count()) * 100
 
print("The CPU usage is : ", cpu_usage)

def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result

print(get_cpu_temp())

# sleep(4)
# print("Reboot")
# os.system("systemctl reboot -i")

# import psutil
# import time

# while True:
#     cpu_percent = psutil.cpu_percent(interval=1)
#     print(f"CPU Usage: {cpu_percent}%")
#     time.sleep(1)
