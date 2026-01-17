"""
Gemini AI Feedback Module

This module handles AI-powered feedback generation using Google's Gemini API.
It generates structured, teacher-style feedback for student assignments.

Output format (JSON):
{
  "overall_evaluation": "2–3 short sentences",
  "strengths": ["point 1", "point 2", "point 3"],
  "weaknesses": ["point 1", "point 2", "point 3"],
  "suggestions": ["point 1", "point 2", "point 3"]
}
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env explicitly from backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


def generate_ai_feedback(text):
    """
    Sends assignment text to Gemini and returns structured feedback as dict.
    Handles:
    - API key loading
    - Model selection
    - JSON-only prompting
    - Truncated output recovery
    - Brace-balanced JSON extraction
    """

    # Read API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    # Configure Gemini SDK
    genai.configure(api_key=api_key)

    # Use stable, supported model
    model = genai.GenerativeModel("models/gemini-flash-lite-latest")


    # Strict JSON-only prompt
    prompt = f"""
Return ONLY valid JSON. Keep values short. No explanations.

{{
  "overall_evaluation": "max 2 sentences",
  "strengths": ["p1","p2","p3"],
  "weaknesses": ["p1","p2","p3"],
  "suggestions": ["p1","p2","p3"]
}}

Text:
{text}
"""

    # Low temperature for deterministic formatting
    generation_config = {
    "temperature": 0.1,
    "max_output_tokens": 500
    }

    def call_model():
        return model.generate_content(prompt, generation_config=generation_config)

    def extract_json(raw_text):
        """
        Extracts a complete JSON object using balanced brace parsing.
        This handles cases where the model output is truncated or contains extra text.
        """
        start = raw_text.find("{")
        if start == -1:
            raise Exception("No JSON object found in Gemini response")

        brace_count = 0
        in_string = False
        escape = False

        for i in range(start, len(raw_text)):
            ch = raw_text[i]

            if escape:
                escape = False
                continue

            if ch == "\\":
                escape = True
                continue

            if ch == '"':
                in_string = not in_string
                continue

            if not in_string:
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        json_block = raw_text[start:i + 1]
                        return json.loads(json_block)

        raise Exception("Incomplete JSON (missing closing brace)")

    # Try once, retry once on truncation
    for attempt in range(2):
        response = call_model()
        raw_text = response.candidates[0].content.parts[0].text.strip()

        try:
            feedback = extract_json(raw_text)
            return feedback
        except Exception as e:
            if attempt == 1:
                raise Exception(f"Gemini API error: {str(e)}")

    raise Exception("Gemini API error: Unknown failure")
