import json
import re
from datetime import datetime
from collections import Counter
from netmiko import ConnectHandler

def run_mitigation():
    with open("ip_inventory.txt", "r") as f:
        routers = f.read().splitlines()
    
    # Aturan: Blokir jika gagal >= 5 kali
    threshold = 5

    # Struktur hasil JSON
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "threshold": threshold,
        "routers": []
    }

    for ip in routers:
        if not ip.strip(): continue
        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip.strip(),
            'username': 'admin',
            'password': 'polibest123',
        }

        router_result = {
            "router_ip": ip.strip(),
            "status": "",
            "blocked_ips": [],
            "total_attacks_detected": 0,
            "error": None
        }

        try:
            print(f"\n🔍 Memeriksa Router: {ip}")
            with ConnectHandler(**device) as link:
                raw_logs = link.send_command("/log print without-paging")
                
                # Ekstrak IP penyerang menggunakan Regex
                attacker_ips = re.findall(r'from\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', raw_logs)
                counts = Counter(attacker_ips)
                
                for attacker, total in counts.items():
                    if total >= threshold:
                        print(f"⚠️ SERANGAN TERDETEKSI! IP {attacker} mencoba {total} kali.")
                        cmd = f'/ip firewall address-list add list=Blacklist address={attacker} comment="AutoBlock_AI"'
                        link.send_command(cmd)
                        print(f"✅ IP {attacker} berhasil diblokir di {ip}")

                        router_result["blocked_ips"].append({
                            "attacker_ip": attacker,
                            "attempt_count": total,
                            "action": "blocked"
                        })

                router_result["total_attacks_detected"] = len(router_result["blocked_ips"])
                router_result["status"] = "success"

        except Exception as e:
            print(f"❌ Koneksi Gagal ke {ip}: {e}")
            router_result["status"] = "failed"
            router_result["error"] = str(e)

        results["routers"].append(router_result)

    # Simpan hasil ke file JSON
    with open("mitigation_result.json", "w") as f:
        json.dump(results, f, indent=4)
    
    # Tampilkan hasil JSON di terminal
    print("\n" + "="*50)
    print("📋 HASIL MITIGASI (JSON):")
    print("="*50)
    print(json.dumps(results, indent=4))
    print(f"\n💾 Hasil disimpan ke: mitigation_result.json")

if __name__ == "__main__":
    run_mitigation()
