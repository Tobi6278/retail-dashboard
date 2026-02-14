import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Retail Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

df = pd.read_csv('cleaned_retail.csv')
df = df.sort_values(by="Category")
df = df[['Category', 'Item', 'Price Per Unit', 'Quantity', 'Total Spent']]

category_type = st.sidebar.multiselect(
    "Select a Category:",
    options  = df['Category'].unique(),
    default= df['Category'].unique()
)

df_selection = df.query(
    "Category == @category_type"
)


#MAIN PAGE

st.title(":chart_with_upwards_trend: Retail Store Data")
st.markdown("---")

total_sales = int(df_selection['Total Spent'].sum()) if not df_selection.empty else 0
average_cost_per_unit = round(df_selection['Price Per Unit'].mean(), 1) if not df_selection.empty else 0

if not df_selection.empty and not df_selection['Item'].mode().empty:
    mode_item = df_selection['Item'].mode()[0]
else:
    mode_item = "N/A"

columns = st.columns(3)

with columns[0]:
    st.markdown("<p style='font-size:16px;'>Total Sales:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:20px;'>US $ {total_sales:,}</p>", unsafe_allow_html=True)

with columns[1]:
    st.markdown("<p style='font-size:16px;'>Average Cost/Unit:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:20px;'>US $ {average_cost_per_unit:,}</p>", unsafe_allow_html=True)

with columns[2]:
    st.markdown("<p style='font-size:16px;'>Most Bought Item:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:20px;'>{mode_item}</p>", unsafe_allow_html=True)

if not df_selection.empty:
    revenue_by_category = df_selection.groupby('Category')['Total Spent'].sum().sort_values(ascending=False)
else:
    revenue_by_category = pd.Series(dtype=float)

if not revenue_by_category.empty:
    fig, ax = plt.subplots(figsize=(6,4))
    revenue_by_category.plot(kind='bar', ax=ax, color='skyblue', width=0.6)
    ax.set_title("Total Revenue by Category", fontsize=14)
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Total Revenue", fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)
else:
    st.info("Select at least one category to see the bar chart.")
