from netmiko import ConnectHandler
from switch_list import switchList
# switch_list.py contains connection info and is excluded from source control

macAddress = ('aa:bb:cc:dd:ee:ff').lower()

def findMac(macAddress):
    command = "show mac-address"
    output = net_connect.send_command(command)
    output_test = output.split('\n')
    output_test2 = []
    for item in output_test:
        item_dump = item.split()
        output_test2.append(item_dump)
    for interface in output_test2:
        try:
            if macAddress in interface:
                return(interface)
        except:
            pass

def getConfig():
    command = "show run"
    output = net_connect.send_command(command)
    return output

def getMacs():
    command = "show mac-address"
    output = net_connect.send_command(command)
    output_test = output.split('\n')
    output_test2 = []
    for item in output_test:
        item_dump = item.split()
        output_test2.append(item_dump)
    return output_test2

def getDeviceDetails():
    command = "Getmib sysDescr.0"
    output = net_connect.send_command(command)
    return output

for switch in switchList:
    try:
        print("")
        print(switch["host"])
        net_connect = ConnectHandler(**switch)

        print(findMac(macAddress))
        
    except:
        pass
