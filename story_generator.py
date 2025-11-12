from http.client import responses

from dotenv import load_dotenv
load_dotenv()

import os
from google import genai

from gtts import gTTS
from io import BytesIO
api_key= os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise  ValueError("API key  not found")

client= genai.Client(api_key=api_key)


def create_advanced_prompt(style):
    # --- Base prompt ---
    base_prompt = f"""
    You are a friendly storyteller. Your job is to write a short and engaging story that is very easy to read and in easy words.

    **GOAL:**
    Write ONE story using all the images provided, in the same order.

    **REQUIREMENTS:**
    1. The story must be written in simple, modern English.
    2. Use the '{style}' genre for the story.
    3. Connect all images into one clear story with a beginning, middle, and end.
    4. Use Indian names, characters, places, and references.
    5. Include at least one detail from every image.

    **OUTPUT FORMAT:**
    - Start with a short title.
    - Write the story in **2–3 paragraphs only.**
    """

    # --- Add Style-Specific Instructions ---
    style_instruction = ""
    if style == "Morale":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction



def generate_story_from_images(images, style):

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[images,create_advanced_prompt(style)]
    )
    return  response.text




def narrate_story(story_text):
    try:
        tts= gTTS(text=story_text, lang="en", slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        return f"An unexpected error  occured during the API call"