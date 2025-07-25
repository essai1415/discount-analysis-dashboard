import streamlit as st
import pandas as pd

def show_facts_and_figures(df):
    st.set_page_config(page_title="Jewellery Data Explorer", layout="centered")

    st.markdown("### <b> Interactive Facts and Figures of the Dataset</b>", unsafe_allow_html=True)

    # Optional Exclude Negative Transactions
    exclude_negatives = st.checkbox(" Exclude returned (negative) transactions", value=False)
    filtered_df = df.copy()
    if exclude_negatives:
        filtered_df = filtered_df[(filtered_df['qty'] > 0) & (filtered_df['value'] > 0) & (filtered_df['wt'] > 0) & (filtered_df['discount'] >= 0)]

    raw_df = filtered_df.copy()

    # === Dataset Overview ===
    st.markdown("### <b> Dataset Overview</b>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", f"{raw_df.shape[0]:,}")
    with col2:
        st.metric("Total Columns", f"{raw_df.shape[1]:,}")
    with col3:
        try:
            # Detect customer and date columns
            customer_cols = [col for col in raw_df.columns if 'cust' in col.lower()]
            
            if customer_cols and 'docdate' in raw_df.columns:
                cust_col = customer_cols[0]
                raw_df['docdate'] = pd.to_datetime(raw_df['docdate'], errors='coerce')
                raw_df = raw_df.sort_values('docdate')

                # Get first purchase date
                first_purchase = raw_df.groupby(cust_col)['docdate'].min().reset_index()
                first_purchase.columns = [cust_col, 'first_purchase']
                raw_df = raw_df.merge(first_purchase, on=cust_col)

                # Tag new/repeat
                raw_df['Customer Type'] = raw_df.apply(
                    lambda row: 'New' if row['docdate'] == row['first_purchase'] else 'Repeat',
                    axis=1
                )

                new_txns = (raw_df['Customer Type'] == 'New').sum()
                repeat_txns = (raw_df['Customer Type'] == 'Repeat').sum()
                total_txns = new_txns + repeat_txns

                new_pct = round((new_txns / total_txns) * 100, 2)
                repeat_pct = round((repeat_txns / total_txns) * 100, 2)

                st.markdown(f"""
                •  **Total Transactions:** {total_txns:,}  
                •  **New Customers:** {new_txns:,} ({new_pct}%)  
                •  **Repeat Customers:** {repeat_txns:,} ({repeat_pct}%)
                """, unsafe_allow_html=True)
            else:
                st.markdown("• **Customer or Date column missing.**", unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"• **Customer Info Error:** {e}", unsafe_allow_html=True)

    # === High-Level Facts ===
    st.markdown("### <b> High-Level Facts</b>", unsafe_allow_html=True)

    def cleaned_unique_count(df, column):
        return df[~df[column].astype(str).str.upper().isin(["NULL", "NA", "NIL", "","[NULL]"])][column].nunique()

    facts = {
        "Unique Brands": raw_df['brand'].nunique(),
        "Regions Covered": cleaned_unique_count(raw_df, 'region'),
        "Retail Levels": raw_df['level'].nunique(),
        "Years Available": raw_df['year'].nunique(),
        "YearMonth Patterns": raw_df['yearmonth'].nunique(),
        "Months in Data": raw_df['month'].nunique(),
        "Date Range": f"{pd.to_datetime(raw_df['docdate']).min().date()} to {pd.to_datetime(raw_df['docdate']).max().date()}",
        "Unique Locations": raw_df['loccode'].nunique(),
        "Retail Clusters": cleaned_unique_count(raw_df, 'rcluster'),
        "Bill Discount Types": raw_df['bdisc'].nunique() + (1 if (raw_df['discount'] > 0).any() else 0),
        "Categories": cleaned_unique_count(raw_df, 'totcategory'),
        "EC Bands (Total)": cleaned_unique_count(raw_df, 'totalecband'),
        "Cluster EC Bands": cleaned_unique_count(raw_df, 'clusterecband'),
        "Price Bands": cleaned_unique_count(raw_df, 'priceband'),
        "AMCB Bands": raw_df['amcb'].nunique(),
        "Unique Customers": cleaned_unique_count(raw_df, 'customerno')
    }

    for key, value in facts.items():
        st.markdown(f"- **{key}:** {value}")

    # === Customer Insight ===
    st.markdown("###  **Core Transaction Insights & Data Gaps**", unsafe_allow_html=True)

    # === Customer Transaction Summary - Single Line ===
    try:
        # Detect customer and date columns
        customer_cols = [col for col in df.columns if 'cust' in col.lower()]
        
        # Top brands
        top_brands = df['brand'].value_counts().head(5)
        st.markdown("-**Top Brands by Customer Count:**")
        for brand, count in top_brands.items():
            st.markdown(f"  - {brand}: {count:,} customers")

        # Top price bands
        top_pricebands = df['priceband'].value_counts().head(3)
        st.markdown("-**Most Common Price Bands:**")
        for band, count in top_pricebands.items():
            st.markdown(f"  - {band}: {count:,} items")

        # Busiest month
        busiest_month = df['month'].value_counts().idxmax()
        st.markdown(f"-**Month with Highest Transactions:** {busiest_month}")

        # Top regions by total sales value
        top_regions = df.groupby('region')['value'].sum().sort_values(ascending=False).head(3)
        st.markdown("-**Top Regions by Total Sales Value:**")
        for region, val in top_regions.items():
            st.markdown(f"  - {region}: ₹{val:,.0f}")

    except Exception as e:
        st.warning(f"Could not generate customer insights: {e}")
        # Missing values in categorical columns (including amcb with NaN and placeholder strings)
    missing_like = ["NULL", "NA", "NIL", "", "[NULL]"]

    st.markdown("-**Missing Values in Categorical Columns:**")

    found_missing = False

    # Check object (categorical) columns
    for col in df.select_dtypes(include='object').columns:
        col_upper = df[col].astype(str).str.upper()
        missing_count = col_upper.isin(missing_like).sum()
        if missing_count > 0:
            st.markdown(f"  - {col}: {missing_count:,} missing")
            found_missing = True

    # Check 'amcb' column
    if 'amcb' in df.columns:
        amcb_str_missing = df['amcb'].astype(str).str.upper().isin(missing_like).sum()
        amcb_nan_missing = df['amcb'].isnull().sum()
        total_amcb_missing = amcb_str_missing + amcb_nan_missing
        if total_amcb_missing > 0:
            st.markdown(f"  - amcb: {total_amcb_missing:,} missing")
            found_missing = True

    if not found_missing:
        st.markdown("   No missing values found")

    # === Summary Statistics ===
    st.markdown("### <b>Summary Statistics</b>", unsafe_allow_html=True)
    if not filtered_df.empty:
        numeric_cols = ['qty', 'value', 'wt', 'discount', 'idisc', 'obdisc', 'ghsdisc', 'mc', 'goldprice', 'stonevalue']
        filtered_df = filtered_df[filtered_df[numeric_cols].ge(0, axis=1).all(axis=1)]
        num_summary = filtered_df[numeric_cols].describe().T[['min', 'mean', 'max', 'std', '25%', '50%', '75%']]

        st.markdown("#### <b>Numeric Summary</b>", unsafe_allow_html=True)
        st.dataframe(num_summary, use_container_width=True)

