









import os
import subprocess

def check_health():
    print("=== Al-Haqq Repository & System Health ===")
    
    # Cek status git
    print("\n[1] Status Git Lokal:")
    try:
        result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(result.stdout)
        else:
            print("Semua file bersih dan tersinkronisasi (Clean working tree).")
    except Exception as e:
        print(f"Gagal mengecek git status: {e}")
        
    # Cek keberadaan file inti
    print("\n[2] Integritas Berkas Sistem:")
    files = ["protocol_state.json", "dashboard.py", "scheduler.py", "make_schema.py", "journal_log.py"]
    for f in files:
        exists = os.path.exists(f)
        status_text = "Hadir & Aman" if exists else "Belum Dibuat"
        print(f" - {f}: {status_text}")

if __name__ == "__main__":
    check_health()
