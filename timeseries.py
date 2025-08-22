# time_series.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from ai_agent import display_insight_panel  # Groq AI integration

# === Predefined insights by plot ===
predefined_insights = {
    "Plot 1": [
        "Spikes in discounts (Days 9–13) may align with events like festivals or marketing campaigns.",
        "Sudden drop after peak days suggests end of limited-period offers or demand saturation post events.",
        "Steady mid to end month discounting may indicate efforts to sustain engagement or clear non premium stock.",
        "Low discounts in the first week could reflect strategy to maintain premium pricing before planned triggers.",
        "Analyzing discount trends alongside festivals like Akshaya Tritiya, wedding season can improve campaign timing."
    ],
    "Plot 2": [
        "Comparing sales on days with high OBDISC vs GHSDISC can help decide which type of discount works better.",
        "OBDISC changes a lot on days like 17, 21, 25 — may be due to special store offers.",
        "GHSDISC stays more steady, showing a planned customer scheme.",
        "On days like 31, both discounts rise together to boost end-of-month sales.",
        "GHSDISC builds long-term loyalty, while OBDISC helps with quick sales when needed."
    ],
    "Plot 3": [
        "Monday and Thursday offer the highest average discounts (6.4%), boosting early-week sales.",
        "Tuesday and Wednesday have lowest discounts, suggesting slow-sale strategy midweek.",
        "Friday to Sunday maintain steady discounts to attract weekend shoppers.",
        "Higher Monday discounts may kickstart the week with better footfall.",
        "Guide weekly campaign planning: promotions on low-performing days, optimize staffing on peaks."
    ],
    "Plot 4": [
        "Day 9 had the highest discount at ₹1.13 Cr, 13.96% of sales value discounted.",
        "Days 9–13 show peak discount window, daily discounts ₹89.93L–₹1.13 Cr.",
        "Day 12 saw most transactions (736) and highest total value (₹8.54 Cr).",
        "Day 13 highest discount-to-sales percentage 14.91%, avg discount/txn ₹23,118.",
        "Overall discount rates hovered 4–8%, spiking above 10% during campaigns."
    ],
    "Plot 5": [
        "Total of 420 return transactions during the month, ~13–14 per day.",
        "Return spikes on Days 13, 18, 25, 30, suggesting post-offer dissatisfaction.",
        "Tanishq had 349 returns, far more than Mia (68) and Zoya (3).",
        "Returns mostly from DIA (167), GIS (97), MCG (67), showing higher dissatisfaction in gems/diamonds.",
        "Average daily return rate low (~13) compared to peak transactions (>700), manageable returns."
    ]
}

# === Helper to format summary for AI ===
def format_summary(summary_data):
    if summary_data is None:
        return "No summary data available."
    if isinstance(summary_data, pd.DataFrame):
        summary_data = summary_data.values.tolist()
    if not isinstance(summary_data, list):
        return "Invalid summary format."
    return "\n".join([f"• {' — '.join(map(str, row))}" for row in summary_data])

