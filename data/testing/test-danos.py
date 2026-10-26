from netmiko import ConnectHandler

devices = [
    {
        "device_type": "linux",
        "host": "103.133.25.67",
        "username": "dan0s",
        "password": "!Tahun2025",
        "port": 2245,
        "name": "ROUTER_DANOS"
    }
]

for device in devices:
    try:
        device_copy = device.copy()
        device_name = device_copy.pop("name")

        print(f"connecting to {device_copy['host']} ({device_name})...")

        connection = ConnectHandler(**device_copy)
        
        output = connection.send_command(
            "show configuration",
            expect_string=r"\$"
        )
        print("=== OUTPUT ===")
        print(output)

        connection.disconnect()

    except Exception as e:
        print(f"Error di {device['host']}: {e}")