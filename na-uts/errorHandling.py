import pynetbox
from netmiko import ConnectHandler
from datetime import datetime
import os

# Ambil path folder tempat file Python ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "error_log.txt")

# Koneksi ke Netbox
NB_URL = "http://10.10.93.61:8000"
NB_TOKEN = "GLYzO9mDMpnkmJrCJ7MW4GnTFJEWBWuAcVnXdYFl"

nb = pynetbox.api(url=NB_URL, token=NB_TOKEN)

# Nama mahasiswa
NAMA = "ZICO NAKANO"


def run_health_check():
    ip_list = list(nb.ipam.ip_addresses.filter(status='active'))
    print(f"Ditemukan {len(ip_list)} IP di Netbox. Memulai otomasi...\n")
    print(f"Lokasi file log: {LOG_FILE}\n")  # Debug biar kelihatan

    for ip_obj in ip_list:
        target_ip = str(ip_obj.address).split('/')[0]

        print(f"--- Menghubungkan ke Mikrotik: {target_ip} ---")

        device_params = {
            'device_type': 'mikrotik_routeros',
            'host': target_ip,
            'username': 'admin',
            'password': 'polibest123',
            'timeout': 5,
        }

        try:
            with ConnectHandler(**device_params) as ssh:
                output = ssh.send_command("/ip address print")
                print(output)
                print(f"Status {target_ip}: [OK]")

                # Update description di NetBox
                tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                deskripsi = f"Verified by {NAMA} pada {tanggal}"

                ip_obj.description = deskripsi
                ip_obj.save()

                print(f"Deskripsi berhasil diupdate: {deskripsi}")

        except Exception as e:
            print(f"Gagal koneksi ke {target_ip}: {e}")

            # Logging error (pasti ke folder script)
            waktu_error = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log = f"[{waktu_error}] {target_ip} - FAILED - {e}\n"

            try:
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(log)
                print(f"Log tersimpan ke: {LOG_FILE}")
            except Exception as log_error:
                print(f"Gagal menulis log: {log_error}")

            continue


if __name__ == "__main__":
    run_health_check()