import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Predefined insights by feature
predefined_insights = {
    "qty": [
        "Customers purchasing more items are not necessarily rewarded with higher discounts.",
        "The weak correlation suggests discounts are not structured around quantity bought.",
        "The discounting strategy appears to be driven more by other factors than purchase volume.",
        "High-quantity buyers may not feel incentivized to increase their purchase volume.",
        "Encourage customers to buy more by offering clear, attractive discounts when they purchase multiple jewelry pieces together."
    ],
    "value": [
        "Higher bill values consistently attract larger discounts.",
        "High value transactions receive larger discounts, suggesting a value-driven discounting strategy.",
        "High spenders are being rewarded, possibly aiding in retention.",
        "Profits on large-value items may be affected — review margin impact.",
        "Consider tiered discounting for better profit control."
    ],
    "wt": [
        "Product weight has minimal influence on discount allocation.",
        "Heavy jewellery pieces are not incentivized through current discounting.",
        "Customers buying heavier items may not feel value benefits.",
        "Opportunity exists to reward purchases of heavy, high-margin items.",
        "Introduce weight-based discount tiers to balance pricing."
    ],
    "mc": [
        "There is a strong positive correlation between making charges and discounts, indicating discounts increase as making charges rise.",
        "Customers purchasing jewelry with higher making charges tend to receive larger discounts.",
        "The discounting strategy appears to be closely tied to the craftsmanship or complexity of the jewelry.",
        "High making-charge items may be used strategically to offer attractive discounts and close high-margin sales.",
        "This pattern suggests an opportunity to highlight premium pieces through targeted discounts on making charges."
    ],
    "goldprice": [
        "There is a moderate positive correlation between gold price and discount, suggesting some influence but not a strong one.",
        "Discounts tend to increase slightly with gold price, but the relationship is not as consistent as with total bill value, stone value or making charges.",
        "Customers spending more on gold don’t always see bigger discounts, which might feel inconsistent or unclear from their perspective.",
        "This pattern hints that gold price alone may not be the main factor driving discount decisions.",
        "Making discounts more aligned with gold price changes can help customers feel the pricing is fair and transparent."
    ],
    "stonevalue": [
        "There is an extremely strong positive correlation between stone value and discount, indicating a direct and consistent relationship.",
        "As the value of stones increases, the discount offered increases proportionally, showing a highly structured pricing approach.",
        "The discounting pattern on stone-heavy jewelry appears well-structured and likely serves as a smart tactic to attract high-value, premium buyers.",
        "Customers buying high-value stone jewelry clearly benefit from better discounts",
        "Customers can trust that spending more on diamonds or other stones leads to meaningful price advantages, encouraging repeat and high-value sales.",
        "Ensure margins are not overly impacted on high-stone-value items."
    ],
    "discount": [
        "Item-level discounts (IDISC) account for a massive 98.6% of all discounts, showing that most savings are applied directly on individual jewelry pieces.",
        "Other bill-level discounts (OBDISC) contribute less than 1%, indicating they play a very minimal role in the current pricing strategy.",
        "Gold harvest scheme discounts (GHSDISC) make up just 0.5%, suggesting such programs are either rarely used or have limited impact.",
        "The discount structure is heavily dependent on item-level pricing, which simplifies operations but may limit strategic flexibility.",
        "Expanding the use of bill-level or scheme-based discounts could offer new levers for promotions or targeted campaigns."
    ],
    "priceband": [
        "Discounts clearly rise with higher price bands, especially beyond the ₹1 lakh mark, indicating a structured, tiered discounting approach.",
        "Price bands like 'O(20L+)', 'M(12-15L)', and 'N(15-20L)' show the highest median and variability in discounts, reflecting flexibility for premium buyers.",
        "Lower price bands such as 'A(0-25K)', 'C(50-100K)', and 'B(25-50K)' receive very low discounts.",
        "The spread in higher bands suggests scope for negotiation, possibly used to close high-value deals.",
        "This structure reinforces a premium customer experience, rewarding larger spends with more significant savings."
    ],
    "totalecband": [
        "Customers in band 'H' (highest EC band) consistently receive the largest discounts",
        "Bands A to C (lower EC bands) show minimal and consistent discount values.",
        "Band 'H' also shows the highest variability in discounts, which could reflect negotiations or custom offers for premium segments.",
        "Bands D to G offer moderate and fairly stable discounts.",
        "The overall trend validates that discounts scale with customer EC value."
    ],
    "clusterecband": [
        "Customers in the ‘H’ band (Cluster EC 10L+) clearly receive the highest discounts.",
        "Discount distribution for Band ‘H’ is wide.",
        "‘G’ and ‘F’ bands (8–10L & 5–8L) follow next with substantial and relatively consistent discounts.",
        "Clusters A to D (under 3L) get minimal discounts.",
        "Explore adjusting discount tiers for underperforming clusters."
    ]
}

# Main plotting and insight function
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as ticker

def plot_and_insight(df_plot, x_col, x_label):
    corr = df_plot['discount'].corr(df_plot[x_col]) if pd.api.types.is_numeric_dtype(df_plot[x_col]) else None

    with st.container():
        # Plotting first
        if x_col != 'discount' and corr is not None:
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.regplot(
                data=df_plot, x=x_col, y='discount',
                scatter_kws={'alpha': 0.6, 'color': '#3498db'},
                line_kws={'color': '#e74c3c'}, ax=ax
            )
            ax.set(title=f"{x_label} vs Discount", xlabel=x_label, ylabel="Discount")
            ax.text(0.95, 0.05, f"r = {corr:.2f}", transform=ax.transAxes, ha='right',
                    bbox=dict(boxstyle="round", fc="lightyellow"))

            # ✅ Disable scientific notation for both axes
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:,.0f}'))

            st.pyplot(fig)

        elif x_col != 'discount':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_plot, x=x_col, y='discount', palette='Set2', ax=ax)
            ax.set(title=f"Discount by {x_label}", xlabel=x_label, ylabel="Discount")
            plt.xticks(rotation=45)

            # ✅ Disable scientific notation for y-axis (discount)
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:,.0f}'))

            st.pyplot(fig)

        st.markdown("---")
        st.markdown("### Insights for Business Stakeholders")
        for insight in predefined_insights.get(x_col, [f"No predefined insights available for {x_label}."]):
            st.markdown(f"- {insight}")



