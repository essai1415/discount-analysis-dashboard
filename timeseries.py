# time_series.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator


# Define insights (revised to 5 per plot)
predefined_insights = {
    "Plot 1": [
        "Spikes in discounts (Days 9–13) may align with events like festivals, auspicious dates, or marketing campaigns.",
        "Sudden drop after peak days suggests end of limited period offers or demand saturation post events.",
        "Steady mid to end month discounting may indicate efforts to sustain engagement or clear non premium stock.",
        "Low discounts in the first week could reflect strategy to maintain premium pricing before planned triggers.",
        "Analyzing discount trends alongside festivals like Akshaya Tritiya, wedding season can improve campaign timing and inventory planning."
    ],
    "Plot 2": [
        "Comparing sales on days with high OBDISC vs GHSDISC can help decide which type of discount works better.",
        "OBDISC changes a lot, with big jumps on days like 1-4, 17, and 25 this may be due to special store offers or quick sales pushes.",
        "GHSDISC stays more steady, showing it’s part of a planned customer scheme.",
        "GHSDISC builds long-term loyalty, while OBDISC helps with quick sales when needed."
    ],
    "Plot 3": [
        "Monday and Thursday offer the highest average discounts (6.4%), possibly to boost early-week sales and pre-weekend interest.",
        "Tuesday and Wednesday have the lowest discounts (4.7% and 4.5%), suggesting a slow-sale strategy on midweek days.",
        "Friday to Sunday maintain steady discounts (5.8%–6.0%) to attract weekend shoppers.",
        "Higher discounts on Mondays may be used to kickstart the week with better footfall and sales.",
        "This trend can guide weekly campaign planning like more promotions on low-performing days or optimized staffing on peak days."
    ],
    "Plot 4": [
        "Day 9 had the highest discount at ₹1.13 Cr, with 13.96% of sales value discounted.",
        "Days 9–13 show a peak discount window, with daily discounts ranging from ₹89.93L to ₹1.13 Cr.",
        "Day 12 saw the most transactions (736) and highest total value (₹8.54 Cr), with a 12.82% discount rate.",
        "Day 13 had the highest discount-to-sales percentage at 14.91%, with an average discount per transaction of ₹23,118.",
        "Overall discount rates hovered around 4–8%, but spiked above 10% during campaign days, indicating heavy promotions."
    ],
    "Plot 5": 
    ["A total of 420 return transactions occurred during the month, averaging around 13–14 returns per day.",
     "Return spikes occurred on Days 13, 18, 25, and 30, each peaking at 20–22 returns, suggesting potential post-offer dissatisfaction.",
     "Tanishq had the highest returns with 349 transactions, far more than Malabar (68) and Joy (3). Tanishq also had the highest number of unique returning customers (318), showing broader customer participation in returns.",
     "Returns were mostly from the DIA category (167), followed by GIS (97) and MCG (67), indicating that diamond and gemstone segments saw higher dissatisfaction or exchanges.",
     "Despite 420 total returns, the average daily return rate was ~13, which is low compared to peak daily transactions (700+), showing returns were manageable."
]
}

