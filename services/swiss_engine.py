import json
import os

DB_FILE = "tournament_data.json"

class SwissTournament:
    def __init__(self, name="GOD•MauL TCG Championship"):
        self.name = name
        self.players = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.name = data.get("name", self.name)
                    self.players = data.get("players", [])
                except json.JSONDecodeError:
                    self.players = []

    def save_data(self):
        data = {
            "name": self.name,
            "players": self.players
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_player(self, name):
        if not any(p["name"] == name for p in self.players):
            self.players.append({"name": name, "points": 0, "opponents": []})
            self.save_data()
            print(f"[+] Peserta terdaftar: {name}")
        else:
            print(f"[!] Peserta {name} sudah terdaftar.")

    def generate_pairings(self):
        sorted_players = sorted(self.players, key=lambda x: x["points"], reverse=True)
        pairings = []
        paired = set()

        for i, p1 in enumerate(sorted_players):
            if p1["name"] in paired:
                continue
            
            opponent = None
            for j in range(i + 1, len(sorted_players)):
                p2 = sorted_players[j]
                if p2["name"] not in paired and p2["name"] not in p1["opponents"]:
                    opponent = p2
                    break
            
            if not opponent:
                for j in range(i + 1, len(sorted_players)):
                    p2 = sorted_players[j]
                    if p2["name"] not in paired:
                        opponent = p2
                        break

            if opponent:
                pairings.append((p1["name"], opponent["name"]))
                paired.add(p1["name"])
                paired.add(opponent["name"])
            else:
                pairings.append((p1["name"], "BYE (Free Win)"))
                paired.add(p1["name"])

        return pairings

    def record_match(self, p1_name, p2_name, result):
        # result: 'p1', 'p2', or 'draw'
        for p in self.players:
            if p["name"] == p1_name and p2_name != "BYE (Free Win)":
                if p2_name not in p["opponents"]:
                    p["opponents"].append(p2_name)
            if p["name"] == p2_name and p1_name != "BYE (Free Win)":
                if p1_name not in p["opponents"]:
                    p["opponents"].append(p1_name)

        if p2_name == "BYE (Free Win)":
            for p in self.players:
                if p["name"] == p1_name:
                    p["points"] += 3
        else:
            if result.lower() == 'p1':
                for p in self.players:
                    if p["name"] == p1_name: p["points"] += 3
            elif result.lower() == 'p2':
                for p in self.players:
                    if p["name"] == p2_name: p["points"] += 3
            elif result.lower() == 'draw':
                for p in self.players:
                    if p["name"] == p1_name or p["name"] == p2_name: p["points"] += 1

        self.save_data()
        print(f"[OK] Hasil pertandingan berhasil dicatat.")

    def standings(self):
        sorted_players = sorted(self.players, key=lambda x: x["points"], reverse=True)
        print(f"\n=== KLASEMEN SEMENTARA: {self.name} ===")
        for idx, p in enumerate(sorted_players, 1):
            print(f"{idx}. {p['name']} — {p['points']} Poin")
        print("=========================================\n")

if __name__ == "__main__":
    import sys
    tourney = SwissTournament()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "add" and len(sys.argv) > 2:
            tourney.add_player(sys.argv[2])
        elif cmd == "pair":
            pairings = tourney.generate_pairings()
            print("\n--- PAIRING BABAK INI ---")
            for idx, (p1, p2) in enumerate(pairings, 1):
                print(f"Meja {idx}: {p1} VS {p2}")
            print("-------------------------\n")
        elif cmd == "win" and len(sys.argv) > 4:
            tourney.record_match(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "standings":
            tourney.standings()
        else:
            print("Perintah tidak dikenal. Gunakan: add <nama>, pair, win <p1> <p2> <p1/p2/draw>, standings")
    else:
            tourney.standings()
