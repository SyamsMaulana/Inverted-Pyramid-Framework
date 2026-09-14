


import json

with open('tcg_framework.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

framework = data['tcg_framework']
print(f"--- {framework['title']} ({framework['protocol']}) ---")
print(f"Author: {framework['author']} | Version: {framework['version']}\n")

print("Fundamental Rulings:")
for rule in framework['fundamental_rulings']:
    print(f"[{rule['rule_id']}] {rule['name']}: {rule['description']}")

print("\nAlternative Win Conditions & Success Chance:")
for wc in framework['alternative_win_conditions']:
    print(f"- {wc['category']}: {wc['success_chance_min_pct']}% - {wc['success_chance_max_pct']}% (Example: {wc['classic_example']})")

