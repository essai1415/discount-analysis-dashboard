# multivariate.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick



# Define insights (revised to 5 per plot)
predefined_insights = {
    "Plot 1": [
        "RJH had the highest total sales on Jan 16 with ₹9.2L discount and ₹37.6L worth of purchases, showing a big sales opportunity to learn from.",
        "Jan 13 was a high-performing day with three top locations (VRR, UDI, TPP, KPB) contributing over ₹6.2L in total discounts and ₹6.3Cr in transaction value combined, indicating strong mid-month demand.",
        "Locations like CSB, CAN, TNV, and GUT gave discounts around ₹4.4L each but saw lower sales returns (~₹16L–17L), signaling the need to reassess the discount strategy there.",
        "AST had two appearances (Jan 12 & 31) with combined transactions of ₹29.5L, making it a consistently valuable location for repeated targeting.",
        "Stores like ZAH and ZBL delivered strong sales (₹20.8L and ₹19.4L) with lower discount inputs (~₹3.6L), showing efficient discount-to-sales conversion."
    ],
    "Plot 2": [
        "Products without discounts have a much higher return rate (15.1%) compared to those with discounts (4.2%).",
        "Discounted purchases are more likely to be final, suggesting higher customer satisfaction.",
        "Offering discounts may help reduce returns and improve customer retention.",
        "Non-discounted items may be returned due to price sensitivity, mismatch with expectations, or uncertain purchase decisions.",
        "These insights support using targeted discounts to drive quality sales and minimize returns."
    ],
    "Plot 3": [
        "Tanishq has the highest number of repeat customers (1,761) and most transactions (4,448) among multiple-time buyers",
        "Zoya offers the highest average discount (13.01%) for multiple time buyers, this may indicate an over-discounting trend to retain premium segment customers.",
        "Across both buyer types, ECOM maintains the lowest average discounts (0.14% for multiple, 0.84% for one-time buyers)",
        "MIA gives ~8.85% average discount to repeat buyers, yet has far fewer repeat customers (422) compared to Tanishq.",
        "One-time buyers at Tanishq receive an average 8.17% discount, lower than multiple-time buyers (9.55%)."
    ],
    "Plot 4": [
        "Days 9–13 show peak discounting (avg 8.18%) despite high gold prices (₹52.5K–₹63.7K), indicating possible festival or campaign-driven sales push.",
        "Day 3 had the highest gold price (₹63,702.75) with a strong discount (4.43%), suggesting margin flexibility on high-value days.",
        "Lowest discounts occurred on Days 6–7 (avg 3.23%) when gold prices dropped below ₹38K, implying pricing stability when metal costs are low.",
        "Discounts stabilize between Days 14–31 at 5.2%, aligning with mid-to-late month consistency, ideal for predictable promotions.",
        "Spikes in discounts (7–8% range) on Days 9–13 could be optimized via targeted marketing during these high-yield sales windows."
    ],
    "Plot 5": [
        "Plot 1: Overall Discount (discount): Strongly linked to stone value, total value, and making charges, showing higher discounts on premium, ornate items.",
        "Plot 2: Item Level Discount (idisc): Closely mirrors overall discount pattern, confirming it drives most of the total discount.",
        "Plot 3: Other Bill Discount (obdisc): Weakly correlated, suggesting it’s used for on demand or bill level adjustments.",
        "Plot 4: Gold Harvest Scheme Discount (ghsdisc): Has minimal correlation with transaction features, indicating it's likely applied uniformly or scheme based."
    ],
    "Plot 6": [
        "Customer 19878 made 19 transactions, spent ₹51.1L, and received a discount of ₹1.01L, a highly valuable and loyal customer.",
        "Customer 83776 (DIA) received a massive discount of ₹3.56L in just 5 transactions, spending ₹33.05L, signaling high-ticket discount optimization needs.",
        "8 customers transacted 9+ times, all in MCG or HCG, with spend ranging from ₹9.9L to ₹35.4L, deserving retention priority.",
        "Customer 2349 (DIA) got the highest single discount of ₹5.26L over only 5 transactions, spending ₹48.2L, may need manual review.",
        "Customers like 89042 and 91004 bought only 6 times but spent over ₹18.9L and ₹15.1L, showing they are big spenders who buy rarely and should be personally followed up."
    ],
    "Plot 7": [
        "Zoya  in WEST 3 gives the highest average discount (12.14%) with just 9 transactions totaling ₹77.96L, pointing to a small but highly discounted customer group.",
        "Tanishq in NORTH 1 leads with ₹13.16Cr in sales across 1000 transactions, showing strong reach with moderate 6.86% discounts.",
        "South 2 region saw the second highest contribution of Tanishq, totaling ₹9.2 Cr over 683 transactions, with a 6.32% average discount.",
        "Zoya achieved the highest average discount of 12.14% in West 3, though from only 9 transactions, generating ₹77.95 Lakhs.",
        "Mia's strongest performance was in South 3, with ₹44L from 109 transactions and an average discount of 7.64%."
        "Tanishq in West 3 led in both volume (774 transactions) and value (₹9.08 Cr) despite offering a moderate average discount of 7.12%."
    ],
    "Plot 8":[],
    "Plot 9":[]
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
            # Step 1: Calculate Discount % per bill safely
            df['discount_pct'] = df.apply(
                lambda row: round((row['discount'] / row['value']) * 100, 2) if row['value'] > 0 else 0,
                axis=1
            )

            # Step 2: Classify customers into Buyer Type
            txn_counts = df.groupby('customerno').size().reset_index(name='transaction_count')
            txn_counts['Buyer Type'] = txn_counts['transaction_count'].apply(
                lambda x: 'One-Time Buyer' if x == 1 else 'Multiple-Time Buyer'
            )
            df = df.merge(txn_counts[['customerno', 'Buyer Type']], on='customerno', how='left')

            # Step 3: Compute average discount % by buyer type
            avg_discount_summary = df.groupby('Buyer Type').agg(
                Customer_Count=('customerno', 'nunique'),
                Avg_Discount_Percent=('discount_pct', lambda x: round(x.mean(), 2))
            ).reset_index()

            # Step 4: Plot
            plt.figure(figsize=(6, 5))
            ax = sns.barplot(data=avg_discount_summary, x='Buyer Type', y='Avg_Discount_Percent', palette='Set2')

            for index, row in avg_discount_summary.iterrows():
                plt.text(index, row['Avg_Discount_Percent'] + 0.5, f"{row['Avg_Discount_Percent']:.2f}%", 
                        ha='center', va='bottom', fontsize=12, color='black', fontweight='bold')

            plt.title("Average Discount % by Buyer Type", fontsize=14)
            plt.ylabel("Avg Discount (%)", fontsize=12)
            plt.xlabel("Buyer Type", fontsize=12)
            plt.ylim(0, avg_discount_summary['Avg_Discount_Percent'].max() + 5)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            plt.clf()



        elif plot_key == "Plot 4":
            df['docdate'] = pd.to_datetime(df['docdate'])
            df['day'] = df['docdate'].dt.day

            # Calculate discount percentage per row
            df['discount_percent'] = (df['discount'] / df['value']) * 100  # assuming 'value' is bill amount

            # Remove negative discount percentages
            df = df[df['discount_percent'] >= 0]

            # Group by day and compute mean
            daily_df = df.groupby('day').agg({
                'discount_percent': 'mean',
                'goldprice': 'mean'
            }).reset_index()

            fig, ax1 = plt.subplots(figsize=(12, 6))
            line1, = ax1.plot(daily_df['day'], daily_df['discount_percent'], color='blue', marker='o', label='Avg Discount (%)')
            ax1.set_xlabel('Day of Month')
            ax1.set_ylabel('Average Discount (%)', color='blue')
            ax1.set_xticks(range(1, 32))
            ax1.grid(True)

            ax2 = ax1.twinx()
            line2, = ax2.plot(daily_df['day'], daily_df['goldprice'], color='orange', marker='s', label='Gold Price')
            ax2.set_ylabel('Gold Price', color='orange')

            ax1.legend([line1, line2], ['Avg Discount (%)', 'Gold Price'], loc='upper right')
            plt.title("Average Discount (%) vs Day and Gold Price")
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
            # Drop missing or invalid rows
            df_clean = df.dropna(subset=['region', 'brand', 'totcategory', 'discount', 'value'])
            df_clean = df_clean[(df_clean['discount'] > 0) & (df_clean['value'] > 0)]

            # Standardize region and brand names
            df_clean['region'] = df_clean['region'].str.strip().str.upper()
            df_clean['brand'] = df_clean['brand'].str.strip().str.upper()

            # Remove ECOM brand
            df_clean = df_clean[df_clean['brand'] != 'ECOM']

            # Calculate discount percentage
            df_clean['discount_percent'] = (df_clean['discount'] / df_clean['value']) * 100

            # Group by Region, Brand, and Totcategory
            grouped = df_clean.groupby(['region', 'brand', 'totcategory'])['discount_percent'].mean().reset_index()
            grouped['discount_percent'] = grouped['discount_percent'].round(2)

            # Plot
            plt.figure(figsize=(14, 6))
            sns.barplot(data=grouped, x='region', y='discount_percent', hue='brand')
            plt.title("Average Discount (%) by Region and Brand (Excluding ECOM)")
            plt.ylabel("Average Discount (%)")
            plt.xlabel("Region")
            plt.xticks(rotation=0)
            plt.grid(True)
            plt.tight_layout()

            fig = plt.gcf()
            st.pyplot(fig)
            plt.clf()

        elif plot_key == "Plot 8":
            df_plot = df.copy()

            # Filter valid rows
            df_plot = df_plot[
                (df_plot['brand'].notnull()) &
                (df_plot['level'].notnull()) &
                (df_plot['discount'] > 0) &
                (df_plot['value'] > 0)
            ]

            # Calculate discount percentage
            df_plot['discount_percent'] = (df_plot['discount'] / df_plot['value']) * 100

            # Clean and standardize brand and level
            df_plot['brand'] = df_plot['brand'].str.strip().str.upper()
            df_plot['level'] = df_plot['level'].astype(str).str.strip().str.upper()

            # Group by brand and level using discount_percent
            grouped = df_plot.groupby(['brand', 'level'])['discount_percent'].mean().reset_index()

            # Preserve brand order based on total discount percent (descending)
            brand_order = grouped.groupby('brand')['discount_percent'].sum().sort_values(ascending=False).index
            grouped['brand'] = pd.Categorical(grouped['brand'], categories=brand_order, ordered=True)

            # Plot
            plt.figure(figsize=(18, 10))
            sns.set_theme(style="whitegrid")

            ax = sns.barplot(
                data=grouped,
                x='discount_percent',
                y='brand',
                hue='level',
                palette='Set2'
            )

            # Bar labels
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f%%', padding=3, fontsize=12)

            # Titles and axis labels
            plt.title("Average Discount (%) per Transaction by Brand and Level", fontsize=18, weight='bold')
            plt.xlabel("Average Discount (%)", fontsize=14)
            plt.ylabel("Brand", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend(title="Level", title_fontsize=13, fontsize=12, loc='center left', bbox_to_anchor=(1, 0.5))

            plt.tight_layout()
            st.pyplot(plt)
            plt.clf()

        elif plot_key == "Plot 9":
            df_plot = df.copy()

            # Clean and preprocess
            df_plot = df_plot.dropna(subset=['region', 'brand', 'discount', 'value', 'customerno'])
            df_plot = df_plot[
                (df_plot['discount'] > 0) &
                (df_plot['value'] > 0) &
                (~df_plot['region'].astype(str).str.upper().isin(['NULL', '[NULL]', 'NAN'])) &
                (~df_plot['brand'].astype(str).str.upper().isin(['NULL', '[NULL]', 'NAN']))
            ]

            # Standardize text
            df_plot['region'] = df_plot['region'].astype(str).str.strip().str.upper()
            df_plot['brand'] = df_plot['brand'].astype(str).str.strip().str.upper()

            # Compute discount %
            df_plot['discount_percent'] = (df_plot['discount'] / df_plot['value']) * 100

            # Get top 6 regions by total discount (not excluding ECOM)
            region_discounts = df_plot.groupby('region')['discount'].sum().sort_values(ascending=False)
            top_regions = region_discounts.head(6).index.tolist()
            remaining_regions = region_discounts.iloc[6:].index.tolist()

            # Exclude ECOM when choosing top brands
            valid_brands = df_plot[~df_plot['brand'].isin(['ECOM'])]
            top_brands = valid_brands.groupby('brand')['discount'].sum().nlargest(5).index.tolist()

            # Function: Avg discount % per customer, grouped by region and brand
            def get_avg_discount_percent(df_sub):
                return (
                    df_sub.groupby(['region', 'brand', 'customerno'])['discount_percent']
                    .mean()
                    .reset_index()
                    .groupby(['region', 'brand'])['discount_percent']
                    .mean()
                    .reset_index()
                )

            # -------- Plot 1: Top 6 Regions × Top 5 Brands (including ECOM if present) --------
            top_df = df_plot[df_plot['region'].isin(top_regions) & df_plot['brand'].isin(top_brands + ['ECOM'])]
            grouped_top = get_avg_discount_percent(top_df)
            region_order_top = grouped_top.groupby('region')['discount_percent'].mean().sort_values(ascending=False).index.tolist()
            grouped_top['region'] = pd.Categorical(grouped_top['region'], categories=region_order_top, ordered=True)

            st.subheader("Top 6 Regions vs Top 5 Brands – Avg Discount % per Transaction")
            fig1, ax1 = plt.subplots(figsize=(14, 8))
            sns.set_theme(style="whitegrid")
            sns.barplot(
                data=grouped_top,
                x='region',
                y='discount_percent',
                hue='brand',
                palette='Set2',
                width=0.7,
                ax=ax1
            )

            for container in ax1.containers:
                for bar in container:
                    height = bar.get_height()
                    if height > 0:
                        ax1.text(
                            bar.get_x() + bar.get_width() / 2,
                            height + 0.4,
                            f"{height:.1f}%",
                            ha='center',
                            va='bottom',
                            fontsize=10,
                            weight='semibold',
                            color='black'
                        )

            ax1.set_title("Top 6 Regions – Avg Discount % per Transaction to Top 5 Brands (incl. ECOM)", fontsize=16, weight='bold')
            ax1.set_xlabel("Region", fontsize=13)
            ax1.set_ylabel("Avg Discount per Transaction (%)", fontsize=13)
            ax1.tick_params(axis='x', labelsize=11)
            ax1.tick_params(axis='y', labelsize=11)
            ax1.legend(title="Brand", title_fontsize=12, fontsize=11, loc='center left', bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            st.pyplot(fig1)
            plt.clf()

            # -------- Plot 2: Remaining Regions × Top 5 Brands (including ECOM if present) --------
            remaining_df = df_plot[df_plot['region'].isin(remaining_regions) & df_plot['brand'].isin(top_brands + ['ECOM'])]
            grouped_remain = get_avg_discount_percent(remaining_df)
            region_order_remain = grouped_remain.groupby('region')['discount_percent'].mean().sort_values(ascending=False).index.tolist()
            grouped_remain['region'] = pd.Categorical(grouped_remain['region'], categories=region_order_remain, ordered=True)

            st.subheader("Remaining Regions vs Top 5 Brands – Avg Discount % per Transaction")
            fig2, ax2 = plt.subplots(figsize=(14, 8))
            sns.barplot(
                data=grouped_remain,
                x='region',
                y='discount_percent',
                hue='brand',
                palette='Set2',
                width=0.7,
                ax=ax2
            )

            for container in ax2.containers:
                for bar in container:
                    height = bar.get_height()
                    if height > 0:
                        ax2.text(
                            bar.get_x() + bar.get_width() / 2,
                            height + 0.4,
                            f"{height:.1f}%",
                            ha='center',
                            va='bottom',
                            fontsize=10,
                            weight='semibold',
                            color='black'
                        )

            ax2.set_title("Remaining Regions – Avg Discount % per Transaction to Top 5 Brands (incl. ECOM)", fontsize=16, weight='bold')
            ax2.set_xlabel("Region", fontsize=13)
            ax2.set_ylabel("Avg Discount per Transaction (%)", fontsize=13)
            ax2.tick_params(axis='x', labelsize=11, rotation=30)
            ax2.tick_params(axis='y', labelsize=11)
            ax2.legend(title="Brand", title_fontsize=12, fontsize=11, loc='center left', bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            st.pyplot(fig2)
            plt.clf()

# Summary Table

        if plot_key == "Plot 1":
            # [Existing plot logic above...]
            summary_table = top20.copy()
            summary_table['docdate'] = pd.to_datetime(summary_table['docdate']).dt.strftime('%Y-%m-%d')
            summary_table = summary_table.rename(columns={
                'docdate': 'Date',
                'loccode': 'Location',
                'discount': 'Discount Value',
                'value': 'Transaction Value'
            })[['Date', 'Location', 'Discount Value', 'Transaction Value']]
            st.markdown("###  Top 20 Discounted Transactions")
            st.dataframe(summary_table)

        elif plot_key == "Plot 2":
            # Step 1: Flag returns and discounts
            df['returned'] = (df['qty'] < 0) | (df['value'] < 0)
            df['got_discount'] = df['discount'] > 0

            # Step 2: Aggregate per customer
            customer_flags = df.groupby('customerno').agg({
                'got_discount': 'any',
                'returned': 'any'
            }).reset_index()

            # Step 3: Label groups
            customer_flags['Discount Group'] = customer_flags['got_discount'].map({
                True: 'With Discount',
                False: 'Without Discount'
            })

            # Sidebar: Only Discount Group filter
            discount_filter = st.selectbox(
                "Filter by Discount Group",
                options=['All', 'With Discount', 'Without Discount'],
                index=0
            )

            # Apply selected filter
            if discount_filter != 'All':
                customer_flags = customer_flags[customer_flags['Discount Group'] == discount_filter]

            # Summary metrics
            total_customers = customer_flags['customerno'].nunique()
            total_returns = customer_flags['returned'].sum()
            avg_return_rate = (total_returns / total_customers * 100) if total_customers > 0 else 0

            # Display summary
            st.markdown("### Customer Return Summary")
            st.markdown(f"- **Total Unique Customers:** {total_customers}")
            st.markdown(f"- **Customers Who Returned:** {int(total_returns)}")
            st.markdown(f"- **Return Rate:** {avg_return_rate:.2f}%")

        elif plot_key == "Plot 3":
            # Add Buyer Type column
            df['Buyer Type'] = df.groupby('customerno')['customerno'].transform('count').apply(
                lambda x: 'One-Time Buyer' if x == 1 else 'Multiple-Time Buyer'
            )

            # Dropdown filters
            buyer_type_options = df['Buyer Type'].unique().tolist()
            brand_options = df['brand'].unique().tolist()

            selected_buyer_types = st.multiselect("Select Buyer Type(s):", buyer_type_options, default=buyer_type_options)
            selected_brands = st.multiselect("Select Brand(s):", brand_options, default=brand_options)

            # Filtered DataFrame
            filtered_df = df[df['Buyer Type'].isin(selected_buyer_types) & df['brand'].isin(selected_brands)]

            # Group by Buyer Type and Brand
            multivariate_summary = filtered_df.groupby(['Buyer Type', 'brand']).agg(
                Total_Customers=('customerno', 'nunique'),
                Total_Transactions=('customerno', 'count'),
                Total_Discount=('discount', 'sum'),
                Total_Value=('value', 'sum')
            ).reset_index()

            multivariate_summary['Avg Discount (%)'] = multivariate_summary.apply(
                lambda row: round((row['Total_Discount'] / row['Total_Value']) * 100, 2)
                if row['Total_Value'] > 0 else 0,
                axis=1
            )


            # Final clean columns
            multivariate_summary = multivariate_summary[['Buyer Type', 'brand', 'Total_Customers', 'Total_Transactions', 'Avg Discount (%)']]

            # Display in Streamlit
            st.markdown("### Buyer Type × Brand vs Discount Summary")
            st.dataframe(multivariate_summary)

        elif plot_key == "Plot 4":
            df['docdate'] = pd.to_datetime(df['docdate'])
            df['day'] = df['docdate'].dt.day

            # Calculate discount percentage
            df['discount_percent'] = (df['discount'] / df['value']) * 100

            # Remove negative values and zero bill value (to avoid division by zero)
            df = df[(df['value'] > 0) & (df['discount_percent'] >= 0)]

            # Group by day
            daily_df = df.groupby('day').agg({
                'discount_percent': 'mean',
                'goldprice': 'mean'
            }).reset_index()

            # Updated summary table
            daily_stats = daily_df.copy()
            daily_stats.columns = ['Day of Month', 'Avg Discount (%)', 'Avg Gold Price (₹)']
            daily_stats = daily_stats.round(2)

            st.markdown("### Day-wise Discount vs Gold Price Summary")
            st.dataframe(daily_stats)


        elif plot_key == "Plot 5":
            rows = []
            for disc_col in discount_columns:
                eligible_columns = [col for col in df.select_dtypes(include='number').columns 
                                    if col not in discount_columns + base_exclude_cols]
                corr_series = df[eligible_columns + [disc_col]].corr()[disc_col].drop(disc_col)
                top_feature = corr_series.idxmax()
                rows.append({
                    "Discount Type": disc_col.upper(),
                    "Top Correlated Feature": top_feature,
                    "Correlation Value": round(corr_series[top_feature], 3)
                })
            st.markdown("###  Key Drivers of Each Discount Type")
            st.dataframe(pd.DataFrame(rows))

        elif plot_key == "Plot 6":
            st.markdown("###  Top 50 Customers by Brand & Category Preference")

            # Clean data: Remove invalid/NULL values in totcategory and filter only valid purchases
            valid_df = df_clean[
                (df_clean['discount'] >= 0) &
                (df_clean['qty'] > 0) &
                (~df_clean['totcategory'].isin(["NULL", "[NULL]", "None", "", None])) &
                (df_clean['totcategory'].notna())
            ]

            # Filters
            brands = valid_df['brand'].dropna().unique().tolist()
            categories = valid_df['totcategory'].unique().tolist()

            selected_brands = st.multiselect("Select Brand(s):", options=sorted(brands), default=sorted(brands))
            selected_categories = st.multiselect("Select Category(ies):", options=sorted(categories), default=sorted(categories))

            # Apply filters
            filtered_df = valid_df[
                (valid_df['brand'].isin(selected_brands)) &
                (valid_df['totcategory'].isin(selected_categories))
            ]

            if filtered_df.empty:
                st.warning("No data available for the selected filters.")
            else:
                # Groupwise most frequent brand/category (mode)
                brand_mode = filtered_df.groupby('customerno')['brand'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
                category_mode = filtered_df.groupby('customerno')['totcategory'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)

                # Summary aggregation
                summary = filtered_df.groupby('customerno').agg(
                    Max_Discount=('discount', 'max'),
                    Transaction_Count=('discount', 'count'),
                    Total_Spend=('value', 'sum')
                ).round(2)

                # Combine with mode values
                summary['Most Frequent Brand'] = brand_mode
                summary['Top Category Purchased'] = category_mode

                # Final formatting
                summary = summary.reset_index().sort_values(by='Transaction_Count', ascending=False).head(50)

                st.dataframe(summary[['customerno', 'Most Frequent Brand', 'Top Category Purchased',
                                    'Max_Discount', 'Transaction_Count', 'Total_Spend']])

        elif plot_key == "Plot 7":
            st.markdown("###  Region-Brand Level Discount (%) Performance")

            # Clean and standardize fields
            df_clean['region'] = df_clean['region'].astype(str).str.strip().str.upper()
            df_clean['brand'] = df_clean['brand'].astype(str).str.strip().str.upper()

            # Remove invalid entries
            valid_df = df_clean[
                (df_clean['discount'] >= 0) &
                (df_clean['qty'] > 0) &
                (df_clean['value'] > 0) &  # prevent division by zero
                (~df_clean['region'].isin(["NULL", "[NULL]", "NONE", "", None])) &
                (df_clean['region'].notna()) &
                (df_clean['brand'].notna())
            ]

            # Remove ECOM brand and fix EAST region if needed
            valid_df = valid_df[valid_df['brand'] != 'ECOM']

            # Calculate discount percentage
            valid_df['discount_percent'] = (valid_df['discount'] / valid_df['value']) * 100

            # Dropdown filters
            regions = valid_df['region'].dropna().unique().tolist()
            brands = valid_df['brand'].dropna().unique().tolist()

            selected_regions = st.multiselect("Select Region(s):", options=sorted(regions), default=sorted(regions))
            selected_brands = st.multiselect("Select Brand(s):", options=sorted(brands), default=sorted(brands))

            # Apply filters
            filtered_df = valid_df[
                (valid_df['region'].isin(selected_regions)) &
                (valid_df['brand'].isin(selected_brands))
            ]

            if filtered_df.empty:
                st.warning("No data available for the selected filters.")
            else:
                # Group and summarize
                summary = filtered_df.groupby(['region', 'brand']).agg(
                    Avg_Discount_Percent=('discount_percent', 'mean'),
                    Txn_Count=('discount_percent', 'count'),
                    Total_Value=('value', 'sum')
                ).reset_index().round(2).sort_values(by='Avg_Discount_Percent', ascending=False)

                summary.rename(columns={
                    'region': 'Region',
                    'brand': 'Brand',
                    'Avg_Discount_Percent': 'Avg Discount (%)',
                    'Txn_Count': 'Transaction Count',
                    'Total_Value': 'Total Value (₹)'
                }, inplace=True)

                st.dataframe(summary[['Region', 'Brand', 'Avg Discount (%)', 'Transaction Count', 'Total Value (₹)']])

        elif plot_key == "Plot 8":
            # (This assumes df_plot already has discount_percent calculated and cleaned above)

            summary = df_plot.groupby(['brand', 'level']).agg(
                Avg_Discount_Percent=('discount_percent', 'mean'),
                Total_Transactions=('discount_percent', 'count')
            ).round(2).reset_index().sort_values(by='Avg_Discount_Percent', ascending=False)

            # Rename for clarity
            summary.columns = ['Brand', 'Level', 'Avg Discount (%)', 'Total Transactions']

            st.markdown("### Brand × Level Discount (%) Overview")
            st.dataframe(summary)

        elif plot_key == "Plot 9":
            st.markdown("###  Brand-wise Avg Discount (%) by Region")

            # Clean data - Match plot logic
            valid_df = df[
                (df['discount'] > 0) &
                (df['value'] > 0) &
                (~df['region'].astype(str).str.upper().isin(["NULL", "[NULL]", "NONE", "", "NAN"])) &
                (df['region'].notna()) &
                (df['brand'].notna())
            ].copy()

            # Standardize region & brand
            valid_df['region'] = valid_df['region'].astype(str).str.strip().str.upper()
            valid_df['brand'] = valid_df['brand'].astype(str).str.strip().str.upper()

            # Compute row-level discount %
            valid_df['discount_percent'] = (valid_df['discount'] / valid_df['value']) * 100

            # Filters
            regions = valid_df['region'].unique().tolist()
            brands = valid_df['brand'].unique().tolist()

            selected_regions = st.multiselect("Select Region(s):", options=sorted(regions), default=sorted(regions))
            selected_brands = st.multiselect("Select Brand(s):", options=sorted(brands), default=sorted(brands))

            # Apply filters
            filtered_df = valid_df[
                (valid_df['region'].isin(selected_regions)) &
                (valid_df['brand'].isin(selected_brands))
            ]

            if filtered_df.empty:
                st.warning("No data available for the selected filters.")
            else:
                # Align with plot logic: average per customer first, then average per brand-region
                summary = (
                    filtered_df
                    .groupby(['region', 'brand', 'customerno'])['discount_percent']
                    .mean()
                    .reset_index()
                    .groupby(['region', 'brand'])['discount_percent']
                    .mean()
                    .reset_index()
                    .rename(columns={'discount_percent': 'Avg Discount (%)'})
                    .round(2)
                )

                st.dataframe(summary)


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