# === Main function for plotting and insights ===
def plot_and_insight(df, plot_key, plot_label=""):
    df.columns = df.columns.str.strip().str.lower()
    df['docdate'] = pd.to_datetime(df['docdate'], errors='coerce')
    df = df.dropna(subset=['docdate'])
    df['day'] = df['docdate'].dt.day

    summary_df = None  # Initialize summary_df for AI panel

    # ---------------- PLOT 1: Daily Avg idisc % ----------------
    if plot_key == "Plot 1":
        st.subheader("Daily Average idisc % (1-Month View)")
        df_idisc = df.dropna(subset=['idisc', 'value'])
        df_idisc = df_idisc[(df_idisc['idisc'] > 0) & (df_idisc['value'] > 0)]
        df_idisc['idisc_pct'] = (df_idisc['idisc'] / df_idisc['value']) * 100
        daily_avg = df_idisc.groupby('day')['idisc_pct'].mean().reset_index()
        plt.figure(figsize=(12, 5))
        sns.lineplot(data=daily_avg, x='day', y='idisc_pct', marker='o', color='teal')
        plt.title("Daily Average idisc % (1-Month View)")
        plt.xlabel("Day of the Month")
        plt.ylabel("Average idisc (%)")
        plt.xticks(range(1, 32))
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

        # Summary table
        df_idisc['brand'] = df_idisc['brand'].str.upper()
        df_idisc['region'] = df_idisc['region'].str.upper()
        daily_avg = df_idisc.groupby('day')['idisc_pct'].mean()
        top_discount_day = daily_avg.idxmax()
        peak_discount_value = daily_avg.max()
        brand_avg = df_idisc.groupby('brand')['idisc_pct'].mean()
        most_discounted_brand = brand_avg.idxmax()
        brand_discount_value = brand_avg.max()
        region_avg = df_idisc.groupby('region')['idisc_pct'].mean()
        underperforming_region = region_avg.idxmin()
        underperforming_region_val = region_avg.min()
        high_discount_days = df_idisc[df_idisc['idisc_pct'] > 10]['day'].value_counts()
        most_frequent_high_discount_day = high_discount_days.idxmax()
        total_high_discount_days = high_discount_days.count()
        total_bills = df_idisc.shape[0]
        summary_data = {
            "Insight Area": [
                "Peak Discount Day",
                "Peak Discount % on That Day",
                "Most Discounted Brand",
                "Avg Discount % for That Brand",
                "Region with Least Discount Focus",
                "Avg Discount % in That Region",
                "Most Frequent High Discount Day (10% >)",
                "Total Days with High Discounts (10% >)",
            ],
            "Value": [
                int(top_discount_day),
                f"{peak_discount_value:.2f}%",
                most_discounted_brand,
                f"{brand_discount_value:.2f}%",
                underperforming_region,
                f"{underperforming_region_val:.2f}%",
                int(most_frequent_high_discount_day),
                int(total_high_discount_days)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        st.markdown("### Discount Summary Insights (Based on idisc %)")
        st.dataframe(summary_df, use_container_width=True)

    # ---------------- PLOT 2: OBDISC & GHSDISC ----------------
    elif plot_key == "Plot 2":
        st.subheader("Daily Trend of OBDISC and GHSDISC (as % of Bill Value)")
        idisc_cols = ['obdisc', 'ghsdisc']
        df2 = df.dropna(subset=idisc_cols + ['value'])
        df2 = df2[df2['value'] > 0]
        df2['obdisc_pct'] = (df2['obdisc'] / df2['value']) * 100
        df2['ghsdisc_pct'] = (df2['ghsdisc'] / df2['value']) * 100
        df2 = df2[(df2['obdisc_pct'] >= 0) & (df2['ghsdisc_pct'] >= 0)]
        df2['day'] = df2['docdate'].dt.day
        daily_avg2 = df2.groupby('day')[['obdisc_pct', 'ghsdisc_pct']].mean().reset_index()
        df_melted = daily_avg2.melt(id_vars='day', var_name='idisc_type', value_name='average_discount_pct')
        plt.figure(figsize=(14, 6))
        sns.lineplot(data=df_melted, x='day', y='average_discount_pct', hue='idisc_type', marker='o', palette='Dark2')
        plt.title("Daily Trend of OBDISC and GHSDISC (%)")
        plt.xlabel("Day of Month")
        plt.ylabel("Average Discount (%)")
        plt.xticks(range(1, 32))
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

        # Summary table
        summary_data = {
            "Discount Type": [], "Average Discount (%)": [], "Highest Daily Average (%)": [],
            "Lowest Daily Average (%)": [], "Day with Highest Avg Discount": [], "Day with Lowest Avg Discount": []
        }
        for col in ['obdisc_pct', 'ghsdisc_pct']:
            avg = daily_avg2[col].mean()
            max_val = daily_avg2[col].max()
            min_val = daily_avg2[col].min()
            max_day = daily_avg2.loc[daily_avg2[col].idxmax(), 'day']
            min_day = daily_avg2.loc[daily_avg2[col].idxmin(), 'day']
            summary_data["Discount Type"].append("OBDISC" if "obdisc" in col else "GHSDISC")
            summary_data["Average Discount (%)"].append(f"{avg:.2f}")
            summary_data["Highest Daily Average (%)"].append(f"{max_val:.2f}")
            summary_data["Lowest Daily Average (%)"].append(f"{min_val:.2f}")
            summary_data["Day with Highest Avg Discount"].append(int(max_day))
            summary_data["Day with Lowest Avg Discount"].append(int(min_day))
        summary_df = pd.DataFrame(summary_data)
        st.write("**Key Insights from OBDISC and GHSDISC (Daily Averages as % of Bill Value)**")
        st.dataframe(summary_df, use_container_width=True)

    # ---------------- PLOT 3: Avg Discount by Day of Week ----------------
    elif plot_key == "Plot 3":
        st.subheader("Average Discount % by Day of Week")
        df3 = df.dropna(subset=['value', 'discount'])
        df3 = df3[(df3['value'] > 0) & (df3['discount'] >= 0)]
        df3['discount_pct'] = df3['discount'] / df3['value']
        df3['day_of_week'] = df3['docdate'].dt.day_name()
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        df3['day_of_week'] = pd.Categorical(df3['day_of_week'], categories=day_order, ordered=True)
        avg_by_day = df3.groupby('day_of_week')['discount_pct'].mean().reindex(day_order)
        plt.figure(figsize=(10,5))
        ax = sns.barplot(x=avg_by_day.index, y=avg_by_day.values, palette='Set3')
        plt.title("Average Discount % by Day of Week")
        plt.ylabel("Average Discount %")
        plt.xlabel("")
        plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
        plt.xticks(rotation=30)
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        for idx, val in enumerate(avg_by_day.values):
            ax.text(idx, val/2, f"{val:.1%}", ha='center', va='center', fontsize=10, color='black')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

        # Summary table
        summary_df = df3.groupby('day_of_week')['discount_pct'].agg(
            Avg_Discount_Percentage='mean',
            Transaction_Count='count'
        ).reindex(day_order).reset_index()
        summary_df['Day_Type'] = summary_df['day_of_week'].apply(
            lambda x: 'Weekday' if x in day_order[:5] else 'Weekend'
        )
        summary_df['Avg_Discount_Percentage'] = (summary_df['Avg_Discount_Percentage']*100).round(2)
        st.markdown("**Day wise Discount Summary**")
        st.dataframe(summary_df.rename(columns={'day_of_week':'Day','Avg_Discount_Percentage':'Avg Discount %','Transaction_Count':'Txn Count'}), use_container_width=True)

    # -----------------OLOT 4-------------
    elif plot_key == "Plot 4":
        st.subheader("Daily Discount Trend (%): Tanishq vs Mia, Zoya & Ecom")

        df['docdate'] = pd.to_datetime(df['docdate'], errors='coerce')
        df['brand'] = df['brand'].str.upper()
        df['day'] = df['docdate'].dt.day

        df_valid = df[(df['discount'] > 0) & (df['value'] > 0)].copy()
        if df_valid.empty:
            st.warning("No valid discount data available for plotting.")
        else:
            df_valid['discount_pct'] = (df_valid['discount'] / df_valid['value']) * 100
            df_valid = df_valid[df_valid['discount_pct'] <= 100]

            df_tanishq = df_valid[df_valid['brand'] == 'TANISHQ']
            df_other = df_valid[df_valid['brand'] != 'TANISHQ']

            fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

            if not df_tanishq.empty:
                daily_discount_tanishq = df_tanishq.groupby('day')['discount_pct'].mean().reset_index()
                sns.lineplot(
                    data=daily_discount_tanishq,
                    x='day',
                    y='discount_pct',
                    marker='o',
                    color='goldenrod',
                    ax=axs[0]
                )
            axs[0].set_title("Tanishq - Daily Avg Discount (%)")
            axs[0].set_ylabel("Avg Discount (%)")
            axs[0].grid(True)

            if not df_other.empty:
                daily_discount_other = df_other.groupby(['day', 'brand'])['discount_pct'].mean().reset_index()
                sns.lineplot(
                    data=daily_discount_other,
                    x='day',
                    y='discount_pct',
                    hue='brand',
                    marker='o',
                    palette='tab10',
                    ax=axs[1]
                )
            axs[1].set_title("Mia, Zoya & Ecom - Daily Avg Discount (%)")
            axs[1].set_xlabel("Day of Month")
            axs[1].set_ylabel("Avg Discount (%)")
            axs[1].grid(True)
            axs[1].set_xticks(range(1, 32))

            plt.tight_layout()
            st.pyplot(fig)
            plt.clf()

            # Summary Table
            summary_data = []
            for brand, group in df_valid.groupby('brand'):
                avg_disc = round(group['discount_pct'].mean(), 2)
                total_txn = len(group)
                summary_data.append({
                    "Brand": brand,
                    "Avg Discount (%)": avg_disc,
                    "Total Transactions": total_txn
                })
            summary_df = pd.DataFrame(summary_data)
            st.write("**Daily Discount Summary by Brand**")
            st.dataframe(summary_df.sort_values(by="Avg Discount (%)", ascending=False), use_container_width=True)



    # ---------------- PLOT 5: Returns ----------------
    elif plot_key == "Plot 5":
        st.subheader("Daily Returned Transactions (Day 1–31)")
        df_return = df.copy()
        df_return['is_returned'] = (df_return['qty']<0) | (df_return['value']<0)
        returned_df = df_return[df_return['is_returned']].copy()
        returned_df['day'] = returned_df['docdate'].dt.day
        daily_returns = returned_df.groupby('day').size().reset_index(name='Return Count')
        all_days = pd.DataFrame({'day':range(1,32)})
        daily_returns = all_days.merge(daily_returns,on='day',how='left').fillna(0)
        plt.figure(figsize=(12,5))
        sns.lineplot(data=daily_returns, x='day', y='Return Count', marker='o', linewidth=2, color='crimson')
        plt.title("Returned Transactions per Day (1–31)")
        plt.xlabel("Day of Month")
        plt.ylabel("Return Count")
        plt.xticks(range(1,32))
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

        # Summary table
        summary_data = {
            "Metric": [
                "Total Returned Transactions",
                "Average Discount on Returned Items (₹)"
            ],
            "Value": [
                len(returned_df),
                round(returned_df['discount'].mean(),2) if not returned_df.empty else 0
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        st.write("**Return Metrics Summary**")
        st.dataframe(summary_df, use_container_width=True)

    # ---------------- AI Insight Panel ----------------
    if summary_df is not None and not summary_df.empty:
        col_insights = predefined_insights.get(plot_key, [f"No insights available for {plot_key}."])
        display_insight_panel(
            x_col=plot_key,
            predefined_insights={plot_key: col_insights},
            summary_df=summary_df
        )
