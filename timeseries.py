# time_series.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Define insights (revised to 5 per plot)
predefined_insights = {
    "Plot 1": [
        "Spikes in discounts (Days 9–13) may align with events like festivals, auspicious dates, or marketing campaigns.",
        "Sudden drop after peak days suggests end of limited-period offers or demand saturation post events.",
        "Steady mid to end month discounting may indicate efforts to sustain engagement or clear non premium stock.",
        "Low discounts in the first week could reflect strategy to maintain premium pricing before planned triggers.",
        "Analyzing discount trends alongside festivals like Akshaya Tritiya, wedding season can improve campaign timing and inventory planning."
    ],
    "Plot 2": [
        "Comparing sales on days with high OBDISC vs GHSDISC can help decide which type of discount works better.",
        "OBDISC changes a lot, with big jumps on days like 17, 21, and 25 — this may be due to special store offers or quick sales pushes.",
        "GHSDISC stays more steady, showing it’s part of a planned customer scheme.",
        "On days like the 31st, both discounts rise together — this might be to boost end-of-month sales.",
        "GHSDISC builds long-term loyalty, while OBDISC helps with quick sales when needed."
    ],
    "Plot 3": [
        "Monday and Thursday offer the highest average discounts (6.4%), possibly to boost early-week sales and pre-weekend interest.",
        "Tuesday and Wednesday have the lowest discounts (4.7% and 4.5%), suggesting a slow-sale strategy on midweek days.",
        "Friday to Sunday maintain steady discounts (5.8%–6.0%) to attract weekend shoppers.",
        "Higher discounts on Mondays may be used to kickstart the week with better footfall and sales.",
        "This trend can guide weekly campaign planning like more promotions on low-performing days or optimized staffing on peak days."
    ]
}

def plot_and_insight(df, plot_key, plot_label):
    df.columns = df.columns.str.strip().str.lower()
    with st.container():
        df['docdate'] = pd.to_datetime(df['docdate'], errors='coerce')
        df = df.dropna(subset=['docdate'])
        df['day'] = df['docdate'].dt.day

        if plot_key == "Plot 1":
            st.subheader("Daily Average idisc (1-Month View)")
            df_idisc = df.dropna(subset=['idisc'])
            df_idisc = df_idisc[df_idisc['idisc'] > 0]
            daily_avg = df_idisc.groupby('day')['idisc'].mean().reset_index()
            plt.figure(figsize=(12, 5))
            sns.lineplot(data=daily_avg, x='day', y='idisc', marker='o', color='teal')
            plt.title("Daily Average idisc (1-Month View)")
            plt.xlabel("Day of the Month")
            plt.ylabel("Average idisc (%)")
            plt.xticks(range(1, 32))
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()

        elif plot_key == "Plot 2":
            st.subheader("Daily Trend of OBDISC and GHSDISC")
            idisc_cols = ['obdisc', 'ghsdisc']
            df2 = df.dropna(subset=idisc_cols)
            daily_avg2 = df2.groupby('day')[idisc_cols].mean().reset_index()
            df_melted = daily_avg2.melt(id_vars='day', var_name='idisc_type', value_name='average_idisc')
            plt.figure(figsize=(12, 5))
            sns.lineplot(data=df_melted, x='day', y='average_idisc', hue='idisc_type', marker='o', palette='Dark2')
            plt.title("Daily Trend of OBDISC and GHSDISC")
            plt.xlabel("Day of Month")
            plt.ylabel("Average idisc (%)")
            plt.xticks(range(1, 32))
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()

        elif plot_key == "Plot 3":
            st.subheader("Average Discount % by Day of Week")
            df3 = df.dropna(subset=['value', 'discount'])
            df3 = df3[(df3['value'] > 0) & (df3['discount'] >= 0)]
            df3['discount_pct'] = df3['discount'] / df3['value']
            df3['day_of_week'] = df3['docdate'].dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df3['day_of_week'] = pd.Categorical(df3['day_of_week'], categories=day_order, ordered=True)
            avg_by_day = df3.groupby('day_of_week')['discount_pct'].mean().reindex(day_order)
            plt.figure(figsize=(10, 5))
            ax = sns.barplot(x=avg_by_day.index, y=avg_by_day.values, palette='Set3')
            plt.title("Average Discount % by Day of Week", fontsize=16)
            plt.ylabel("Average Discount %")
            plt.xlabel("")
            plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
            plt.xticks(rotation=30)
            plt.grid(axis='y', linestyle='--', alpha=0.4)

            # Add text labels inside bars
            for index, value in enumerate(avg_by_day.values):
                ax.text(index, value / 2, f"{value:.1%}", ha='center', va='center', fontsize=10, color='black')

            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()

        st.markdown("---")
        st.markdown("### Insights for Business Stakeholders")
        for insight in predefined_insights.get(plot_key, ["No predefined insights available."]):
            st.markdown(f"- {insight}")
