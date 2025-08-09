# app/routes/generate.py
# Purpose: /api/surveys/generate with DB cache + OpenAI fallback

from flask import Blueprint, request, jsonify
from app.config.config import Config
from app.db import SessionLocal
from app.models.survey import Survey
from openai import OpenAI
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
import json
import re
import pprint

generate_bp = Blueprint("generate", __name__)
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def normalize_prompt(s: str) -> str:
    """Lowercase, trim, collapse internal whitespace for deduping."""
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

@generate_bp.route("/api/surveys/generate", methods=["POST"])
def generate_survey():
    # ---------- Input validation ----------
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    prompt = (data.get("prompt") or "").strip()
    if not (3 <= len(prompt) <= 200):
        return jsonify({"error": "prompt must be 3–200 characters"}), 400

    norm = normalize_prompt(prompt)

    # ---------- DB session per request ----------
    db = SessionLocal()
    try:
        # 1) CACHE LOOKUP
        row = db.execute(
            select(Survey).where(Survey.prompt_normalized == norm)
        ).scalar_one_or_none()

        if row:
            # Cache hit
              # Cache hit
            print("=== Loaded cached survey JSON ===")
            pprint.pprint(row.survey_json)   # <-- Add this line
            resp = jsonify(row.survey_json)
            resp.headers["X-Cached"] = "true"
            return resp, 200
           

        # 2) OPENAI CALL (cache miss)
        system = (
            "You generate professional surveys and return ONLY JSON with keys: "
            "title (string) and questions (array). Each question has: "
            "type ('multiple_choice'|'rating'|'open_text'), text (string); "
            "for multiple_choice include options (2–10 strings); "
            "for rating include scale (3–10). No extra commentary."
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Generate a survey for: {prompt}"},
        ]

        resp = client.chat.completions.create(
            model="gpt-4o-mini",                     # any available chat model
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"}, # ask for strict JSON
            # timeout can be set via client options if desired
        )

        ai_text = resp.choices[0].message.content.strip()
        print("\n=== OpenAI raw (first 400 chars) ===")
        print(ai_text[:400])

        # Parse JSON from model
        try:
            survey_json = json.loads(ai_text)
        except json.JSONDecodeError:
            return jsonify({"error": "MODEL_OUTPUT_INVALID", "raw": ai_text}), 502

        # Optional: quick schema sanity check
        if not isinstance(survey_json, dict) or "title" not in survey_json or "questions" not in survey_json:
            return jsonify({"error": "MODEL_OUTPUT_INVALID", "raw": ai_text}), 502

        # 3) SAVE TO DB
        rec = Survey(
            prompt_raw=prompt,
            prompt_normalized=norm,
            survey_json=survey_json,
        )
        db.add(rec)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # Another request inserted the same prompt first; return existing row
            existing = db.execute(
                select(Survey).where(Survey.prompt_normalized == norm)
            ).scalar_one()
            resp = jsonify(existing.survey_json)
            resp.headers["X-Cached"] = "true"
            return resp, 200

        print("=== Saved survey JSON ===")
        pprint.pprint(survey_json)

        # Return freshly generated survey
        out = jsonify(survey_json)
        out.headers["X-Cached"] = "false"
        return out, 200

    except Exception as e:
        db.rollback()
        print("DB/Service error:", repr(e))
        return jsonify({"error": "SERVER_ERROR", "details": str(e)}), 500
    finally:
        db.close()
