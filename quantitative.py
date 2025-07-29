import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Predefined insights by feature
predefined_insights = {
    "qty": [
        "Correlation between quantity and discount is just **0.07**, indicating no meaningful relationship.",
        "Customers purchasing more items are not necessarily rewarded with higher discounts.",
        "Over **80%** of high-value discounts are given for quantities between 1 and 3.",
        "High-quantity buyers may not feel incentivized to increase their purchase volume.",
        "Encourage customers to buy more by offering clear, attractive discounts when they purchase multiple jewelry pieces together."
    ],
    "value": [
        "There's a very strong positive correlation (0.81) between item value and discount, meaning higher-value items consistently receive higher discounts.",
        "The average discount on high-value items (> ₹43,804) is ₹17,155, while low-value items receive barely ₹59, a 290x difference.",
        "In nearly ***80% of the sales***, when the value of an item went up, the discount also went up — showing that costlier items are regularly given bigger discounts.",
        "All top 5 highest-value transactions belong to the DIA (Diamond) category, with discounts exceeding ₹3.8 lakhs",
        "This pattern shows an opportunity to improve how discounts are given on diamonds, so the business can protect margins and avoid losing too much profit."
    ],
    "wt": [
        "There’s a moderate connection **(r=0.43)** when jewellery is heavier, it usually gets a bigger discount, but not always.",
        "Higher Discounts on Heavier Items, On average, heavy-weight items receive ₹15,845.21 in discounts vs just ₹1,372.50 for lighter ones.",
        "Around **67%** of the data supports the idea that heavier items get more discount.",
        "The heaviest item weighed **215.75g**, and the biggest discount given was **₹87,648**.",
        "But the pattern isn’t perfect, Out of the 5 heaviest items, only 3 actually got big discounts."
    ],
    "mc": [
        "A strong correlation **(r = 0.74)** shows that higher making charges often lead to higher discounts.",
        "There are **371 transactions** with discounts above **₹50,000**, indicating frequent high-value discounting.",
        "A total of 835 products had making charges over ₹50,000, suggesting a focus on premium jewellery.",
        "Deep discounts above ₹1,00,000 were given 142 times, which could significantly impact margins.",
        "Making charges range from ₹153 to ₹6,35,241 and discounts from ₹0.1 to ₹9,19,871.16, showing large variation in pricing strategy.",
        "This pattern suggests an opportunity to highlight premium pieces through targeted discounts on making charges."
    ],
    "goldprice": [
        "Band 10 alone got **₹4.64 Cr** in discounts, nearly **45.08% of total discount value**.",
        "Bands 9 and 10 together received **₹6.46 Cr**, covering over **70% of all discounts**.",
        "Bands 1 to 4 received only **₹80.8 Lakhs in total**, despite having similar order volumes.",
        "Average discount per transaction rises steeply from **₹744 in Band 1 to ₹43,147 in Band 10**",
        "Optimizing Bands 9–10 discounts and upselling in Bands 5–7 can improve profits."
    ],
    "stonevalue": [
        "There is an extremely strong positive correlation between stone value and discount **(r=0.91)**, indicating a direct and consistent relationship.",
        "**SSC, SSB, and SSA** have only **217 transactions** but extremely high average stone values **(₹6.13L, ₹3.29L, ₹1.20L)**.",
        "**DIA and GIS**, with **6,281 transactions**, contribute consistently with moderate average stone values of **₹49.5K and ₹25.8K**.",
        "**MCG and LCG** show very low average stone values **(₹95.06 and ₹1.65)** despite **1,877 transactions**, indicating low-value or stone-absent products.",
        "**COI, PUC, and SIL** record **380 transactions** with ₹0 average stone value, suggesting non-stone categories",
        "Because stone values vary a lot by category, each group needs its own pricing and marketing plan, and also it should be ensured that the margins are not overly impacted on high-stone-value items."
    ],
    "discount": [
        "Item-level discounts (IDISC) account for a massive 98.6% of all discounts, showing that most savings are applied directly on individual jewelry pieces.",
        "Other bill-level discounts (OBDISC) contribute less than 1%, indicating they play a very minimal role in the current pricing strategy.",
        "Gold harvest scheme discounts (GHSDISC) make up just 0.5%, suggesting such programs are either rarely used or have limited impact.",
        "The discount structure is heavily dependent on item-level pricing, which simplifies operations but may limit strategic flexibility.",
        "Expanding the use of bill-level or scheme-based discounts could offer new levers for promotions or targeted campaigns."
    ],
    "priceband": [
        "Lower bands A to D (0–2L) account for 8,432 transactions and ₹29.4 Cr in discounts, showing where most volume and discount spend is concentrated.",
        "High-value bands from E (2–3L) to G (4–5L) have fewer transactions (902) but steep average discounts, ranging from ₹22.5K to ₹48.2K per order.",
        "Ultra-premium bands K to O (₹8L+) have only 93 transactions but receive extremely high average discounts — up to ₹5.3 Lakhs per order which might heavily impact margins",
        "Average discount per transaction jumps from ₹633 in Band A to ₹5.3L in Band O, showing a sharp increase with price.",
        "Bands M to O (₹12L+) gave out ₹10.7 Cr in discounts over just 33 transactions, suggesting a need to review high-ticket discount policies."
    ],
    "totalecband": [
        "Bands A to C (₹0–2L) have 6,930 transactions with ₹19.5 Cr in discounts, showing strong volume at lower to mid-range prices.",
        "Band E (₹3–5L) alone contributed ₹13.13 Cr across 749 transactions, with a high average discount of ₹17,527",
        "Band F (₹5–8L) shows rising value with 481 transactions and ₹1.01 Cr in discounts, averaging ₹21,072 per transaction.",
        "Band G (₹8–10L) has fewer orders (231) but a steep average discount of ₹40,804, indicating margin pressure in upper-mid range sales.",
        "Band H (₹10L+) gave out ₹3.14 Cr in discounts across 501 transactions, with the highest average discount of ₹62,768, needing careful control on high-end promotions."
    ],
    "clusterecband": [
        "Bands A to C (₹0–2L) cover 6,872 transactions with ₹20.3 Cr in total discounts, showing high volume but relatively lower average discounts (₹1K–₹7.4K).",
        "Band E (₹3–5L) gave ₹13.5 Cr in discounts over 685 transactions, averaging ₹19,749 per transaction — a key mid-premium segment.",
        "Band F (₹5–8L) had 392 transactions with ₹9.81 Cr in discounts, pushing the average discount to ₹25,025 per customer.",
        "Band G (₹8–10L) saw fewer sales (221) but a high average discount of ₹42,055, indicating aggressive pricing in upper bands.",
        "Band H (₹10L+) gave the highest total discount of ₹3.05 Cr with only 409 transactions, averaging ₹74,632 per order, needing tighter discount control to protect margins."
    ]
}

