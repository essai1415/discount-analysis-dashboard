import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# --- Predefined insights ---
predefined_insights = {
    "brand": [
        "ZOYA: With ₹2,24,96,641 in sales from 43 orders (3 returns) and the highest average discount of ₹69,078.83, Zoya’s aggressive premium discounting strategy should be reviewed to protect brand value.",
        "TANISHQ: Leading with ₹92,91,08,222 in sales from 8203 orders (349 returns) and a moderate average discount of ₹10,639.73, Tanishq balances mass appeal with scale but must address its return rate.",
        "MIA: Mia generated ₹5,13,79,544 in sales from 1652 orders (68 returns) at an average discount of ₹2,491.51, indicating solid traction but potential gaps in customer satisfaction.",
        "ECOM: ECOM saw ₹44,81,756 in sales from 102 orders with zero returns and the lowest average discount of ₹194.82, reflecting stable performance with scope for market expansion."
    ],
    "region": [
        "NORTH 3 recorded the highest average discount per transaction at **₹12,929.92 over 449 transactions, with ₹5.08 Cr in total sales**.",
        "SOUTH had the lowest average discount per transaction at ₹194.82, with only ₹44.81 lakh in total bill value and 173 quantity sold.",
        "NORTH 1 achieved the highest total value of ₹14.82 Cr from 1,433 transactions, offering an average discount of ₹8,677.09 per transaction.",
        "WEST 3 showed balanced performance with ₹10.52 Cr in sales, 1,086 quantity sold, and a strong average discount per transaction of ₹9,347.51.",
        "NORTH 3 offered the highest discount-to-value ratio at 11.4%, well above WEST 1 at 7.9% and SOUTH 2 at 8.1%, reflecting deeper discounting strategy."
    ],
    "level": [
        "L1 gives the highest discount per transaction at ₹12,069, much more than L2's ₹7,167 and L3's ₹774, showing that L1 uses more discounts to attract or retain customers.",
        "L2 gives the highest total discount of ₹5.32 crore across 2,591 transactions, but the average discount per bill is ₹7,167, much lower than L1.",
        "L3 has the lowest discount per transaction at ₹774, with only 64 transactions and ₹69,694 total discount, indicating minimal discounting at this level.",
        "L2 contributes the most to revenue with ₹60.72 crore in total value, serving 4,982 unique customers.",
        "Despite fewer transactions, L2’s average bill value is ₹81,734, significantly higher than L1’s ₹12,891, showing premium purchases at that level."
    ],
    "rcluster": [
        "STUDDED cluster gives the highest discount of ₹7.71 crore across 5,624 transactions, with ₹13,709 average discount per bill, indicating heavy discounting in high-value segments.",
        "PLAIN contributes ₹89.11 lakh in discounts over 1,860 bills, with an average bill value of ₹1.81 lakh, reflecting large-ticket purchases with moderate per-bill discounts of ₹4,791.",
        "COINS cluster shows very low discounting with ₹21,360 total discount across 171 transactions, averaging just ₹125 per bill, despite a high average bill value of ₹79,520.",
        "SILVER and SILVER COINS clusters have nearly zero discounting, showing either non-negotiated pricing or low priority segments, with average bills under ₹4,000.",
        "OTHERS cluster has only 3 transactions and no discount, likely indicating either negligible demand or an area to investigate for growth or phase-out."
    ],
    "totcategory": [
        "DIA category leads with ₹39.3 Cr in sales across 3,156 transactions, but also gives the highest total discount of ₹5.84 Cr, with an average discount of ₹18,506 per transaction.",
        "SSB shows the highest average discount per transaction at ₹58,200, despite only 24 transactions.",
        "SSC offers the second-highest average discount of ₹66,176 over just 11 transactions, signaling a possible luxury or niche segment needing tighter discount control.",
        "LCG and SIL have the lowest average discounts of ₹1,847 and ₹499 respectively.",
        "SSA’s average discount of ₹21,513 across 163 bills marks it as a mid-volume but high-discount category."
    ],
    "amcb": [
        "Band F (30%+) had the highest average discount per transaction at ₹10,861 across 251 transactions, totaling a discount of ₹27.26 lakhs.",
        "Band E (24–30%) contributed the highest total discount of ₹31.98 lakhs over 768 transactions, with an average discount of ₹4,164.",
        "Band D (18–24%) recorded the maximum number of transactions (1,040) with a total discount of ₹26.98 lakhs and an average discount of ₹2,595.",
        "Band C (14–18%) served as a mid-tier group, delivering ₹5.12 lakhs in total discount across 219 transactions, averaging ₹2,337 per transaction.",
        "Band A (1–10%) and B (11–14%) combined accounted for just ₹2.54 lakhs in total discount across 307 transactions, with average discounts of ₹516 and ₹1,032 respectively."
    ],
    "day": [
        "Day 9 recorded the highest total discount of ₹1.13 Cr across 558 transactions, averaging ₹20,369 per transaction.",
        "Day 13 had the highest average discount per transaction at ₹23,118 with a total discount of ₹89.93 lakhs across 389 transactions, reflecting deep discounting.",
        "A peak discounting streak occurred from Day 9 to Day 13, totaling over ₹4.15 Cr in discounts across 2,465 transactions, with daily average discounts exceeding ₹13K.",
        "Day 12 had the most transactions (648) with a total discount of ₹1.10 Cr and an average discount of ₹16,912, highlighting strong footfall and generous offers.",
        "In contrast, Day 6 saw the lowest total discount of ₹3.74 lakhs and lowest average discount per transaction of ₹2,616 over 143 transactions",
        "Use these daily patterns to optimize calendar planning, ensuring peak days align with customer buying behavior."
    ]
}

