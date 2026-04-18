from netmiko.ssh_dispatcher import CLASS_MAPPER

for device in CLASS_MAPPER.keys():
    print(device)