def plot_and_insight(df, plot_key, plot_label):
    df.columns = df.columns.str.strip().str.lower()
    with st.container():
        df['docdate'] = pd.to_datetime(df['docdate'], errors='coerce')
        df = df.dropna(subset=['docdate'])
        df['day'] = df['docdate'].dt.day

        if plot_key == "Plot 1":
            st.subheader("Daily Average idisc % (1-Month View)")

            # Step 1: Drop rows where idisc or value is missing or invalid
            df_idisc = df.dropna(subset=['idisc', 'value'])
            df_idisc = df_idisc[(df_idisc['idisc'] > 0) & (df_idisc['value'] > 0)]

            # Step 2: Calculate discount percentage
            df_idisc['idisc_pct'] = (df_idisc['idisc'] / df_idisc['value']) * 100

            # Step 3: Group by day and compute average discount %
            daily_avg = df_idisc.groupby('day')['idisc_pct'].mean().reset_index()

            # Step 4: Plot
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

        elif plot_key == "Plot 2":
                st.subheader("Daily Trend of OBDISC and GHSDISC")

                idisc_cols = ['obdisc', 'ghsdisc']
                df2 = df.dropna(subset=idisc_cols + ['value'])
                df2 = df2[df2['value'] > 0]  # Avoid divide-by-zero

                # Convert to percentage
                df2['obdisc_pct'] = (df2['obdisc'] / df2['value']) * 100
                df2['ghsdisc_pct'] = (df2['ghsdisc'] / df2['value']) * 100

                # Remove negative values
                df2 = df2[(df2['obdisc_pct'] >= 0) & (df2['ghsdisc_pct'] >= 0)]

                # Extract day
                df2['day'] = df2['docdate'].dt.day

                # Group and average
                daily_avg2 = df2.groupby('day')[['obdisc_pct', 'ghsdisc_pct']].mean().reset_index()

                # Melt for plotting
                df_melted = daily_avg2.melt(id_vars='day', var_name='idisc_type', value_name='average_discount_pct')

                # Plot
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
        
        elif plot_key == "Plot 4":
            st.subheader("Daily Discount Trend (%): Tanishq vs Mia, Zoya & Ecom")

            df['docdate'] = pd.to_datetime(df['docdate'])
            df['brand'] = df['brand'].str.upper()
            df['day'] = df['docdate'].dt.day

            df_valid = df[(df['discount'] > 0) & (df['value'] > 0)].copy()
            df_valid['discount_pct'] = (df_valid['discount'] / df_valid['value']) * 100

            # Remove outliers: Keep only 0–100%
            df_valid = df_valid[df_valid['discount_pct'] <= 100]


            # --- Tanishq
            df_tanishq = df_valid[df_valid['brand'] == 'TANISHQ']
            daily_discount_tanishq = df_tanishq.groupby('day')['discount_pct'].mean().reset_index()

            # --- Other Brands
            df_other = df_valid[df_valid['brand'] != 'TANISHQ']
            daily_discount_other = df_other.groupby(['day', 'brand'])['discount_pct'].mean().reset_index()

            # --- Plotting both subplots
            fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

            # Tanishq plot
            sns.lineplot(data=daily_discount_tanishq, x='day', y='discount_pct',
                        marker='o', color='goldenrod', ax=axs[0])
            axs[0].set_title("Tanishq - Daily Avg Discount (%)")
            axs[0].set_ylabel("Avg Discount (%)")
            axs[0].grid(True)

            # Other Brands plot
            sns.lineplot(data=daily_discount_other, x='day', y='discount_pct', hue='brand',
                        marker='o', palette='tab10', ax=axs[1])
            axs[1].set_title("Mia, Zoya & Ecom - Daily Avg Discount (%)")
            axs[1].set_xlabel("Day of Month")
            axs[1].set_ylabel("Avg Discount (%)")
            axs[1].grid(True)

            # Common x-ticks
            axs[1].set_xticks(range(1, 32))

            plt.tight_layout()
            st.pyplot(fig)
            plt.clf()


        
        elif plot_key == "Plot 5":
            st.subheader(" Daily Returned Transactions (Day 1–31)")

            df_ret = df.copy()
            df_ret['docdate'] = pd.to_datetime(df_ret['docdate'])

            # Filter only returned items
            df_ret['is_returned'] = (df_ret['qty'] < 0) | (df_ret['value'] < 0)
            returned_df = df_ret[df_ret['is_returned']]

            # Extract day of the month
            returned_df['day'] = returned_df['docdate'].dt.day

            # Group by day
            daily_returns = returned_df.groupby('day').size().reset_index(name='Return Count')

            # Ensure days 1 to 31 are present
            all_days = pd.DataFrame({'day': range(1, 32)})
            daily_returns = all_days.merge(daily_returns, on='day', how='left').fillna(0)

            # Plotting
            plt.figure(figsize=(12, 5))
            sns.lineplot(data=daily_returns, x='day', y='Return Count', marker='o', linewidth=2, color='crimson')
            plt.title("Returned Transactions per Day (1–31)", fontsize=16)
            plt.xlabel("Day of Month")
            plt.ylabel("Return Count")
            plt.xticks(range(1, 32))
            plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))  # Ensures y-axis is in whole numbers
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()

