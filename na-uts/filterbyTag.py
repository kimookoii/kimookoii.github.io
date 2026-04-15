import pynetbox
from netmiko import ConnectHandler

# Koneksi ke Netbox
NB_URL = "http://10.10.93.61:8000"
NB_TOKEN = "GLYzO9mDMpnkmJrCJ7MW4GnTFJEWBWuAcVnXdYFl"

nb = pynetbox.api(url=NB_URL, token=NB_TOKEN)


def run_health_check():
    # Ambil hanya IP dengan tag "prod"
    ip_list = list(nb.ipam.ip_addresses.filter(status='active', tag='prod'))
    print(f"Ditemukan {len(ip_list)} IP dengan tag 'prod'. Memulai otomasi...\n")

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

        except Exception as e:
            print(f"Gagal koneksi ke {target_ip}: {e}")
            with open("error_log.txt", "a") as f:
                f.write(f"{target_ip} - {e}\n")


if __name__ == "__main__":
    run_health_check()