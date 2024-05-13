# import subprocess
# import time
# import os


# def get_cpu_temperature():
#     # Initialize the result.
#     result = 0.0
#     # The first line in this file holds the CPU temperature as an integer times 1000.
#     # Read the first line and remove the newline character at the end of the string.
#     if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
#         with open('/sys/class/thermal/thermal_zone0/temp') as f:
#             line = f.readline().strip()
#         # Test if the string is an integer as expected.
#         if line.isdigit():
#             # Convert the string with the CPU temperature to a float in degrees Celsius.
#             result = float(line) / 1000
#     # Give the result back to the caller.
#     return result

# def reboot_system():
#     """Reboots the system."""

#     subprocess.call(["sudo", "reboot"])

# if __name__ == '__main__':
#     cpu_temperature = get_cpu_temperature()

#     print("CPU temperature is : ", cpu_temperature)

#     # Set the CPU temperature threshold at 85 degrees Celsius.
#     # cpu_temperature_threshold = 85

#     # if cpu_temperature > cpu_temperature_threshold:
#     #     print("CPU temperature is too high! Rebooting system in 5 seconds...")
#     #     time.sleep(5)
#     #     reboot_system()
#     # else:
#     #     print("CPU temperature is normal.")


import psutil
import time
import os

def processcheck(seekitem):
    process_name = "control-panel"
    for p in psutil.process_iter():
        if (seekitem in p.name()):
            cpu = p.cpu_percent(1)
            print(p.name() + " : " + str(p.pid) + " : " + str(cpu))
            if(cpu==0):
                os.system("sudo kill -9 " + str(p.pid))
            if(cpu >= 90):
                os.system("sudo reboot")
            
    # plist = psutil.get_process_list()
    # str1=" ".join(str(x) for x in plist)
    # if seekitem in str1:
    #     print ("Requested process is running")   

processcheck("control-panel")