#SUMMARY TABLE

        if plot_key == "Plot 1":

            df_idisc = df.dropna(subset=['idisc', 'value'])
            df_idisc = df_idisc[(df_idisc['idisc'] > 0) & (df_idisc['value'] > 0)]

            # Calculate idisc as %
            df_idisc['idisc_pct'] = (df_idisc['idisc'] / df_idisc['value']) * 100

            # Clean fields
            df_idisc['day'] = df_idisc['docdate'].dt.day
            df_idisc['brand'] = df_idisc['brand'].str.upper()
            df_idisc['region'] = df_idisc['region'].str.upper()

            # Group-level summaries
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

            # Summary table
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

            st.markdown("### Discount Summary Insights (Based on idisc %)")
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True)


        elif plot_key == "Plot 2":
            st.markdown("### Summary table")

            idisc_cols = ['obdisc', 'ghsdisc']
            df2 = df.dropna(subset=idisc_cols + ['value'])
            df2 = df2[(df2['value'] > 0)]  # Avoid divide by zero

            # Calculate percentages
            df2['obdisc_pct'] = (df2['obdisc'] / df2['value']) * 100
            df2['ghsdisc_pct'] = (df2['ghsdisc'] / df2['value']) * 100

            # Remove negative values
            df2 = df2[(df2['obdisc_pct'] >= 0) & (df2['ghsdisc_pct'] >= 0)]

            # Extract day
            df2['day'] = df2['docdate'].dt.day

            # Group by day
            daily_avg = df2.groupby('day')[['obdisc_pct', 'ghsdisc_pct']].mean().reset_index()

            # Build summary
            summary_data = {
                "Discount Type": [],
                "Average Discount (%)": [],
                "Highest Daily Average (%)": [],
                "Lowest Daily Average (%)": [],
                "Day with Highest Avg Discount": [],
                "Day with Lowest Avg Discount": []
            }

            for col in ['obdisc_pct', 'ghsdisc_pct']:
                avg = daily_avg[col].mean()
                max_val = daily_avg[col].max()
                min_val = daily_avg[col].min()
                max_day = daily_avg.loc[daily_avg[col].idxmax(), 'day']
                min_day = daily_avg.loc[daily_avg[col].idxmin(), 'day']

                summary_data["Discount Type"].append("OBDISC" if "obdisc" in col else "GHSDISC")
                summary_data["Average Discount (%)"].append(f"{avg:.2f}")
                summary_data["Highest Daily Average (%)"].append(f"{max_val:.2f}")
                summary_data["Lowest Daily Average (%)"].append(f"{min_val:.2f}")
                summary_data["Day with Highest Avg Discount"].append(int(max_day))
                summary_data["Day with Lowest Avg Discount"].append(int(min_day))

            summary_df = pd.DataFrame(summary_data)

            st.dataframe(summary_df, use_container_width=True)


        elif plot_key == "Plot 3":

            df3 = df.dropna(subset=['value', 'discount'])
            df3 = df3[(df3['value'] > 0) & (df3['discount'] >= 0)]
            df3['discount_pct'] = df3['discount'] / df3['value']
            df3['docdate'] = pd.to_datetime(df3['docdate'])
            df3['day_of_week'] = df3['docdate'].dt.day_name()

            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df3['day_of_week'] = pd.Categorical(df3['day_of_week'], categories=day_order, ordered=True)

            avg_by_day = df3.groupby('day_of_week')['discount_pct'].mean().reindex(day_order)

            # --- Summary Table with Weekday vs Weekend Insights ---

            summary_df = df3.groupby('day_of_week')['discount_pct'].agg(
                Average_Discount_Percentage='mean',
                Transaction_Count='count'
            ).reindex(day_order).reset_index()

            summary_df['Day_Type'] = summary_df['day_of_week'].apply(
                lambda x: 'Weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'Weekend'
            )

            summary_df['Average_Discount_Percentage'] = (summary_df['Average_Discount_Percentage'] * 100).round(2)

            group_summary = summary_df.groupby('Day_Type').agg({
                'Average_Discount_Percentage': 'mean',
                'Transaction_Count': 'sum'
            }).round(2).reset_index()

            st.markdown("**Day wise Discount Summary**")
            st.dataframe(summary_df.rename(columns={
                'day_of_week': 'Day',
                'Average_Discount_Percentage': 'Avg Discount %',
                'Transaction_Count': 'Txn Count'
            }), use_container_width=True)

            st.markdown("**Weekday vs Weekend Summary**")
            st.dataframe(group_summary.rename(columns={
                'Day_Type': 'Day Type',
                'Average_Discount_Percentage': 'Avg Discount %',
                'Transaction_Count': 'Total Txns'
            }), use_container_width=True)


        elif plot_key == "Plot 4":
            st.markdown("###  Discount Summary")

            # Always define this at the beginning
            df_filtered = df[df['discount'] >= 0].copy()
            df_filtered['day'] = df_filtered['docdate'].dt.day
            df_filtered['brand'] = df_filtered['brand'].str.upper()

            # Separate unfiltered version for customer count
            df_customers = df.copy()
            df_customers['day'] = df_customers['docdate'].dt.day
            df_customers['brand'] = df_customers['brand'].str.upper()

            # Now start your logic
            summary_type = st.radio(
                "Choose Summary Type:",
                ["Per Brand per Day", "Total per Day (All Brands)"],
                horizontal=True
            )


            summary = None

            if summary_type == "Per Brand per Day":
                available_brands = df_filtered['brand'].unique().tolist()
                selected_brands = st.multiselect(
                    "Select Brands:",
                    options=available_brands,
                    default=available_brands
                )

                if selected_brands:
                    df_filtered = df_filtered[df_filtered['brand'].isin(selected_brands)]

                    grouped = df_filtered.groupby(['day', 'brand'])

                    summary = grouped.agg(
                        total_discount=('discount', 'sum'),
                        total_value=('value', 'sum'),
                        total_qty=('qty', 'sum'),
                        transactions=('docdate', 'count'),
                        total_customers=('customerno', 'count'),  # All transactions (not unique)
                        unique_customers=('customerno', pd.Series.nunique)  # Unique customer count
                    ).reset_index()

                else:
                    st.info("Please select at least one brand to view the summary.")

            else:  # Total per day
                grouped = df_filtered.groupby('day')

                summary = grouped.agg(
                    total_discount=('discount', 'sum'),
                    total_value=('value', 'sum'),
                    total_qty=('qty', 'sum'),
                    transactions=('docdate', 'count'),
                    unique_customers=('customerno', pd.Series.nunique)
                ).reset_index()

            # Step 3: Compute KPIs
            if summary is not None and not summary.empty:
                summary['avg_discount_per_transaction'] = summary['total_discount'] / summary['transactions']
                summary['avg_bill_value'] = summary['total_value'] / summary['transactions']
                summary['discount_pct_of_value'] = (summary['total_discount'] / summary['total_value']) * 100
                summary['avg_discount_per_unit'] = summary['total_discount'] / summary['total_qty']

                summary = summary.round(2)
                st.dataframe(summary, use_container_width=True)
            else:
                st.warning("No data to display.")

        elif plot_key == "Plot 5":

            df_return = df.copy()
            df_return['docdate'] = pd.to_datetime(df_return['docdate'])
            df_return['is_returned'] = (df_return['qty'] < 0) | (df_return['value'] < 0)
            returned_df = df_return[df_return['is_returned']].copy()

            if returned_df.empty:
                st.warning("No returned items found in the dataset.")
            else:
                # Add helper columns
                returned_df['day'] = returned_df['docdate'].dt.day
                returned_df['got_discount'] = returned_df['discount'] > 0

                # Summary metrics
                total_returns = len(returned_df)
                avg_discount = returned_df['discount'].mean()
                discounted_return_ratio = returned_df['got_discount'].value_counts(normalize=True) * 100

                summary_data = {
                    "Metric": [
                        "Total Returned Transactions",
                        "Average Discount on Returned Items (₹)",
                        "Returned with Discount (%)",
                        "Returned without Discount (%)"
                    ],
                    "Value": [
                        total_returns,
                        f"{avg_discount:,.2f}",
                        f"{discounted_return_ratio.get(True, 0):.2f}%",
                        f"{discounted_return_ratio.get(False, 0):.2f}%"
                    ]
                }
                summary_df = pd.DataFrame(summary_data)

                # Display metrics
                st.write(" **Key Return Metrics**")
                st.dataframe(summary_df, use_container_width=True)

                # Returns by Day + Brand + Category + Customer
                returns_by_day_detailed = (
                    returned_df
                    .groupby(['day', 'brand', 'totcategory', 'customerno'])
                    .size()
                    .reset_index(name='Return Count')
                    .sort_values(by='day')
                )
                returns_by_day_detailed.columns = ['Day of Month', 'Brand', 'Category', 'Customer No', 'Return Count']

                # Filters
                brands = ['All'] + sorted(returns_by_day_detailed['Brand'].unique().tolist())
                categories = ['All'] + sorted(returns_by_day_detailed['Category'].unique().tolist())

                selected_brand = st.selectbox(" Filter by Brand", brands)
                selected_category = st.selectbox(" Filter by Category", categories)

                filtered_df = returns_by_day_detailed.copy()
                if selected_brand != 'All':
                    filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
                if selected_category != 'All':
                    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

                # Add total row
                if not filtered_df.empty:
                    total_return_count = filtered_df['Return Count'].sum()
                    total_row = pd.DataFrame([{
                        'Day of Month': 'Total',
                        'Brand': '',
                        'Category': '',
                        'Customer No': '',
                        'Return Count': total_return_count
                    }])
                    filtered_df = pd.concat([filtered_df, total_row], ignore_index=True)

                st.write(" **Returns by Day of Month (Filtered)**")
                st.dataframe(filtered_df, use_container_width=True)

    # --- Toggle Logic for Insights ---
    toggle_key = f"show_insights_{plot_key}"  # Use plot_key here
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = False

    def toggle():
        st.session_state[toggle_key] = not st.session_state[toggle_key]

    button_label = "Hide Detailed Business Insights" if st.session_state[toggle_key] else "Show Detailed Business Insights"
    st.button(button_label, key=f"toggle_button_{plot_key}", on_click=toggle)

    if st.session_state[toggle_key]:
        st.markdown("### Business Insights For Stakeholders")
        for insight in predefined_insights.get(plot_key, [f"No insights available for {plot_key}."]):
            st.markdown(f"- {insight}")
