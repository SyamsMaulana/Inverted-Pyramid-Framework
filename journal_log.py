



import datetime
import os

LEDGER_FILE = "al_haqq_ledger.md"

def write_journal():
    print("=== Al-Haqq Digital Ledger & Journal ===")
    title = input("Judul Refleksi / Catatan: ")
    content = input("Isi Catatan: ")
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
## [{current_time}] {title}
{content}

*(Cap digital kolaborasi pemikiran ICAM & AI — Al-Haqq Framework)*
---
"""
    
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    print(f"\n[Berhasil] Catatan berhasil direkam ke dalam {LEDGER_FILE}")

if __name__ == "__main__":
    write_journal()

