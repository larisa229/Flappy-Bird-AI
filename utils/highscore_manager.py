import json
import os

SCORE_FILE = "data/scores.json"

class HighscoreManager:

    @staticmethod
    def _ensure_file():
        if not os.path.exists("data"):
            os.mkdir("data")

        if not os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "w") as f:
                json.dump({"manual": [], "auto": []}, f)

    @staticmethod
    def load_scores():
        HighscoreManager._ensure_file()

        with open(SCORE_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_score(score, mode="manual"):
        HighscoreManager._ensure_file()

        data = HighscoreManager.load_scores()
        data[mode].append(score)

        with open(SCORE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_best_score(mode="manual"):
        data = HighscoreManager.load_scores()
        return max(data[mode]) if data[mode] else 0

    @staticmethod
    def get_top_scores(mode="manual", limit=5):
        data = HighscoreManager.load_scores()
        return sorted(data[mode], reverse=True)[:limit]
