from netmiko import ConnectHandler
from datetime import datetime
import requests
import csv
import os

BOT_TOKEN = "8700160160:AAFc9EpQSOLUce9DUHBWdeurKftLkJbTjeM"
CHAT_ID ='-5280260003'

def kirim_file_telegram(file_path, device_name):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as f:
        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": f"Backup config: {device_name}"
            },
            files={"document": f}
        )

    return response.status_code


def load_devices(file):
    devices = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["port"] = int(row["port"])
            devices.append(row)
    return devices

devices = load_devices("devices.csv")

vendor_command = {
    "mikrotik_routeros": "/export",
    "cisco_ios": "show running-config",
    "juniper": "show configuration | display set",
    "huawei": "display current-configuration",
    "zte": "show running-config",
    "linux": "show configuration"
}

for device in devices:
    try:
        device_copy = device.copy()
        device_name = device_copy.pop("name")
        print(f"connecting to {device_copy['host']} ({device_name})...")

        connection = ConnectHandler(**device_copy)
        device_type = device["device_type"]
        base_type = device_type.replace("_telnet", "")
        command = vendor_command.get(base_type)

        if base_type == "linux":
            connection.send_command("cli", expect_string=r"[#$]")
            output = connection.send_command(
                command,
                expect_string=r"\$",
                read_timeout=30
            )
        else:
            output = connection.send_command(command)

        if "_telnet" in device_type:
            print("Using TELNET connection")

        if not command:
            print(f"Tidak ada command untuk {device['device_type']}")
            continue

        if device["device_type"] == "zte":
            connection.send_command("terminal length 0")

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = "C:/Users/Rifo/Documents/BACKUP-CONFIG-DEVICE/"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}backup_{device_name}_{now}.rsc"

        with open(filename, "w") as f:
            f.write(output)

        print(f"Backup saved: {filename}")
        status = kirim_file_telegram(filename, device_name)

        if status == 200:
            print("Berhasil kirim ke Telegram")
        else:
            print("Gagal kirim ke Telegram")

        connection.disconnect()

    except Exception as e:
        print(f"Error di {device['host']}: {e}")