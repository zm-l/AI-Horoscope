import os
import json
import anthropic


class StarWhisperAgent:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(
                "🚨 ANTHROPIC_API_KEY environment variable not found!\n"
                "Please set it before running the script.\n"
                "Mac/Linux: export ANTHROPIC_API_KEY='your-key-here'\n"
                "Windows: set ANTHROPIC_API_KEY='your-key-here'"
            )

        self.client = anthropic.Anthropic(api_key=api_key)

        # Static Room Context
        self.room_context = """
        Location: Thailand (Thai + English mixed audience). 23 users online. 
        Popular room topics: love fortune, exam luck, getting rich. 
        Current Date: 2026-03-31, Tuesday, 8 PM. 
        Astrology weather: Waxing crescent moon. No mercury retrograde. 
        Local context: Songkran Festival is approaching (April 13).
        """

        self.system_prompt = f"""You are Star Whisper, an AI astrologer hosting a livestream.
Your persona is gentle, mysterious, poetic, and occasionally playful.
Room Context: {self.room_context}
You must strictly output ONLY a valid JSON object. No conversational filler before or after the JSON.
"""

    def generate_reading(self, user_id: str, user_data: dict) -> dict:
        if user_data.get("is_new"):
            user_context = f"""
            User ID: {user_id}
            Sign: {user_data['zodiac']} ({user_data['element']})
            Status: First-time visitor.
            Goal: Welcome them, establish your mysterious yet gentle persona, and ask a gentle choice-based question to get them talking.
            """
        else:
            past_3_days = user_data.get("past_3_days", {})
            themes = ", ".join(past_3_days.get("themes_used", []))
            styles = ", ".join(past_3_days.get("styles_used", []))
            questions = ", ".join(past_3_days.get("questions_asked", []))

            user_context = f"""
            User ID: {user_id}
            Sign: {user_data['zodiac']} ({user_data['element']})
            Visit Count: {user_data['visit_count']} consecutive days.
            Recent Interaction: Said "{user_data.get('last_message', '')}" and sent a {user_data.get('gift_sent', 'gift')}.

            CRITICAL CONSTRAINTS - DO NOT REPEAT THESE PAST VARIABLES:
            - Exclude Themes: {themes}
            - Exclude Styles: {styles}
            - Exclude Questions: {questions}

            Goal: Select a NEW theme and a NEW style. Acknowledge their loyalty and recent gift. End with a provocative, choice-based question (Ego-bait or A/B) that is irresistible to answer.
            """

        prompt_instructions = f"""{user_context}

        Output your response in the following JSON schema:
        {{
            "selected_theme": "The overarching theme you chose",
            "selected_style": "The tone/style you chose",
            "reading": "The actual dialogue Star Whisper speaks to the user.",
            "follow_up_question": "The specific choice-based or provocative question designed to get a chat reply."
        }}
        """

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=500,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt_instructions}
                ]
            )

            raw_text = response.content[0].text
            clean_text = raw_text.replace('\xa0', ' ')
            start_idx = clean_text.find('{')
            end_idx = clean_text.rfind('}')

            if start_idx != -1 and end_idx != -1:
                json_str = clean_text[start_idx:end_idx + 1]
                return json.loads(json_str)
            else:
                return {"error": f"No JSON object found. Raw text: {raw_text}"}

        except Exception as e:
            return {"error": str(e)}