import json
from netmiko import ConnectHandler

def verifikasi_audit():
    with open("data_mahasiswa.json", "r") as f:
        target = json.load(f)
    with open("ip_inventory.txt", "r") as f:
        routers = f.read().splitlines()

    username = target['user_router']
    print(f"--- MEMULAI VERIFIKASI USER: {username} ---")

    for ip in routers:
        if not ip.strip(): continue
        
        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip.strip(),
            'username': 'admin',
            'password': 'polibest123',      
        }

        try:
            with ConnectHandler(**device) as link:
                # Mengambil daftar user (Read-Only)
                output = link.send_command("/user print without-paging")
                
                if username in output:
                    print(f"✅ IP {ip}: TERVERIFIKASI")
                else:
                    print(f"❌ IP {ip}: TIDAK DITEMUKAN")
        except Exception as e:
            print(f"⚠️ IP {ip}: ERROR ({e})")

if __name__ == "__main__":
    verifikasi_audit()
