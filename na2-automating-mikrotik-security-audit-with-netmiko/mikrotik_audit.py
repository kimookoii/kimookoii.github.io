# Menggunakan library netmiko untuk membuat koneksi SSH
from netmiko import ConnectHandler

# Digunakan untuk menyimpan hasil audit ke format JSON
import json

# Digunakan untuk mendapatkan lokasi folder script
import os

# Konfigurasi perangkat MikroTik
mikrotik = {
    "device_type": "mikrotik_routeros",
    "host": "10.200.10.127",  # IP MikroTik
    "username": "admin",
    "password": "zeynita",
    "port": 22
}

# Membuat koneksi SSH ke MikroTik menggunakan Netmiko
connection = ConnectHandler(**mikrotik)

# Perintah untuk melihat layanan yang aktif
output = connection.send_command("/ip service print")

# Menampilkan output service MikroTik
print("=== HASIL /ip service print ===")
print(output)


# Audit Keamanan Berupa Cek protokol rentan seperti Telnet dan FTP
vulnerabilities = []

# Mengecek apakah telnet aktif
if "telnet" in output.lower():
    vulnerabilities.append("Telnet service aktif (VULNERABLE)")

# Mengecek apakah ftp aktif
if "ftp" in output.lower():
    vulnerabilities.append("FTP service aktif (VULNERABLE)")

# Menyusun hasil audit
result = {
    "mikrotik_ip": mikrotik["host"],
    "service_output": output,
    "vulnerabilities_found": vulnerabilities
}

# Menentukan folder tempat script berada
base_dir = os.path.dirname(__file__)

# Membuat path file JSON di folder yang sama dengan script
file_path = os.path.join(base_dir, "audit_result.json")

# Output JSON
with open(file_path, "w") as file:
    json.dump(result, file, indent=4)
    
print("\n=== HASIL AUDIT KEAMANAN ===")
if vulnerabilities:
    for v in vulnerabilities:
        print("-", v)
else:
    print("Tidak ditemukan kerentanan.")

print("\nHasil audit disimpan ke file:", file_path)