def plot_and_insight(df_plot, x_col, x_label, chart_type="bar", category_order=None):
    with st.container():
        skip_plot = chart_type == "line" and x_col in ["day", "docdate"]

        if not skip_plot:
            fig, ax = plt.subplots(figsize=(14, 6))  # Wider for spacing

            # Group and aggregate
            grouped_df = df_plot.groupby(x_col).agg({
                'discount': ['sum', 'count']
            }).reset_index()

            # Flatten column names
            grouped_df.columns = [x_col, 'total_discount', 'transactions']
            grouped_df['avg_discount_per_transaction'] = (
                grouped_df['total_discount'] / grouped_df['transactions']
            )

            # Sort if needed
            grouped_df.sort_values('avg_discount_per_transaction', ascending=False, inplace=True)

            # Order categories if provided
            if category_order:
                grouped_df[x_col] = pd.Categorical(
                    grouped_df[x_col], categories=category_order, ordered=True
                )

            if chart_type == "bar":
                sns.barplot(
                    data=grouped_df,
                    x=x_col,
                    y='avg_discount_per_transaction',
                    palette='Set2',
                    ax=ax,
                    width=0.6  # narrower bars
                )

                ax.set_title(f"{x_label} vs Discount")
                ax.set_xlabel(x_label)
                ax.set_ylabel("Avg Discount per Transaction")

                # Keep labels straight and add spacing
                ax.set_xticklabels(grouped_df[x_col], rotation=0, ha='center')

                # Add grid for better readability
                ax.grid(axis='y', linestyle='--', alpha=0.5)

                # More spacing between bars if still crowded
                ax.set_xlim(-1, len(grouped_df))

            st.pyplot(fig)



    # === Summary Table Section (Varies by x_col) ===
    if x_col == "brand":
        summary_df = pd.DataFrame({
            "Brand": ["ZOYA", "TANISHQ", "MIA", "ECOM"],
            "Total Purchase Value": ["₹2,24,96,641", "₹92,91,08,222", "₹5,13,79,544", "₹44,81,756"],
            "Average Discount": ["₹69078.83", "₹10639.73", "₹2491.51", "₹194.82"],
            "Number Of Transactions": [43, 8203, 1652, 102],
            "Number Of Returns": [3, 349, 68, 0]
        })
        st.markdown("### Brand Wise Discount and Sales Summary")
        st.dataframe(summary_df, use_container_width=True)

    elif x_col == "region":

        summary_df = pd.DataFrame({
            'Region': [
        'EAST 1', 'EAST 2', 'NORTH 1', 'NORTH 2', 'NORTH 3', 'NORTH 4',
        'SOUTH', 'SOUTH 1', 'SOUTH 2', 'SOUTH 3',
        'WEST 1', 'WEST 2', 'WEST 3'
        ],
        'Total Quantity': [815, 431, 1487, 765, 533, 281, 173, 1182, 1055, 759, 1012, 654, 1086],
        'Total Value': [
            67699482.72, 37787723.15, 148204645.6, 67367585.32, 50807455.71, 33491470.55,
            4481756.8, 112464448.2, 103160438.4, 79628972.6, 90599043, 62617582.51, 105158735.1
        ],
        'Total Discount': [
            6662382.45, 2438974.51, 12434273.68, 5473230.09, 5805535.28, 2916113.66,
            19871.79, 10100324.39, 8356264.83, 8382270.74, 7189964.02, 6096741.98, 10198129.82
        ],
        'Item Level Discount': [
            6812175.8, 2462342.07, 12634347.92, 5619712.34, 5961781.36, 3068542.61,
            8734.91, 10279468.31, 8658641.33, 8839666.69, 7514638.84, 6652231.45, 10435993.02
        ],
        'Other Bill Level Discount': [
            38220.61, 38369.63, 142249.09, 31931.08, 56635.33, 17601.99,
            11136.88, 162978.27, 45693.9, 36040.53, 63684.95, 33621.52, 115380.15
        ],
        'GHS Discount': [
            47678.31, 1664.12, 77467.77, 17822.82, 47403.62, 40515.33,
            0.0, 5301.72, 53260.88, 40266.15, 84533.77, 32793.51, 37450.46
        ],
        'Transaction Count': [861, 375, 1433, 754, 449, 279, 102, 1153, 1043, 766, 1020, 674, 1091],
        'Avg Discount per Transaction': [
            7737.96, 6503.93, 8677.09, 7258.93, 12929.92, 10452.02,
            194.82, 8760.04, 8011.76, 10942.91, 7048.98, 9045.61, 9347.51
        ]
        })

        summary_df["Total Discount"] = summary_df["Total Discount"].round(2)

        # Display in Streamlit
        st.markdown("### Region Wise Discount Summary")
        st.dataframe(summary_df, use_container_width=True)


   
    elif x_col == "level":
        summary_df = pd.DataFrame({
            "Channel Level": ["L1", "L2", "L3"],
            "Number Of Transactions": ["7345", "2591","64"],
            "Total Discount": [32755832.68, 53248549.69, 69694.87],
            "Item Level Discount": [32372257.72, 52668474.57, 51452.5],
            "Other Bill Discount": [223147.65, 325675.34, 18242.37],
            "GHS Discount": [160427.31, 254399.78, 0.0],
            "Total Value": [349866065.4, 607203290.3, 6399983.98],
            "Total Quantity": [2714, 7429, 90],
            "Unique Customers": [1680, 4982, 55],
            "Avg Discount per Transaction": [12069.21, 7167.66, 774.39],
            "Avg Bill Value": [128911.59, 81734.19, 71110.93]
        })
        st.markdown("### Channel Level Discount Summary")
        st.dataframe(summary_df, use_container_width=True)


    elif x_col == "rcluster":
        summary_df = pd.DataFrame({
            "Rcluster": [
                "COINS", "OTHERS", "PLAIN", "SILVER", "SILVER COINS", "STUDDED"
            ],
            "Total Discount": [
                21359.96, 0.00, 8911067.64, 32453.07, 0.00, 77101986.58
            ],
            "Item Level Discount": [
                0.00, 0.00, 8452455.88, 28527.27, 0.00, 76611201.64
            ],
            "Other Bill Discount": [
                17216.15, 0.00, 329205.21, 3791.08, 0.00, 216852.92
            ],
            "GHS Discount": [
                4143.81, 0.00, 129406.55, 134.72, 0.00, 273932.02
            ],
            "Total Value": [
                13598009.22, 2000.03, 337689817.5, 608735.02, 18868.96, 610659333.8
            ],
            "Total Quantity": [
                362, 5, 2634, 261, 18, 6926
            ],
            "Unique Customers": [
                167, 3, 1827, 156, 7, 5348
            ],
            "Transactions": [
                171, 3, 1860, 159, 7, 5624
            ],
            "Avg Discount per Transaction": [
                124.91, 0.00, 4790.90, 204.11, 0.00, 13709.46
            ],
            "Avg Bill Value": [
                79520.52, 666.68, 181553.67, 3828.52, 2695.57, 108580.96
            ]
        })
        
        st.markdown("### Retail Cluster Wise Discount Summary")
        st.dataframe(summary_df, use_container_width=True)
    
    elif x_col == "totcategory":
        summary_df = pd.DataFrame({
            "Totcategory": [
                "Dia", "Gis", "Hcg", "Mcg", "Ssa", "Ssb",
                "Scs", "Ssc", "Lcg", "Sil", "Coi", "Puc"
            ],
            "Number of Transactions": [
                3156, 1786, 446, 711, 163, 24,
                266, 11, 185, 65, 11, 1
            ],
            "Total Value": [
                393096982.37, 147589795.61, 135376975.37, 153323449.42,
                28314548.69, 11001817.90, 34336240.01, 7320498.16,
                19824290.46, 238156.95, 455156.66, 435.12
            ],
            "Total Discount": [
                58405565.80, 15130955.23, 4813579.53, 4153287.23,
                3506751.70, 1396807.24, 1054543.16, 727938.68,
                341831.15, 32453.07, 28569.95, 746.95
            ],
            "Avg Discount per Transaction": [
                18506.20, 8471.98, 10792.78, 5841.47,
                21513.81, 58200.30, 3964.45, 66176.24,
                1847.74, 499.28, 2597.27, 746.95
            ]

        })

        st.markdown("### Category Wise Discount Summary")
        st.dataframe(summary_df, use_container_width=True)

    elif x_col == "amcb":
        summary_df = pd.DataFrame({
            "amcb": [
                "A(1-10%)", "B(11-14%)", "C(14-18%)", "D(18-24%)", "E(24-30%)", "F(30%+)"
            ],
            "Total Discount": [
                62939.91, 191008.71, 511888.25, 2698294.09, 3197886.80, 2726240.52
            ],
            "Number_of_Transactions": [
                122, 185, 219, 1040, 768, 251
            ],
            "Avg_Discount_Per_Transaction": [
                515.900902, 1032.479514, 2337.389269, 2594.513548, 4163.915104, 10861.516016
            ]
        })
        st.markdown("### AMCB Wise Discount Summary")
        st.dataframe(summary_df, use_container_width=True)
    
    elif x_col == "day":
        summary_df = pd.DataFrame({
            "day": list(range(1, 32)),
            "Total_Discount": [
                1420306.24, 582575.98, 1063480.17, 866539.52, 847466.31, 374037.67, 425582.60, 520665.78,
                11365679.41, 5192091.14, 7702931.59, 10959293.60, 8993057.49, 1427623.75, 1102635.56,
                2671087.46, 1780942.74, 2350864.29, 3593751.71, 2469501.13, 1232222.98, 2174111.03,
                2017899.51, 3489018.98, 3059254.38, 2831791.79, 2018189.55, 1651802.01, 1313240.32,
                1509318.90, 3167567.17
            ],
            "Number_of_Transactions": [
                357, 155, 183, 278, 296, 143, 121, 150, 558, 388, 482, 648, 389, 275, 240, 295, 307,
                253, 557, 272, 221, 264, 252, 323, 421, 458, 258, 237, 230, 261, 362
            ],
            "Avg_Discount_Per_Transaction": [
                3978.448852, 3758.554710, 5811.367049, 3117.048633, 2863.061858, 2615.648042,
                3517.211570, 3471.105200, 20368.601093, 13381.678196, 15981.185871, 16912.490123,
                23118.399717, 5191.359091, 4594.314833, 9054.533763, 5801.116417, 9291.953715,
                6451.977935, 9079.048272, 5575.669593, 8235.269053, 8007.537738, 10801.916347,
                7266.637482, 6182.951507, 7822.440116, 6969.628734, 5709.740522, 5782.831034,
                8750.185552
            ]
        })
        st.markdown("### Day of Month Discount Summary")
        st.dataframe(summary_df, use_container_width=True)




    # Add similar elif blocks for totcategory, amcb, priceband, level, day, etc.

    # --- Toggle Logic for Insights ---
    toggle_key = f"show_insights_{x_col}"
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = False

    def toggle():
        st.session_state[toggle_key] = not st.session_state[toggle_key]

    button_label = "Hide Detailed Business Insights" if st.session_state[toggle_key] else "Show Detailed Business Insights"
    st.button(button_label, key=f"toggle_button_{x_col}", on_click=toggle)

    if st.session_state[toggle_key]:
        st.markdown("### Business Insights For Stakeholders")
        for insight in predefined_insights.get(x_col, [f"No insights available for {x_label}."]):
            st.markdown(f"- {insight}")