# Main plotting and insight function
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
            st.pyplot(fig)

        elif x_col != 'discount':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_plot, x=x_col, y='discount', palette='Set2', ax=ax)
            ax.set(title=f"Discount by {x_label}", xlabel=x_label, ylabel="Discount")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # -------------------- Static Summary Table --------------------
        st.markdown("### Summary Table")

        if x_col == "qty":
            summary_data = [
                ["Valid Records", "10,000"],
                ["Correlation Coefficient", "0.07 (Very Weak Positive)"],
                ["Most Common Qty Range", "1–2"],
                ["High Discount Given When Qty Between", "1–2"],
                ["Avg Discount (Low Qty: 1–2)", "₹4,929.15"],
                ["Avg Discount (High Qty: >5)", "₹5,296.42"],
                ["Max Discount Given", "₹42,327.08"],
                ["Min Discount Given", "₹0.03"],
                ["Trend", "18.24% of records show increase in both qty & discount"],
                ["Top Brands in Bulk Purchases", "MIA, ZOYA"]
            ]


        elif x_col == "value":
            summary_data = [
                ["Valid Records", "10,000"],
                ["Correlation Coefficient", "0.81 (Very Strong Positive)"],
                ["Avg Discount (High-Value Items)", "₹17,155.44"],
                ["Avg Discount (Low-Value Items)", "₹59.38"],
                ["Trend", "79.8% of records move in same direction"],
                ["Top Brands in High-Value Sales", "TANISHQ, ZOYA"],
                ["Top Category", "DIA (Diamond)"],
                ["Highest Discount Given", "₹919,871.16"],
                ["Highest Value Item", "₹3,762,273.04"]
            ]

        elif x_col == "wt":
            summary_data = [
                ["Valid Records", "10,000"],
                ["Correlation Coefficient", "0.43 (Moderate Positive)"],
                ["Avg Discount (High-Weight Items)", "₹15,845.21"],
                ["Avg Discount (Low-Weight Items)", "₹1,372.50"],
                ["Trend Alignment", "67.4% of records move in same direction"],
                ["Heaviest Item", "215.75g"],
                ["Highest Discount Given", "₹87,648.19"],
                ["Top Weight Items with Positive Trend", "3 out of 5"]
]


        elif x_col == "mc":
            summary_data = [
                ["Total Valid Records", 10000],
                ["Max Making Charges", 635241.00],
                ["Min Making Charges", 153.21],
                ["Max Discount", 919871.16],
                ["Min Discount", 0.10],
                ["Correlation Coefficient (r)", 0.74],
                ["Records with Discount > ₹50,000", 371],
                ["Records with MC > ₹50,000", 835],
                ["Records with Discount > ₹1,00,000", 142]
            ]

        elif x_col == "goldprice":
            summary_data = [
                ["Band", "Gold Price Range", "Number_of_Transactions", "Total_Discount", "Avg_Discount_Per_Transaction"],
                ["ALL", "ALL", "9416", "₹90,188,826.16", "₹9,573.13"],
                ["Band 1", "(6.139, 4705.239]", "942", "₹701,544.67", "₹744.74"],
                ["Band 2", "(4705.239, 8126.192]", "942", "₹1,171,522.55", "₹1,243.65"],
                ["Band 3", "(8126.192, 11159.796]", "942", "₹2,142,385.99", "₹2,274.30"],
                ["Band 4", "(11159.796, 14483.656]", "941", "₹3,860,619.45", "₹4,102.68"],
                ["Band 5", "(14483.656, 18702.65]", "942", "₹4,444,834.58", "₹4,718.51"],
                ["Band 6", "(18702.65, 25346.76]", "942", "₹5,165,705.94", "₹5,483.76"],
                ["Band 7", "(25346.76, 34897.071]", "941", "₹5,781,272.14", "₹6,143.75"],
                ["Band 8", "(34897.071, 57156.118]", "942", "₹7,986,517.43", "₹8,478.26"],
                ["Band 9", "(57156.118, 128545.746]", "942", "₹18,144,826.18", "₹19,262.02"],
                ["Band 10", "(128545.746, 1560704.77]", "942", "₹40,644,518.03", "₹43,147.05"]
            ]

        elif x_col == "stonevalue":
            summary_data = [
                ["Category", "Number of Transactions", "Avg Stone Value"],
                ["SSC", 11, "₹613,822.77"],
                ["SSB", 27, "₹328,603.27"],
                ["SSA", 179, "₹120,240.95"],
                ["DIA", 4132, "₹49,483.55"],
                ["GIS", 2149, "₹25,830.06"],
                ["SCS", 429, "₹10,229.55"],
                ["HCG", 805, "₹6,475.09"],
                ["MCG", 1512, "₹95.06"],
                ["LCG", 365, "₹1.65"],
                ["COI", 213, "₹0.00"],
                ["PUC", 1, "₹0.00"],
                ["SIL", 166, "₹0.00"]
            ]

        elif x_col == "discount":
            summary_data = [
                ["Component", "Amount (₹)", "Share (%)"],
                ["Total Discount", "86,074,077.24", "100.00"],
                ["IDISC", "85,092,184.79", "98.86"],
                ["obdisc", "567,065.36", "0.66"],
                ["GHSDISC", "414,827.09", "0.48"]
            ]

        elif x_col == "priceband":
            summary_data = [
                ["priceband", "Total_Discount", "Number_of_Transactions", "Avg_Discount_Per_Transaction"],
                ["A(0-25K)", 1694990.12, 2678, 632.931337],
                ["B(25-50K)", 4600711.79, 2501, 1839.548896],
                ["C(50-100K)", 9638369.97, 2099, 4591.886598],
                ["D(1-2L)", 13500152.65, 1154, 11698.572487],
                ["E(2-3L)", 10494410.92, 465, 22568.625634],
                ["F(3-4L)", 10444765.99, 263, 39713.939125],
                ["G(4-5L)", 8390952.71, 174, 48223.866149],
                ["H(5-6L)", 5463252.09, 101, 54091.604851],
                ["I(6-7L)", 3879915.31, 62, 62579.279194],
                ["J(7-8L)", 3715776.46, 42, 88470.868095],
                ["K(8-10L)", 6078479.92, 45, 135077.331556],
                ["L(10-12L)", 1581408.54, 15, 105427.236000],
                ["M(12-15L)", 4367709.06, 18, 242650.503333],
                ["N(15-20L)", 3140671.90, 9, 348963.544444],
                ["O(20L+)", 3182963.33, 6, 530493.888333]
            ]


        elif x_col == "totalecband":
            summary_data = [
                ["totalecband", "Total_Discount", "Number_of_Transactions", "Avg_Discount_Per_Transaction"],
                ["A(0-50K)", 3493566.36, 3290, 1061.874274],
                ["B(50-100K)", 4532868.42, 1856, 2442.278244],
                ["C(1-2L)", 11417084.56, 1784, 6399.711076],
                ["D(2-3L)", 6222261.75, 650, 9572.710385],
                ["E(3-5L)", 13127500.52, 749, 17526.702964],
                ["F(5-8L)", 10135586.65, 481, 21071.905717],
                ["G(8-10L)", 9425683.34, 231, 40803.823983],
                ["H(10L+)", 31446704.26, 501, 62767.872774]
            ]


        elif x_col == "clusterecband":
            summary_data = [
                ["clusterecband", "Total_Discount", "Number_of_Transactions", "Avg_Discount_Per_Transaction"],
                ["A(0-50K)", 3769940.30, 3502, 1076.510651],
                ["B(50-100K)", 4833260.37, 1788, 2703.165755],
                ["C(1-2L)", 11774402.33, 1582, 7442.732193],
                ["D(2-3L)", 6083833.29, 548, 11101.885566],
                ["E(3-5L)", 13527912.27, 685, 19748.777036],
                ["F(5-8L)", 9809897.01, 392, 25025.247474],
                ["G(8-10L)", 9294238.54, 221, 42055.378009],
                ["H(10L+)", 30524351.13, 409, 74631.665355]
    ]

        else:
            summary_data = [["No data available", "—"]]

        # ✅ Flexible header + dataframe rendering
        columns = summary_data[0]                   # First row is header
        data_rows = summary_data[1:]                # Rest are data
        summary_table = pd.DataFrame(data_rows, columns=columns)
        st.dataframe(summary_table, use_container_width=True)

#Ai Agent Logic

    from ai_agent import display_insight_panel

    # Safely fetch insights
    col_insights = predefined_insights.get(x_col, [f"No insights available for {x_col}."])

    # Handle summary conversion if it's a list
    if isinstance(summary_data, list) and len(summary_data) > 1:
        summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
    elif isinstance(summary_data, pd.DataFrame):
        summary_df = summary_data
    else:
        summary_df = None

    # Call AI insight panel
    display_insight_panel(
        x_col=x_col,
        predefined_insights={x_col: col_insights},
        summary_df=summary_df
    )
