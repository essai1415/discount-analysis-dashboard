# multivariate.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define insights (revised to 5 per plot)
predefined_insights = {
    "Plot 1": [
        "The highest discount value was offered at RJH on 2025-01-16, indicating a possible major event or high-value purchase.",
        "Locations like VRR, UDI, and TPP show consistently high discounts, useful for identifying high performing or high competition zones for future campaigns and inventory planning.",
        "Locations at the bottom of the list gave lower total discounts — possibly due to less footfall, fewer high-value transactions, or tighter pricing.",
        "Regional trends in discounting can help tailor offers based on local demand and sales performance.",
        "Repeating high-discount dates across multiple locations (e.g., Jan 13) suggests a pan-location campaign or festival-linked offer.",
        "Monitoring high-discount branches ensures profitability is not compromised while supporting sales growth."
    ],
    "Plot 2": [
        "Products without discounts have a much higher return rate (15.1%) compared to those with discounts (4.2%).",
        "Discounted purchases are more likely to be final, suggesting higher customer satisfaction.",
        "Offering discounts may help reduce returns and improve customer retention.",
        "Non-discounted items may be returned due to price sensitivity, mismatch with expectations, or uncertain purchase decisions.",
        "These insights support using targeted discounts to drive quality sales and minimize returns."
    ],
    "Plot 3": [
        "Existing customers receive a higher average discount (3.91%) compared to new customers (2.48%).",
        "This suggests a loyalty-based discount strategy to retain and reward repeat buyers.",
        "New customers get smaller discounts, possibly to keep profits steady.",
        "Offering slightly higher first-time discounts could help boost new customer acquisition.",
        "The trend supports the idea that building long-term relationships is prioritized over short-term conversions."
    ],
    "Plot 4": [
        "The chart compares daily average discount (blue) with gold price (orange) over the month.",
        "There is no strong direct link, high gold prices don’t always result in higher discounts.",
        "On days like 11 to 13, both discount and gold price were high likely to balance cost and keep customers interested.",
        "On days like Day 3, gold price shot up but discount stayed low possibly to protect profit margins.",
        "Tracking these trends helps decide whether to adjust discounts based on gold price changes to keep sales stable."
    ],
    "Plot 5": [
        "Plot 1: Overall Discount (discount): Strongly linked to stone value, total value, and making charges, showing higher discounts on premium, ornate items.",
        "Plot 2: Item Level Discount (idisc): Closely mirrors overall discount pattern, confirming it drives most of the total discount.",
        "Plot 3: Other Bill Discount (obdisc): Weakly correlated, suggesting it’s used for on demand or bill level adjustments.",
        "Plot 4: Gold Harvest Scheme Discount (ghsdisc): Has minimal correlation with transaction features, indicating it's likely applied uniformly or scheme based."
    ],
    "Plot 6": [
        "A few customers receive very high average discounts, likely due to premium or bulk jewelry purchases.",
        "These top customers may be considered for exclusive loyalty programs or profitability reviews.",
        "Understanding discount trends by customer helps tailor future offers based on actual purchase behavior.",
        "This analysis can guide sales teams to focus on high-potential customers while avoiding unnecessary discount leakage.",
        "Tracking high-discount customers aids in balancing competitive offers with margin preservation."
    ],
    "Plot 7": [
        "Zoya in West 3 gives the highest average discounts, which may indicate over-discounting or aggressive promotion.",
        "Discount patterns differ across regions, suggesting the need for region-specific pricing strategies.",
        "Mia and Tanishq offer moderate to low discounts, showing relatively tighter discount control.",
        "East and North regions show more consistent discounting across all brands.",
        "This chart reveals how each brand performs across regions, helping optimize discount strategies by brand and geography."
    ]
}

