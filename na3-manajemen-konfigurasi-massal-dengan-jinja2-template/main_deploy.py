import json
from jinja2 import Template
from netmiko import ConnectHandler

def deploy_konfigurasi():
    # 1. Load Data
    with open("ip_inventory.txt", "r") as f:
        routers = f.read().splitlines()
    with open("data_mahasiswa.json", "r") as f:
        student = json.load(f)
    with open("user_template.j2", "r") as f:
        tmpl = Template(f.read())
    
    perintah = tmpl.render(student)

    # 2. Eksekusi ke 10 Router
    for ip in routers:
        if not ip.strip(): continue
        
        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip.strip(),
            'username': 'admin', # Akun Instruktur
            'password': 'polibest123',      
        }

        try:
            print(f"Menghubungkan ke {ip}...")
            with ConnectHandler(**device) as link:
                link.send_config_set(perintah.splitlines())
                print(f"✅ Berhasil di {ip}")
        except Exception as e:
            print(f"❌ Gagal di {ip}: {e}")

if __name__ == "__main__":
    deploy_konfigurasi()
