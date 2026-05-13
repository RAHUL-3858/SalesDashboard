import streamlit as st
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter))
]

# KPIs

total_revenue = filtered_df['Revenue'].sum()
total_profit = filtered_df['Profit'].sum()
total_units = filtered_df['Units Sold'].sum()

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    st.metric("Total Profit", f"₹{total_profit:,.0f}")

with col3:
    st.metric("Units Sold", f"{total_units}")

st.markdown("---")

# Revenue by Region
region_chart = px.bar(
    filtered_df.groupby('Region')['Revenue'].sum().reset_index(),
    x='Region',
    y='Revenue',
    color='Region',
    title='Revenue by Region'
)

# Revenue Trend
trend_chart = px.line(
    filtered_df.groupby('Date')['Revenue'].sum().reset_index(),
    x='Date',
    y='Revenue',
    markers=True,
    title='Revenue Trend Over Time'
)

# Top Products
product_chart = px.pie(
    filtered_df.groupby('Product')['Revenue'].sum().reset_index(),
    names='Product',
    values='Revenue',
    title='Revenue Share by Product'
)

# Layout
col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(region_chart, use_container_width=True)

with col5:
    st.plotly_chart(trend_chart, use_container_width=True)

st.plotly_chart(product_chart, use_container_width=True)

# Data Table
st.subheader("Sales Data Table")
st.dataframe(filtered_df)

# Download Button
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)