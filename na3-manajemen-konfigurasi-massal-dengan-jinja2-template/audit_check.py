import json
from netmiko import ConnectHandler

def verifikasi_audit():
    # Membaca data mahasiswa
    with open("data_mahasiswa.json", "r") as f:
        target = json.load(f)

    # Membaca daftar IP router
    with open("ip_inventory.txt", "r") as f:
        routers = f.read().splitlines()

    username = target['user_router']
    nim = target['nim']

    print(f"--- MEMULAI VERIFIKASI USER: {username} ---")

    hasil_audit = []

    for ip in routers:
        if not ip.strip():
            continue
        
        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip.strip(),
            'username': 'admin',
            'password': 'polibest123',
        }

        try:
            with ConnectHandler(**device) as link:
                output = link.send_command("/user print without-paging")

                if username in output:
                    status = "TERVERIFIKASI"
                    print(f"✅ IP {ip}: {status}")
                else:
                    status = "TIDAK DITEMUKAN"
                    print(f"❌ IP {ip}: {status}")

        except Exception as e:
            status = f"ERROR ({e})"
            print(f"⚠️ IP {ip}: {status}")

        hasil_audit.append({
            "ip_router": ip,
            "username": username,
            "status": status
        })

    # Nama file hasil audit sesuai aturan penilaian
    nama_file = f"audit_result_{nim}.json"

    with open(nama_file, "w") as f:
        json.dump(hasil_audit, f, indent=4)

    print(f"\nHasil audit disimpan ke file: {nama_file}")

if __name__ == "__main__":
    verifikasi_audit()