import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.graph_objects as go

from backend.extract import extract_text
from backend.analyze import extract_email, extract_skills, recommend_role, calculate_score
from backend.ai_helper import ai_resume_feedback  # ✅ DeepSeek V3.1 integration

# -----------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

# -----------------------------------------------------------
# Header
# -----------------------------------------------------------
st.title("🤖 AI Resume Analyzer")
st.markdown(
    """
    Upload your **PDF** or **Word (.docx)** resume below,  
    and get instant insights — detected skills, role match, AI feedback, and visual analytics.
    """
)
st.divider()

# -----------------------------------------------------------
# File Uploader
# -----------------------------------------------------------
uploaded = st.file_uploader("📂 Upload your Resume File", type=["pdf", "docx"])

# -----------------------------------------------------------
# Resume Analysis Logic
# -----------------------------------------------------------
if uploaded:
    file_path = f"temp_{uploaded.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded.read())

    with st.spinner("🔍 Extracting and analyzing your resume... Please wait."):
        try:
            # Extract + Analyze
            text = extract_text(file_path)
            email = extract_email(text)
            skills = extract_skills(text)
            role, role_score = recommend_role(skills)
            score = calculate_score(email, skills, role_score)

            st.success("✅ Resume analysis completed successfully!")

            # -----------------------------------------------------------
            # Display Results
            # -----------------------------------------------------------
            st.subheader("📋 Resume Summary")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**📧 Email:** `{email or 'Not Found'}`")
                st.markdown(f"**💼 Recommended Role:** `{role or 'N/A'}`")
                st.markdown(f"**⭐ Resume Score:** `{score}/100`")

            with col2:
                st.markdown("**🧠 Skills Detected:**")
                st.write(", ".join(skills) if skills else "No skills found.")

            st.divider()
            st.markdown("## 📊 Dashboard Insights")

            # -----------------------------------------------------------
            # 1️⃣ Resume Score Gauge (Plotly)
            # -----------------------------------------------------------
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Resume Strength"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#00B4D8"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccc"},
                            {'range': [50, 80], 'color': "#fff3cd"},
                            {'range': [80, 100], 'color': "#d4edda"},
                        ],
                    },
                )
            )
            st.plotly_chart(gauge, width="stretch")

            # -----------------------------------------------------------
            # 2️⃣ Role Relevance Visualization
            # -----------------------------------------------------------
            st.markdown("### 🧭 Role Match Overview")
            if role:
                if role_score >= 4:
                    st.success(f"🎯 Excellent match for **{role}** role!")
                elif role_score >= 2:
                    st.warning(f"⚡ Partial match for **{role}** — add more relevant skills.")
                else:
                    st.error(f"🧩 Weak match for **{role}** — consider tailoring your resume.")
            else:
                st.info("No strong role match found.")

            # -----------------------------------------------------------
            # 3️⃣ AI-Powered Resume Insights (DeepSeek V3.1)
            # -----------------------------------------------------------
            st.divider()
            st.markdown("## 🤖 AI Resume Insights (Powered by DeepSeek V3.1)")

            use_ai = st.toggle("Enable AI feedback", value=True)

            if use_ai:
                with st.spinner("🤖 Generating AI resume insights via DeepSeek V3.1... please wait..."):
                    ai_feedback = ai_resume_feedback(text, role)

                if ai_feedback:
                    st.success("✅ AI feedback generated successfully using DeepSeek V3.1")
                    st.markdown(ai_feedback)
                else:
                    st.warning("⚠️ Unable to generate AI feedback. Please check your API key or try again later.")

            # -----------------------------------------------------------
            # 4️⃣ Next Steps
            # -----------------------------------------------------------
            st.divider()
            st.markdown("### 💡 Next Steps to Improve Your Resume")
            st.markdown(
                """
                ✅ Add missing technical or role-specific skills  
                ✅ Quantify achievements with measurable metrics  
                ✅ Tailor your resume for the target job title  
                ✅ Maintain a consistent, clean layout  
                ✅ Use strong action verbs like *developed*, *led*, *optimized*
                """
            )

        except Exception as e:
            st.error(f"❌ An error occurred while analyzing your resume: {e}")

else:
    st.info("👆 Please upload a `.pdf` or `.docx` resume to get started.")