# Dropdown-style plotting function
def plot_and_insight(df, plot_key, plot_label):
    df.columns = df.columns.str.strip().str.lower()
    with st.container():
        if plot_key == "Plot 1":
            df['docdate'] = pd.to_datetime(df['docdate'], errors='coerce')
            df = df.dropna(subset=['discount', 'value', 'docdate', 'loccode'])
            df['label'] = df['docdate'].dt.strftime('%Y-%m-%d') + ' | ' + df['loccode'].astype(str)

            top20 = df.sort_values(by='discount', ascending=False).head(20)
            top20 = top20.sort_values(by='discount', ascending=True)

            max_discount = top20['discount'].max()
            xlim_buffer = max_discount * 0.15  # 15% buffer to the right

            plt.figure(figsize=(14, 7))
            plt.hlines(y=top20['label'], xmin=0, xmax=top20['discount'], color='skyblue', linewidth=5)
            plt.plot(top20['discount'], top20['label'], "o", color='steelblue')

            for x, y in zip(top20['discount'], top20['label']):
                plt.text(x - (max_discount * 0.02), y, f"{x:,.0f}", va='center', ha='right', fontsize=9)

            plt.title("Top 20 Discounts By Location")
            plt.xlabel("Discount")
            plt.xlim(0, max_discount + xlim_buffer)  # Extend x-axis limit
            plt.grid(True)
            plt.tight_layout()
            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()

        elif plot_key == "Plot 2":
            df['returned'] = (df['qty'] < 0) | (df['value'] < 0)
            df['got_discount'] = df['discount'] > 0

            customer_flags = df.groupby('customerno').agg({
                'got_discount': 'any',
                'returned': 'any'
            }).reset_index()

            customer_flags['discount_group'] = customer_flags['got_discount'].map({True: 'With Discount', False: 'Without Discount'})
            customer_flags['returned'] = customer_flags['returned'].astype(int)

            summary = customer_flags.groupby('discount_group')['returned'].mean().reset_index()
            summary['returned'] *= 100

            plt.figure(figsize=(6, 5))
            ax = sns.barplot(data=summary, x='discount_group', y='returned', palette='Set2')

            for index, row in summary.iterrows():
                plt.text(index, row['returned'] * 0.5, f"{row['returned']:.1f}%", 
                        ha='center', va='center', fontsize=12, color='white', fontweight='bold')

            plt.title("Return Rate: With vs Without Discount")
            plt.ylabel("Return Rate (%)")
            plt.xlabel("Customer Group")
            plt.grid(True)
            plt.tight_layout()
            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()


        elif plot_key == "Plot 3":
            df = df.sort_values(by=['customerno', 'docdate'])
            df['customer_type'] = df.duplicated(subset='customerno', keep='first')
            df['customer_type'] = df['customer_type'].map({True: 'Existing Customers', False: 'New Customers'})
            df = df[(df['discount'] >= 0) & (df['discount'] <= 100)]

            avg_discount = df.groupby('customer_type')['discount'].mean().reset_index()
            avg_discount['discount'] = avg_discount['discount'].round(2)

            plt.figure(figsize=(8, 5))
            ax = sns.barplot(data=avg_discount, x='customer_type', y='discount', palette='pastel')

            for index, row in avg_discount.iterrows():
                plt.text(index, row['discount'] * 0.5, f"{row['discount']}%", 
                        ha='center', va='center', fontsize=12, color='black', fontweight='bold')

            plt.title("Average Discount: New vs Existing Customers")
            plt.ylabel("Discount")
            plt.xlabel("customer_type")
            plt.grid(True)
            plt.tight_layout()
            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()


        elif plot_key == "Plot 4":
            df['docdate'] = pd.to_datetime(df['docdate'])
            df['day'] = df['docdate'].dt.day
            daily_df = df.groupby('day').agg({'discount': 'mean', 'goldprice': 'mean'}).reset_index()
            fig, ax1 = plt.subplots(figsize=(12, 6))
            line1, = ax1.plot(daily_df['day'], daily_df['discount'], color='blue', marker='o', label='Avg Discount')
            ax1.set_xlabel('Day of Month')
            ax1.set_ylabel('Average Discount', color='blue')
            ax1.set_xticks(range(1, 32))
            ax1.grid(True)
            ax2 = ax1.twinx()
            line2, = ax2.plot(daily_df['day'], daily_df['goldprice'], color='orange', marker='s', label='Gold Price')
            ax2.set_ylabel('Gold Price', color='orange')
            ax1.legend([line1, line2], ['Avg Discount', 'Gold Price'], loc='upper right')
            plt.title("Discount vs Day and Gold Price")
            st.pyplot(fig)
            plt.clf()

        elif plot_key == "Plot 5":
            discount_columns = ['discount', 'idisc', 'obdisc', 'ghsdisc']
            base_exclude_cols = ['year', 'yearmonth', 'customerno', 'brand', 'totcategory']
            for disc_col in discount_columns:
                exclude_cols = [col for col in discount_columns if col != disc_col] + base_exclude_cols
                eligible_columns = [col for col in df.select_dtypes(include='number').columns if col not in exclude_cols]
                corr_matrix = df[eligible_columns].corr()
                corr_target = corr_matrix[[disc_col]].drop(index=disc_col)
                corr_target_sorted = corr_target.sort_values(by=disc_col, ascending=False)
                plt.figure(figsize=(8, 6))
                sns.heatmap(corr_target_sorted, annot=True, cmap='Reds', vmin=0, vmax=1, linewidths=0.5)
                plt.title(f'Correlation with {disc_col}')
                fig = plt.gcf()
                st.pyplot(fig)
                plt.clf()

        elif plot_key == "Plot 6":
            df_clean = df.dropna(subset=['customerno', 'discount'])
            df_clean = df_clean[df_clean['discount'] > 0]
            
            # Compute average discount per customer
            customer_avg = df_clean.groupby('customerno')['discount'].mean().reset_index()
            
            # Sort and get top 50 customers
            top_50_customers = customer_avg.sort_values(by='discount', ascending=False).head(50)
            
            # Convert 'customerno' to a categorical type to preserve order in plot
            top_50_customers['customerno'] = top_50_customers['customerno'].astype(str)
            top_50_customers['customerno'] = pd.Categorical(
                top_50_customers['customerno'],
                categories=top_50_customers['customerno'],
                ordered=True
            )
            
            # Plot
            plt.figure(figsize=(14, 6))
            sns.barplot(data=top_50_customers, x='customerno', y='discount', palette='tab20')
            plt.title("Top 50 Customers by Avg Discount")
            plt.xticks(rotation=90)
            plt.grid(True)
            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()


        elif plot_key == "Plot 7":
            df_clean = df.dropna(subset=['region', 'brand', 'totcategory', 'discount'])
            df_clean = df_clean[df_clean['discount'] > 0]
            grouped = df_clean.groupby(['region', 'brand', 'totcategory'])['discount'].mean().reset_index()
            plt.figure(figsize=(14, 6))
            sns.barplot(data=grouped, x='region', y='discount', hue='brand')
            plt.title("Avg Discount by Region, Brand, Category")
            plt.xticks(rotation=30)
            plt.grid(True)
            plt.tight_layout()
            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()

        st.markdown("---")
        st.markdown("### Insights for Business Stakeholders")
        for insight in predefined_insights.get(plot_key, ["No predefined insights available."]):
            st.markdown(f"- {insight}")
