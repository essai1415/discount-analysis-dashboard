import streamlit as st
from groq import Groq
import pandas as pd
import random

# === Groq API Setup ===
groq_api_key = st.secrets["groq"]
client = Groq(api_key=groq_api_key)

# === Main Insight Panel Function ===
import streamlit as st
from groq import Groq
import pandas as pd
import re

# === Groq API Setup ===
groq_api_key = st.secrets["groq_api_key"]
client = Groq(api_key=groq_api_key)

def display_insight_panel(x_col, predefined_insights, summary_df, model="llama3-70b-8192"):
    if not predefined_insights:
        return

    x_col = next(iter(predefined_insights))
    insights_list = predefined_insights[x_col]
    summary_text = format_summary(summary_df)
    full_insight_text = "\n".join(insights_list)

    # === First Toggle: Business Insights ===
    toggle_key_1 = f"toggle_insights_{x_col}"
    if toggle_key_1 not in st.session_state:
        st.session_state[toggle_key_1] = False

    def toggle_insights():
        st.session_state[toggle_key_1] = not st.session_state[toggle_key_1]

    st.button(
        "Hide Detailed Business Insights" if st.session_state[toggle_key_1] else "Show Detailed Business Insights",
        key=f"btn_insights_{x_col}",
        on_click=toggle_insights,
    )

    if st.session_state[toggle_key_1]:
        st.markdown("###  Key Business Insights")
        for insight in insights_list:
            st.markdown(f"- {insight}")
        st.markdown("---")

    # === Second Toggle: AI Recommendation ===
    toggle_key_2 = f"toggle_ai_{x_col}"
    if toggle_key_2 not in st.session_state:
        st.session_state[toggle_key_2] = False

    def toggle_ai():
        st.session_state[toggle_key_2] = not st.session_state[toggle_key_2]

    st.button(
        "Hide AI Powered Strategic Action" if st.session_state[toggle_key_2] else "Reveal AI Powered Strategic Action",
        key=f"btn_ai_{x_col}",
        on_click=toggle_ai,
    )

    if not st.session_state[toggle_key_2]:
        return

    # === AI Recommendation Generation ===
    rec_key = f"ai_recommendation_{x_col}"
    if rec_key not in st.session_state:
        st.session_state[rec_key] = None

    if st.session_state[rec_key] is None:
        prompt = f"""
        You are a senior business analyst AI.

        Given these insights and summary:

        INSIGHTS:
        \"\"\"{full_insight_text}\"\"\"

        SUMMARY:
        \"\"\"{summary_text}\"\"\"

        Respond with:
        Action: <Clear action in 1–2 lines>
        Reason: <Why it matters>
        Urgency: <Low / Medium / High>
        Only include those 3 labeled fields.
        """
        try:
            with st.spinner(" Thinking about recommended action..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    temperature=0.5,
                    max_tokens=300,
                )
                st.session_state[rec_key] = response.choices[0].message.content.strip()
        except Exception as e:
            st.session_state[rec_key] = f"⚠️ AI failed: {e}"

    st.markdown("###  AI Suggested Action Plan")

    response_text = st.session_state[rec_key]
    action = re.search(r"(?i)Action:\s*(.+?)(?:\n|$)", response_text, re.DOTALL)
    reason = re.search(r"(?i)Reason:\s*(.+?)(?:\n|$)", response_text, re.DOTALL)
    urgency = re.search(r"(?i)Urgency:\s*(.+?)(?:\n|$)", response_text, re.DOTALL)

    if action:
        st.markdown(f"**Immediate Action:** {action.group(1).replace('**', '').strip()}")
    if reason:
        st.markdown(f"**Reason:** {reason.group(1).replace('**', '').strip()}")
    if urgency:
        st.markdown(f"**Urgency:** {urgency.group(1).replace('**', '').strip()}")
    if not any([action, reason, urgency]):
        st.markdown(response_text)

    st.markdown("---")

    # === Follow-up Question Section ===
    st.markdown("#### 🤖 Ask a follow-up question:")
    followup = st.text_input(f"Ask anything about the insights:", key=f"followup_{x_col}")

    if followup:
        followup_prompt = f"""
        You are a senior business consultant.

        User asked: "{followup}"

        Context Insights:
        \"\"\"{full_insight_text}\"\"\"

        Summary Table:
        \"\"\"{summary_text}\"\"\"

        Give a concise, precise, very short, helpful and practical answer in simple business terms.
        Structure your response as bullet points for clarity.
        """
        try:
            with st.spinner("AI answering..."):
                followup_response = client.chat.completions.create(
                    messages=[{"role": "user", "content": followup_prompt}],
                    model=model,
                    temperature=0.6,
                    max_tokens=400,
                )
                st.info("AI Says:")
                response_text = followup_response.choices[0].message.content.strip()
                lines = response_text.split("•")

                first_line = lines[0].strip()
                if first_line and not first_line.startswith("-"):
                    st.markdown(first_line)

                for line in lines[1:]:
                    cleaned = line.strip()
                    if cleaned:
                        st.markdown(f"- {cleaned}")

        except Exception as e:
            st.error(f"⚠️ Failed to answer: {e}")

# === Format Summary Helper ===
def format_summary(summary_data):
    if summary_data is None:
        return "No summary data available."
    if isinstance(summary_data, pd.DataFrame):
        summary_data = summary_data.values.tolist()
    if not isinstance(summary_data, list):
        return "Invalid summary format."
    return "\n".join([f"• {' — '.join(map(str, row))}" for row in summary_data])



