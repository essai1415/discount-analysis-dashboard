import streamlit as st
import pandas as pd
import quantitative as quantitative
import qualitativee as qualitative
import matplotlib.pyplot as plt
import multivariate
import timeseries
import fandf
import base64
import requests
import io

st.set_page_config(page_title="Jewellery Discount Dashboard", layout="centered")
# Load the image and convert to base64
with open("gold.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()

# Display the title in one line
st.markdown(
    f"""
    <div style="width: 100%; display: flex; justify-content: center; margin-bottom: 30px;">
        <div style="display: flex; align-items: center; gap: 15px; white-space: nowrap; overflow: hidden;">
            <img src="data:image/png;base64,{encoded}" width="50"/>
            <span style="font-size: 2.2rem; font-weight: bold;">Jewellery Discount Analysis Dashboard</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Load data
@st.cache_data
def load_data():
    try:
        # Load OneDrive shared link from secrets
        onedrive_url = st.secrets["onedrive"]["download_url"]

        # Make request with redirect enabled
        response = requests.get(onedrive_url, allow_redirects=True)
        response.raise_for_status()

        # Check Content-Type (optional, just informative)
        content_type = response.headers.get("Content-Type", "")
        st.info(f"Downloaded content type: {content_type}")

        # Read Excel content from response
        df = pd.read_excel(io.BytesIO(response.content))
        st.success(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        return df

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

# ✅ Call the function and handle fallback
df = load_data()

if df.empty:
    st.error("⚠️ Data is empty or failed to load.")
    st.stop()

# Dropdown 1: Select Analysis Type
analysis_type = st.selectbox(
    "Select Analysis Type:",
    ["Quantitative Analysis", "Qualitative Analysis", "Multivariate Analysis", "Time Series Analysis","Facts and Figures"]
)
#if analysis_type == "Facts & Figures":
    #show_facts_and_figures("DiscAnSamp.xlsx")  # or pass the DataFrame if already loaded

# Dropdown 2: Select Plot (based on selected analysis type)
if analysis_type == "Quantitative Analysis":
    plot_options = [
        "1. Quantity vs Discount",
        "2. Value vs Discount",
        "3. Weight vs Discount",
        "4. Making Charges vs Discount",
        "5. Gold Price vs Discount",
        "6. Stone Value vs Discount",
        "7. Idisc, Obdisc, Ghsdisc vs Discount",
        "8. Price Band vs Discount",
        "9. Total EC Band vs Average Discount",
        "10. Cluster EC Band vs Discount"
    ]
    selected_plot = st.selectbox("Select Quantitative Plot:", plot_options)

    # 1. Quantity vs Discount
    if selected_plot == plot_options[0]:
        df_plot = df[(df['qty'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'qty', "Quantity")

    # 2. Value vs Discount
    elif selected_plot == plot_options[1]:
        df_plot = df[(df['value'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'value', "Total Bill Value")

    # 3. Weight vs Discount
    elif selected_plot == plot_options[2]:
        df_plot = df[(df['wt'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'wt', "Weight")

    # 4. Making Charges vs Discount
    elif selected_plot == plot_options[3]:
        df_plot = df[(df['mc'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'mc', "Making Charges")

    # 5. Gold Price vs Discount
    elif selected_plot == plot_options[4]:
        df_plot = df[(df['goldprice'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'goldprice', "Gold Price")

    # 6. Stone Value vs Discount
    elif selected_plot == plot_options[5]:
        df_plot = df[(df['stonevalue'] > 0) & (df['discount'] > 0)]
        quantitative.plot_and_insight(df_plot, 'stonevalue', "Stone Value")

    # 7. Idisc, Obdisc, Ghsdisc vs Discount (Bar Chart)
    elif selected_plot == plot_options[6]:
        import matplotlib.pyplot as plt

        df_plot = df[
            (df['discount'] > 0) &
            ((df['idisc'] > 0) | (df['ghsdisc'] > 0) | (df['obdisc'] > 0))
        ]

        discount_total = df_plot['discount'].sum()
        idisc_total = df_plot['idisc'].sum()
        obdisc_total = df_plot['obdisc'].sum()
        ghsdisc_total = df_plot['ghsdisc'].sum()

        labels = ['IDISC (Item Level)', 'OBDISC (Other Bill)', 'GHSDISC (Gold Harvest Scheme)']
        values = [idisc_total, obdisc_total, ghsdisc_total]
        percents = [val / discount_total for val in values]
        percent_labels = [f"{p:.1%}" for p in percents]

        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(labels, values, color=['#4C72B0', '#55A868', '#C44E52'])
        ax.set_title("Discount Share", fontsize=14)
        ax.set_xlabel("₹ Value")

        for bar, percent, label in zip(bars, percents, percent_labels):
            width = bar.get_width()
            x_position = width - 0.02 * discount_total if percent > 0.1 else width + 0.01 * discount_total
            align = 'right' if percent > 0.1 else 'left'
            ax.text(x_position, bar.get_y() + bar.get_height() / 2, label,
                    va='center', ha=align, fontsize=10, color='white' if percent > 0.1 else 'black')

        plt.tight_layout()
        st.pyplot(fig)

        # Reuse the same filtered df_plot
        quantitative.plot_and_insight(df_plot, 'discount', "Discount Share")

    # 8. Price Band vs Discount
    elif selected_plot == plot_options[7]:
        df_plot = df[df['priceband'].notnull()].copy()
        df_plot['priceband'] = df_plot['priceband'].astype(str).str.strip().str.upper()
        df_plot = df_plot[~df_plot['priceband'].isin(['NIL', 'NULL']) & (df_plot['discount'] > 0)]
        df_plot = df_plot.groupby('priceband')['discount'].mean().reset_index().sort_values(by='discount', ascending=False)
        qualitative.plot_and_insight(df_plot, 'priceband', "Price Band")

    # 9. Total EC Band vs Average Discount
    elif selected_plot == plot_options[8]:
        df_plot = df[(df['discount'] > 0) & (df['totalecband'].str.lower() != 'nil')].copy()
        quantitative.plot_and_insight(df_plot, 'totalecband', "Total EC Band")

    # 10. Cluster EC Band vs Discount
    elif selected_plot == plot_options[9]:
        df_plot = df.copy()
        df_plot['clusterecband'] = df_plot['clusterecband'].astype(str).str.strip().str.upper()
        invalid = ['[NULL]', 'NULL', 'NIL', 'NA', '', 'NONE']
        df_plot = df_plot[(df_plot['discount'] > 0) & (~df_plot['clusterecband'].isin(invalid))]
        df_plot['clusterecband'] = pd.Categorical(df_plot['clusterecband'], categories=sorted(df_plot['clusterecband'].unique()), ordered=True)
        quantitative.plot_and_insight(df_plot, 'clusterecband', "Cluster EC Band")


elif analysis_type == "Qualitative Analysis":
    plot_options = [
        "1. Brand vs Discount",
        "2. Region vs Discount",
        "3. Level vs Discount",
        "4. Retail Cluster vs Discount",
        "5. Product Category vs Discount",
        "6. AMCB vs Discount",
        "7. Daily Discount Trend",
        "8. Price Band vs Discount"
    ]
    selected_plot = st.selectbox("Select Qualitative Plot:", plot_options)

    # Call exact code blocks from combined.py
    if selected_plot == plot_options[0]:
        df_plot = df[(df['discount'] > 0) & (df['brand'].notnull())]
        df_plot = df_plot.groupby('brand')['discount'].mean().reset_index().sort_values(by='discount', ascending=False)
        qualitative.plot_and_insight(df_plot, 'brand', "Brand")
    elif selected_plot == plot_options[1]:
        df_plot = df[(df['discount'] > 0) & (df['region'].notnull())]

        #  Standardize region names
        df_plot['region'] = df_plot['region'].astype(str).str.strip().str.upper()

        #  Group and sort
        df_plot = (
            df_plot.groupby('region')['discount']
            .mean()
            .reset_index()
            .sort_values(by='discount', ascending=False)
        )
        qualitative.plot_and_insight(df_plot, 'region', "Region")
    elif selected_plot == plot_options[2]:
        df_plot = df[(df['discount'] > 0) & (df['level'].notnull())]
        df_plot = df_plot.groupby('level')['discount'].mean().reset_index().sort_values(by='discount', ascending=False)
        qualitative.plot_and_insight(df_plot, 'level', "Level")
    elif selected_plot == plot_options[3]:
        df['rcluster'] = df['rcluster'].astype(str).str.strip().str.upper()
        invalid = ['NULL', 'NIL', 'NA', '', '[NULL]']
        df_plot = df[(df['discount'] > 0) & (~df['rcluster'].isin(invalid))]
        df_plot = df_plot.groupby('rcluster')['discount'].mean().reset_index().sort_values(by='discount', ascending=False)
        qualitative.plot_and_insight(df_plot, 'rcluster', "Retail Cluster")
    elif selected_plot == plot_options[4]:
        df['totcategory'] = df['totcategory'].astype(str).str.strip().str.title()
        invalid = ['Null', 'Nil', '', '[Null]', 'Na']
        df_plot = df[(df['discount'] > 0) & (~df['totcategory'].isin(invalid))]
        df_plot = df_plot.groupby('totcategory')['discount'].mean().reset_index().sort_values(by='discount', ascending=False)
        qualitative.plot_and_insight(df_plot, 'totcategory', "Product Category")
    elif selected_plot == plot_options[5]:
        df_plot = df[df['amcb'].notnull()].copy()
        df_plot['amcb'] = df_plot['amcb'].astype(str).str.strip().str.upper()
        valid_bands = ["A(1-10%)", "B(11-14%)", "C(14-18%)", "D(18-24%)", "E(24-30%)", "F(30%+)"]
        df_plot = df_plot[df_plot['amcb'].isin(valid_bands) & (df_plot['discount'] > 0)]
        df_plot = df_plot.groupby('amcb')['discount'].mean().reset_index()
        qualitative.plot_and_insight(df_plot, 'amcb', "AMCB Band", category_order=valid_bands)
    elif selected_plot == plot_options[6]:
        df_plot = df.copy()
        df_plot['docdate'] = pd.to_datetime(df_plot['docdate'], errors='coerce')
        df_plot = df_plot.dropna(subset=['docdate', 'discount'])

        # Group by day of month (1–31)
        df_plot['day'] = df_plot['docdate'].dt.day
        df_daily = df_plot.groupby('day')['discount'].mean().reset_index()

        # Plot
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_daily['day'], df_daily['discount'], marker='o', linestyle='-', color='blue')
        ax.set_title("Average Discount by Day of Month")
        ax.set_xlabel("Day of Month (1–31)")
        ax.set_ylabel("Average Discount")
        
        # ✅ Force all days 1–31 to show on x-axis
        ax.set_xticks(range(1, 32))

        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        st.pyplot(fig)

        # Insights
        qualitative.plot_and_insight(df_daily, 'day', "Day of Month", chart_type="line")

    elif selected_plot == plot_options[7]:
        st.markdown("### 📊 Quantity Sold vs Avg. Making Charges by Discount Bucket")

        import matplotlib.pyplot as plt
        import numpy as np

        # Create discount buckets
        df['discount_bucket'] = pd.cut(
            df['discount'],
            bins=[-1, 5, 10, 15, 20, 25, 30, 50, 100],
            labels=['0–5%', '5–10%', '10–15%', '15–20%', '20–25%', '25–30%', '30–50%', '50–100%']
        )

        # Aggregate data
        grouped = df.groupby('discount_bucket').agg({
            'qty': 'sum',
            'mc': 'mean'
        }).reset_index()

        # Set discount bucket order
        ordered_cats = ['0–5%', '5–10%', '10–15%', '15–20%', '20–25%', '25–30%', '30–50%', '50–100%']
        grouped['discount_bucket'] = pd.Categorical(grouped['discount_bucket'], categories=ordered_cats, ordered=True)
        grouped = grouped.sort_values('discount_bucket')

        # Plotting
        x = np.arange(len(grouped))  # label locations
        width = 0.35  # bar width

        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, grouped['qty'], width, label='Total Quantity Sold', color='mediumseagreen')
        bars2 = ax.bar(x + width/2, grouped['mc'], width, label='Avg. Making Charges (₹)', color='cornflowerblue')

        # Labels and formatting
        ax.set_xlabel('Discount Bucket')
        ax.set_ylabel('Value')
        ax.set_title('Total Quantity vs Avg. Making Charges by Discount Bucket')
        ax.set_xticks(x)
        ax.set_xticklabels(grouped['discount_bucket'])
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Add labels on bars
        for bar in bars1:
            ax.annotate(f'{int(bar.get_height())}',
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

        for bar in bars2:
            ax.annotate(f'{int(bar.get_height())}',
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

        st.pyplot(fig)

# ...
# --- Multivariate Analysis ---
elif analysis_type == "Multivariate Analysis":

    multivariate_plot_labels = {
        "Plot 1": "1.Top 20 Discounts by Location",
        "Plot 2": "2.Return Rate: With vs Without Discount",
        "Plot 3": "3.Average Discount for New vs Existing Customers",
        "Plot 4": "4.Discount vs Day and Gold Price",
        "Plot 5": "5.Correlation of Discounts with Numeric Variables",
        "Plot 6": "6.Top 50 Customers by Avg Discount",
        "Plot 7": "7.Avg Discount by Region, Brand",
        "Plot 8": "8. Avg Discount by Brand, Level & Discount",
        "Plot 9": "9. Region vs Brand: Avg Discount per Transaction",
        "Plot 10": "10. Avg Disc"
    }

    multivariate_plot_keys = list(multivariate_plot_labels.keys())
    multivariate_plot_names = list(multivariate_plot_labels.values())

    selected_mv_plot_name = st.selectbox("Select Multivariate Plot:", multivariate_plot_names)
    selected_mv_plot_key = [k for k, v in multivariate_plot_labels.items() if v == selected_mv_plot_name][0]

    multivariate.plot_and_insight(df, selected_mv_plot_key, selected_mv_plot_name)

elif analysis_type == "Time Series Analysis":
    plot_options = [
        "1.Daily Average idisc",
        "2.Daily Trend of obdisc and ghsdisc",
        "3.Average Discount % by Day of Week",
        "4.Daily Trend Of Brand",
        "5.Returned Items Trend"
    ]
    selected_plot = st.selectbox("Select a Time Series Plot", plot_options)

    plot_mapping = {
        "1.Daily Average idisc": "Plot 1",
        "2.Daily Trend of obdisc and ghsdisc": "Plot 2",
        "3.Average Discount % by Day of Week": "Plot 3",
        "4.Daily Trend Of Brand": "Plot 4",
        "5.Returned Items Trend": "Plot 5"
    }

    timeseries.plot_and_insight(df, plot_mapping[selected_plot], "Time Series")

elif analysis_type == "Facts and Figures":
    fandf.show_facts_and_figures(df)