# === Categorical Summary — match High-Level Facts ===
    placeholder_values = ["NULL", "NA", "[NA]", "NIL", "", "[NULL]"]
    cleaned_obj_df = raw_df.copy()

    # Replace placeholders with NaN for consistency
    for col in cleaned_obj_df.select_dtypes(include='object').columns:
        cleaned_obj_df[col] = cleaned_obj_df[col].astype(str).replace(placeholder_values, pd.NA)

    display_df = cleaned_obj_df

    # Get object (categorical) columns
    categorical_cols = display_df.select_dtypes(include='object').columns

    # Prepare summary dictionary
    summary_data = {'unique': [], 'top': [], 'freq': []}

    for col in categorical_cols:
        col_data = display_df[col]
        # Convert everything to actual NaNs first
        col_data = col_data.replace(placeholder_values + ['nan', 'NaN', 'None'], pd.NA)

        # Drop NaNs before computing
        non_null_data = col_data.dropna()

        summary_data['unique'].append(non_null_data.nunique())

        if not non_null_data.empty:
            top_value = non_null_data.mode().iloc[0]
            freq = (non_null_data == top_value).sum()
        else:
            top_value = 'N/A'
            freq = 0

        summary_data['top'].append(top_value)
        summary_data['freq'].append(freq)


    # Create summary DataFrame
    obj_summary = pd.DataFrame(summary_data, index=categorical_cols)

    # Remove 'discount' and 'customertype' rows if present
   # Remove unwanted rows
    for unwanted_row in ['Customer Type', 'discount']:
        if unwanted_row in obj_summary.index:
            obj_summary = obj_summary.drop(index=unwanted_row)

    # Remove 'amcb' row if it's all NA
    if 'amcb' in display_df.columns and display_df['amcb'].dropna().empty:
        obj_summary = obj_summary.drop(index='amcb', errors='ignore')

    # Add new combined 'discount' summary row (across discount types)
    # Add new 'discount' summary row (for all discount types)
    discount_summary = {
    'unique': 3,
    'top': 'idisc',
    'freq': display_df['idisc'].notna().sum() if 'idisc' in display_df.columns else 0
}
    discount_cols = ['bdisc', 'idisc', 'ghsdisc', 'obdisc']
    available_discounts = [col for col in discount_cols if col in display_df.columns]

    if available_discounts:
        total_unique = sum(display_df[col].nunique(dropna=True) for col in available_discounts)
        top_combined = ', '.join(available_discounts)
        total_freq = sum(display_df[col].notna().sum() for col in available_discounts)
        obj_summary.loc['discount'] = {'unique': total_unique, 'top': top_combined, 'freq': total_freq}
        obj_summary.loc['discount'] = discount_summary

        # Display the summary
        if not obj_summary.empty:
            st.markdown("#### <b>Categorical Summary</b>", unsafe_allow_html=True)
            st.dataframe(obj_summary, use_container_width=True)

    # === Line Chart for Trends ===
    st.markdown("### <b>Trend Exploration</b>", unsafe_allow_html=True)
    time_col = st.selectbox("Select Time Column", options=['docdate'])
    metric_col = st.selectbox("Select Metric to Visualize", options=numeric_cols)
    if time_col and metric_col:
        trend_df = filtered_df.copy()
        trend_df[time_col] = pd.to_datetime(trend_df[time_col], errors='coerce')
        trend_df = trend_df.dropna(subset=[time_col])
        trend_data = trend_df.groupby(time_col)[metric_col].sum().reset_index()
        trend_data = trend_data.sort_values(by=time_col)
        st.line_chart(trend_data.set_index(time_col))

    # === Stakeholder Notes ===
    st.markdown("---")
    st.markdown("### <b>Business Use Cases</b>", unsafe_allow_html=True)
    st.markdown("""
    - Offers a 360° view of how discounts are distributed across products, customers, and sales metrics.  
    - Enables data-driven decision-making in discount policies by uncovering what drives discount value.  
    - Filter on product segments (brand/category/priceband) to identify patterns.   
    - Equips management with fact-based evidence to justify or revise discount structures.  
    - Enhances transparency and accountability across branches by surfacing outliers and inconsistencies.  
    """)
