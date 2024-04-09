import psutil

def is_power_connected():
    return psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

power_status = is_power_connected()
if power_status is not None:
    if power_status:
        print("Power cable is connected.")
    else:
        print("Power cable is not connected.")
else:
    print("Unable to determine power status.")
