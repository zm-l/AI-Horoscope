import json
import os
from agent import StarWhisperAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "user_db.json")

def load_user_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8-sig') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading database: {e}")
        return {}


def save_user_db(data):
    with open(DB_FILE, 'w', encoding='utf-8-sig') as file:
        json.dump(data, file, indent=2)


def process_user_visit(user_id: str):
    db = load_user_db()
    user_data = db.get(user_id)

    if not user_data:
        print(f"\nNew user detected! Let's set up the profile for '{user_id}'.")

        zodiac_map = {
            "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air",
            "Cancer": "Water", "Leo": "Fire", "Virgo": "Earth",
            "Libra": "Air", "Scorpio": "Water", "Sagittarius": "Fire",
            "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
        }
        while True:
            assigned_zodiac = input(
                f"Please enter the Zodiac sign for {user_id} (e.g., Aries, Taurus): ").strip().capitalize()

            if assigned_zodiac in zodiac_map:
                assigned_element = zodiac_map[assigned_zodiac]
                break
            else:
                print("Invalid Zodiac sign. Please check your spelling and try again.")

        user_data = {
            "is_new": True,
            "zodiac": assigned_zodiac,
            "element": assigned_element,
            "visit_count": 0
        }
        print(f"Profile created: {assigned_zodiac} ({assigned_element}). Generating first reading...\n")

    agent = StarWhisperAgent()

    result = agent.generate_reading(user_id, user_data)

    if "error" in result:
        print(f"Generation failed: {result['error']}")
        return result

    user_data["visit_count"] += 1

    if user_data.get("is_new"):
        user_data["is_new"] = False
        user_data["past_3_days"] = {
            "themes_used": [],
            "styles_used": [],
            "questions_asked": []
        }

    past = user_data.get("past_3_days")
    if not isinstance(past, dict):
        past = {}
        user_data["past_3_days"] = past

    themes = past.get("themes_used", [])
    styles = past.get("styles_used", [])
    questions = past.get("questions_asked", [])

    themes.append(str(result.get("selected_theme", "")))
    styles.append(str(result.get("selected_style", "")))
    questions.append(str(result.get("follow_up_question", "")))

    # Prevent repeat of themes, styles, and questions for last 3 days
    user_data["past_3_days"] = {
        "themes_used": themes[-3:],
        "styles_used": styles[-3:],
        "questions_asked": questions[-3:]
    }

    db[user_id] = user_data
    save_user_db(db)

    return result


# === Test the Flow ===
if __name__ == "__main__":
    print("=== Star Whisper Livestream Engine ===")
    print("Available users in the database:")
    print(" - mookka_th (Day-5 Veteran)")
    print(" - new_visitor_99 (First-Timer)")
    print("--------------------------------------")

    while True:
        user_id = input("\nEnter a User ID (or type 'quit' to exit): ").strip()

        if user_id.lower() in ['quit', 'exit', 'q']:
            print("Shutting down the engine. Goodbye!")
            break

        if user_id:
            response = process_user_visit(user_id)
            print("\n" + json.dumps(response, indent=2))
        else:
            print("Please enter a valid User ID.")