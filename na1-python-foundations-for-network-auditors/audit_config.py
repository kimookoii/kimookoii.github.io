import os
import json

# menentukan folder tempat script berada
base_dir = os.path.dirname(os.path.abspath(__file__))

# lokasi file config router
file_path = os.path.join(base_dir, "config_router.txt")

hostname = None
password_encryption = True
telnet_enabled = False

# membaca file konfigurasi router
with open(file_path, "r") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()

    # mencari hostname
    if line.startswith("hostname"):
        hostname = line.split()[1]

    # cek password encryption
    if "no service password-encryption" in line:
        password_encryption = False

    # cek telnet
    if "transport input telnet" in line:
        telnet_enabled = True

# membuat hasil audit
result = {
    "hostname": hostname,
    "password_encryption_enabled": password_encryption,
    "telnet_enabled": telnet_enabled
}

# menyimpan hasil ke JSON
output_path = os.path.join(base_dir, "audit_result.json")

with open(output_path, "w") as json_file:
    json.dump(result, json_file, indent=4)

print("Audit selesai")
print("Hostname:", hostname)
print("Password Encryption:", password_encryption)
print("Telnet Enabled:", telnet_enabled)
print("Hasil disimpan di:", output_path)