import os
from dotenv import load_dotenv
from openai import OpenAI
import traceback

# -----------------------------------------------------------
# Load .env from project root
# -----------------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    print(f"✅ Loaded .env from: {ENV_PATH}")
else:
    print(f"❌ .env not found at: {ENV_PATH}")

# -----------------------------------------------------------
# Initialize OpenRouter Client
# -----------------------------------------------------------
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("❌ ERROR: OPENROUTER_API_KEY not found in .env.")
else:
    print("🔑 OpenRouter API key loaded successfully (starts with):", api_key[:10], "...")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
except Exception as e:
    print("❌ Failed to initialize OpenRouter client:", e)
    traceback.print_exc()

# -----------------------------------------------------------
# AI Resume Feedback (DeepSeek V3.1)
# -----------------------------------------------------------
def ai_resume_feedback(resume_text, role=None, model="deepseek/deepseek-chat"):
    """
    Generates AI-powered resume insights using DeepSeek V3.1 via OpenRouter.
    """
    try:
        prompt = f"""
        You are an experienced career coach and technical resume expert.

        Analyze the following resume and provide:
        1. A concise 3-line professional summary of the candidate.
        2. The top 5 technical or soft skills identified.
        3. 3 strengths and 3 improvement suggestions.
        4. {f"How well does this resume match the role '{role}'?" if role else ""}
        5. Give a total match percentage (0–100).

        Resume:
        {resume_text[:4000]}
        """

        response = client.chat.completions.create(
            model=model,  # ✅ DeepSeek V3.1
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.6,
        )

        feedback = response.choices[0].message.content.strip()
        print(f"✅ AI feedback generated successfully using {model}")
        return feedback

    except Exception as e:
        print(f"❌ [ERROR] DeepSeek V3.1 feedback failed: {e}")
        traceback.print_exc()
        return None
