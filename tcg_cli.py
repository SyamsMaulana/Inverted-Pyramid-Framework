


import json
import sys

with open('tcg_framework.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def search_query(keyword):
    fw = data['tcg_framework']
    print(f"\n=== Hasil Pencarian untuk: '{keyword}' ===")
    
    # Cari di rulings
    for r in fw['fundamental_rulings']:
        if keyword.lower() in r['name'].lower() or keyword.lower() in r['description'].lower():
            print(f"[Ruling {r['rule_id']}] {r['name']}\n-> {r['description']}\n")
            
    # Cari di win conditions
    for wc in fw['alternative_win_conditions']:
        if keyword.lower() in wc['category'].lower() or keyword.lower() in wc['classic_example'].lower():
            print(f"[Win Con] {wc['category']} (Peluang: {wc['success_chance_min_pct']}-{wc['success_chance_max_pct']}%)")
            print(f"-> {wc['description']} (Contoh: {wc['classic_example']})\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_query(sys.argv[1])
    else:
        print("Gunakan: python3 tcg_cli.py <kata_kunci>")

