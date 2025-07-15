import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# --- Predefined insights ---
predefined_insights = {
    "brand": [
        "Zoya offers the highest average discounts, suggesting an aggressive promotional strategy that should be evaluated for its impact on customer acquisition and profit margins.",
        "Tanishq maintains moderate discount levels, suggesting a balanced pricing approach aimed at the mass market.",
        "Mia provide minimal discounts, which could reflect a limited promotional reach",
        "The discount gap across brands is quite large, so aligning each brand’s strategy with its target audience can create a more consistent customer experience.",
        "Avoid over-discounting premium brands to protect brand value."
    ],
    "region": [
        "North 3 and South 3 regions receive the highest average discounts.",
        "Mid-performing regions like North 4, West 2, West 3 and South 1 show moderate discounting.",
        "Regions such as East 1, North 2, and East 2 are on the lower end.",
        "South and East 2 (duplicate label) show extremely low discounts.",
        "Monitor margin impact in high-discount regions."
    ],
    "level": [
        "L1 offer the highest discounts, indicating strong in-house promotional efforts to drive direct sales.",
        "L2  offer mid-level discounts, which shows moderate control, fine tuning their targets could increase efficiency.",
        "L3 stores offer minimal discounts, which could hinder customer attraction.",
        "The sharp discount drop from L1 to L3 risks inconsistent customer experience.",
        "Balancing discount policies across channels will help improve customer experience and ensure all store types contribute effectively to growth."
    ],
    "rcluster": [
        "Studded jewellery receives the highest discounts, indicating it's a key category for driving sales",
        "Plain gold jewellery gets moderate discounts, showing balanced pricing.",
        "Coins receive low discounts, possibly due to lower margins or stable demand.",
        "Silver products get minimal discounts, which may reduce their visibility.",
        "The wide discount gap across clusters suggests a need to reassess whether current discount strategies align with sales goals and customer expectations."
    ],
    "totcategory": [
        "Ssc and Ssb receive the highest discounts, showing they are the primary focus of promotional efforts.",
        "Ssa and Dia get moderate discounts, indicating potential under promotion & consider testing higher discounts to lift their performance.",
        "Mid-tier categories like Hcg, Gis, and Mcg show lower discounts, and may benefit from limited-time offers to stimulate interest.",
        "Categories like Coi, Lcg, Puc, and Sil receive minimal discounts, which could result in low visibility and stagnant inventory, review their sales trends and revise discount strategy.",
        "Reassess the discount allocation strategy, ensuring it reflects each category’s contribution to revenue, stock levels, and customer demand patterns."
    ],
    "amcb": [
        "Higher AMCB bands (like F: 30%+) receive the highest discounts, indicating heavy discounting on high making charge products.",
        "Discounts rise steadily with AMCB, suggesting products with higher making charges are being rewarded.",
        "Lower bands (A to C: 1–18%) get minimal discounts, which may limit their movement.",
        "The discount gap between low and high bands is significant, possibly creating a value mismatch in the eyes of price sensitive customers.",
        "Optimizing discounts across AMCB bands can help balance margin protection."
    ],
    "priceband": [
        "O (₹20L+) receives the highest average discount, indicating heavy promotions for ultra-premium purchases.",
        "Discounts steadily increase with price, peaking in high-value bands (M, N, O), reflecting a strategy to attract elite buyers.",
        "Mid-tier bands like D (₹1–2L) and E (₹2–3L) get moderate discounts, showing a balance between volume and value.",
        "Entry-level bands A to C (₹0–1L) have the lowest discounts, possibly due to lower margins or strong baseline demand.",
        "Consider evaluating ROI from top-tier discounts to ensure profitability which aligns with premium customer conversions."
    ],
    "day": [
        "The 9th and 13th show peak discount spikes, marking them as strong candidates for future high-impact campaigns.",
        "Early month (1st–7th) sees consistently low discounts, suggesting limited engagement, consider boosting early month offers.",
        "Discounts stabilize mid-month (15th–25th), which may indicate a routine strategy, experiment with flash sales to drive momentum.",
        "The sharp dip after the 13th hints at untapped days, where timely promotions could maintain customer interest and conversions.",
        "Use these daily patterns to optimize calendar planning, ensuring peak days align with customer buying behavior."
    ]
}

# --- Reusable plotting and insight function ---
def plot_and_insight(df_plot, x_col, x_label, chart_type="bar", category_order=None):
    with st.container():
        # Only create plot if it's not the docdate/day line chart (those are handled in main.py)
        skip_plot = chart_type == "line" and x_col in ["day", "docdate"]

        if not skip_plot:
            fig, ax = plt.subplots(figsize=(10, 5))

            if chart_type == "bar":
                if category_order:
                    df_plot[x_col] = pd.Categorical(df_plot[x_col], categories=category_order, ordered=True)
                sns.barplot(data=df_plot, x=x_col, y='discount', palette='Set2', ax=ax)
                ax.set(title=f"{x_label} vs Discount", xlabel=x_label, ylabel="Average Discount")
                plt.xticks(rotation=45)

            elif chart_type == "line":
                sns.lineplot(data=df_plot, x=x_col, y='discount', color='orangered', ax=ax)
                ax.set(title=f"{x_label} Trend", xlabel=x_label, ylabel="Average Discount")

            elif chart_type == "box":
                sns.boxplot(data=df_plot, x=x_col, y='discount', palette='Set2', ax=ax)
                ax.set(title=f"Discount by {x_label}", xlabel=x_label, ylabel="Discount")
                plt.xticks(rotation=45)

            st.pyplot(fig)

        # Insights (always shown)
        st.markdown("### Business Insights For Stakeholders")
        for insight in predefined_insights.get(x_col, [f"No insights available for {x_label}."]):
            st.markdown(f"- {insight}")
