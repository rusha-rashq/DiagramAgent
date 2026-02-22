import json
import os
import re

from dotenv import load_dotenv
from google import genai

from ir_schema import DiagramIR

load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a diagram generation agent.

Return ONLY valid JSON.
No markdown.
No explanations.

Structure:
{
  "nodes": [{"id": "...", "label": "...", "type": "..."}],
  "edges": [{"source": "...", "target": "..."}]
}
"""


def generate_diagram(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=SYSTEM_PROMPT + "\nUser request: " + prompt,
    )
    return response.text.strip()


def clean_json(text: str):
    text = text.strip()

    # Remove triple backticks with optional language tag
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"```$", "", text)

    return json.loads(text.strip())


if __name__ == "__main__":
    user_prompt = input("Describe your diagram: ")

    raw_output = generate_diagram(user_prompt)
    print("\nRaw LLM Output:\n", raw_output)

    try:
        parsed = clean_json(raw_output)
        validated = DiagramIR(**parsed)
        print("\nValidated JSON IR:\n", validated)
    except Exception as e:
        print("\nValidation Error:", e)
