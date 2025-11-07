import re
import spacy
import pandas as pd
import json
import os
import sys

# -----------------------------------------------------------
# Load spaCy model safely
# -----------------------------------------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("[INFO] spaCy model 'en_core_web_sm' not found. Installing...")
    os.system(f"{sys.executable} -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# -----------------------------------------------------------
# Email Extraction (clean + robust)
# -----------------------------------------------------------
def extract_email(text: str):
    """
    Extracts the most probable email address from messy PDF text.
    Handles:
      - extra characters (India, mailto, etc.)
      - duplication errors from PDFs
      - line breaks, spaces, or special symbols
    """
    try:
        if not text or not isinstance(text, str):
            return None

        # Step 1: Normalize & clean
        clean_text = re.sub(r"[^A-Za-z0-9@._%+\-\s]", " ", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        # Step 2: Find all possible email-like patterns
        candidates = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", clean_text
        )
        if not candidates:
            return None

        filtered = []
        for mail in candidates:
            mail = mail.lower().strip()

            # Skip fake or irrelevant addresses
            if any(bad in mail for bad in ["example@", "support@", "help@", "service@", "test@"]):
                continue

            # Fix common decode issues (e.g., gmailcom → gmail.com)
            mail = re.sub(r"gmail(\b|$)", "gmail.com", mail)
            mail = mail.replace("gmaillcom", "gmail.com").replace("gmaiicom", "gmail.com")

            # Remove accidental prefixes (like "india" or "email")
            mail = re.sub(r"^(india|email|mail|www)\.?", "", mail)

            filtered.append(mail)

        if not filtered:
            return None

        probable_email = filtered[0]

        # Step 3: Handle duplicated fragments (e.g., yadagirinagakoushiknagakoushikyadagiri1@gmail.com)
        local_part, _, domain = probable_email.partition("@")

        if len(local_part) > 15:
            for size in range(4, 8):  # chunk size
                chunks = [local_part[i:i+size] for i in range(0, len(local_part), size)]
                if len(chunks) > 2:
                    half = len(chunks) // 2
                    first_half = "".join(chunks[:half])
                    second_half = "".join(chunks[half:])
                    if first_half in second_half:
                        local_part = "".join(chunks[half:])
                        break

        cleaned_email = f"{local_part}@{domain}"

        # Step 4: Final regex validation
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", cleaned_email):
            return None

        return cleaned_email.strip().lower()

    except Exception as e:
        print(f"[ERROR] extract_email: {e}")
        return None


# -----------------------------------------------------------
# Skill Extraction (safe + file path aware)
# -----------------------------------------------------------
def extract_skills(text):
    """
    Extracts recognized skills from resume text based on data/skills.csv.
    """
    try:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "skills.csv"))
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Skills file not found at: {data_path}")

        df = pd.read_csv(data_path)
        skills = df["Skill"].dropna().tolist()

        found = [s for s in skills if s.lower() in text.lower()]
        return sorted(list(set(found)))  # unique + sorted

    except Exception as e:
        print(f"[ERROR] extract_skills: {e}")
        return []


# -----------------------------------------------------------
# Role Recommendation (Weighted logic)
# -----------------------------------------------------------
def recommend_role(skills):
    """
    Determines the most relevant job role based on skill overlap.
    Uses percentage matching with fallback to top match.
    """
    try:
        role_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "job_roles.json"))
        if not os.path.exists(role_path):
            raise FileNotFoundError(f"Job roles file not found at: {role_path}")

        with open(role_path, "r", encoding="utf-8") as f:
            roles = json.load(f)

        best_role, best_match = None, 0
        role_match_percentage = {}

        for role, req_skills in roles.items():
            if not req_skills:
                continue
            matched = len(set(s.lower() for s in skills) & set(r.lower() for r in req_skills))
            total = len(req_skills)
            match_percent = round((matched / total) * 100, 2)
            role_match_percentage[role] = match_percent

            if match_percent > best_match:
                best_role = role
                best_match = match_percent

        return best_role, best_match

    except Exception as e:
        print(f"[ERROR] recommend_role: {e}")
        return None, 0


# -----------------------------------------------------------
# Resume Scoring Logic (Weighted)
# -----------------------------------------------------------
def calculate_score(email, skills, role_score):
    """
    Calculates resume score (0–100) based on:
      - Email presence (10)
      - Skills detected (max 50)
      - Role match percentage (max 40)
    """
    try:
        score = 0
        if email:
            score += 10
        score += min(50, len(skills) * 2)
        score += min(40, int(role_score * 0.4))
        return min(score, 100)
    except Exception as e:
        print(f"[ERROR] calculate_score: {e}")
        return 0
