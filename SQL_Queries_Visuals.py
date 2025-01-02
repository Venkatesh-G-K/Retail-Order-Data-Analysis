


import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from sqlalchemy import create_engine

#from Test_ import *
# PostgreSQL connection setup using SQLAlchemy
def get_connection():
    connection_string = "postgresql+psycopg2://postgres:venkat@localhost:5432/mydb"
    engine = create_engine(connection_string)
    return engine

# Run query and return result as DataFrame
def run_query(query):
    engine = get_connection()
    with engine.connect() as connection:
        result = pd.read_sql_query(query, connection)
    return result

# Simplified titles for the sidebar
simplified_titles = [
    "1.Top 10 Highest Revenue Generating Products",
    "2.Top 5 Cities with Highest Profit Margins",
    "3.Total Discount by Category",
    "4.Average Sale Price per Product Category",
    "5.Region with the Highest Average Sale Price",
    "6.Total Profit per Category",
    "7.Top 3 Segments with Highest Quantity of Orders",
    "8.Average Discount Percentage per Region",
    "9.Product Category with Highest Total Profit",
    "10.Total Revenue per Year",
    "11.Top-Selling Products by Revenue",
    "12.Year-Over-Year Monthly Sales Comparison",
    "13.Best Performing Products by Revenue",
    "14.Region-Wise Performance",
    "15.Impact of Discounts on Sales",
    "16.Category Performance Metrics",
    "17.Monthly Regional Sales Analysis",
    "18.Revenue from Discounted Sales",
    "19.Top 10 cities by sales",
    "20.Top 10 state by profit",
]

# Corresponding SQL queries
query_options = [
    ("1.Top 10 Highest Revenue Generating Products", """
        SELECT product_id, sale_price 
        FROM product
        ORDER BY sale_price DESC
        LIMIT 10;
    """),

    ("2.Top 5 Cities with Highest Profit Margins", """
        SELECT s.city, SUM(p.profit) as total_profit
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY s.city
        ORDER BY total_profit DESC
        LIMIT 5;
    """),

    ("3.Total Discount by Category", """
        SELECT category, SUM(discount) as total_discount
        FROM product
        GROUP BY category
        ORDER BY total_discount DESC;
    """),

    ("4.Average Sale Price per Product Category", """
        SELECT category, AVG(sale_price) as average_sale_price
        FROM product
        GROUP BY category
        ORDER BY average_sale_price;
    """),

    ("5.Region with the Highest Average Sale Price", """
        SELECT s.region
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY s.region
        ORDER BY AVG(p.sale_price) DESC
        LIMIT 1;
    """),

    ("6.Total Profit per Category", """
        SELECT category, SUM(profit) as total_profit
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY category
        ORDER BY total_profit DESC;
    """),

    ("7.Top 3 Segments with Highest Quantity of Orders", """
        SELECT segment, SUM(quantity) as total_quantity
        FROM shipment s
        JOIN product p ON p.order_id = s.order_id
        GROUP BY segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    """),

    ("8.Average Discount Percentage per Region", """
        SELECT region, AVG(discount_percent) as avg_discount
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY region
        ORDER BY avg_discount DESC;
    """),

    ("9.Product Category with Highest Total Profit", """
        SELECT category, SUM(profit) as total_profit
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY category
        ORDER BY total_profit DESC
        LIMIT 1;
    """),

    ("10.Total Revenue per Year", """
        SELECT EXTRACT(YEAR FROM order_date::DATE) AS year, SUM(sale_price) AS total_revenue
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY year
        ORDER BY total_revenue DESC;
    """),

    ("11.Top-Selling Products by Revenue", """
        SELECT product_id, SUM(sale_price) as total_revenue
        FROM product
        GROUP BY product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """),

    ("12.Year-Over-Year Monthly Sales Comparison", """
        SELECT EXTRACT(YEAR FROM order_date::DATE) AS year,
               EXTRACT(MONTH FROM order_date::DATE) AS month,
               SUM(sale_price) AS total_sales
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY year, month
        ORDER BY year, month;
    """),

    ("13.Best Performing Products by Revenue", """
        SELECT category, product_id, SUM(sale_price) as total_revenue
        FROM product
        GROUP BY category, product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """),

    ("14.Region-Wise Performance", """
        SELECT s.region, SUM(p.sale_price) as total_revenue
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY s.region
        ORDER BY total_revenue DESC;
    """),

    ("15.Impact of Discounts on Sales", """
        SELECT discount_percent, SUM(sale_price) as total_sales
        FROM product
        GROUP BY discount_percent
        ORDER BY discount_percent;
    """),

    ("16.Category Performance Metrics", """
        SELECT category, SUM(quantity) as total_quantity, 
               SUM(sale_price) as total_revenue, 
               AVG(profit) as avg_profit
        FROM product
        GROUP BY category
        ORDER BY total_revenue DESC;
    """),

    ("17.Monthly Regional Sales Analysis", """
        SELECT EXTRACT(MONTH FROM order_date::DATE) AS month,
               s.region, SUM(p.sale_price) AS total_sales
        FROM product p
        JOIN shipment s ON p.order_id = s.order_id
        GROUP BY month, s.region
        ORDER BY month, total_sales DESC;
    """),

    ("18.Revenue from Discounted Sales", """
        SELECT CASE 
                    WHEN discount_percent > 0 THEN 'discounted'
                    ELSE 'Non-Discounted'
               END AS sale_type, 
               SUM(sale_price) AS total_revenue
        FROM product
        GROUP BY sale_type;
    """),

    ("19.Top 10 cities by sales", """
        SELECT city, 
	    SUM(sale_price) AS total_sales
        FROM product p
        JOIN shipment s 
        ON p.order_id = s.order_id
        GROUP BY s.city
        ORDER BY total_sales DESC
        LIMIT 10;
       
    """),

    ("20.Top 10 state by profit", """
        SELECT state, SUM(profit) AS total_profit
        FROM shipment s
        JOIN product p
        ON p.order_id = s.order_id
        GROUP BY state
        ORDER BY total_profit DESC
        LIMIT 10;
    """),
]



# Sidebar
title = ":red[Order Data Analysis]"
st.sidebar.title(title)
selected_title = st.sidebar.radio("Select Query", simplified_titles)

# Match the selected title to the corresponding query
query_title, selected_query = next(
    (title, query) for title, query in query_options if title == selected_title
)


#-----------------------------------------------------------------------------------#
# Run the query and display results
data = run_query(selected_query)

# Main content display
st.title(query_title)
st.dataframe(data)



# 1.Top 10 highest revenue generating products (Bar chart)

if selected_title == "1.Top 10 Highest Revenue Generating Products":
    fig = px.bar(data, x='product_id', y='sale_price', 
                 title="Top 10 Highest Revenue Generating Products",
                 color='sale_price',  
                 )  
    st.plotly_chart(fig)


# 2.Top 5 Cities with Highest Profit Margins(Bar chart)

if selected_title == "2.Top 5 Cities with Highest Profit Margins":
    fig = px.bar(data, x='city', y='total_profit', title='Top 5 Cities with Highest Profit Margins')
    st.plotly_chart(fig)


#3.Total Discount by Category(Bar chart)

if selected_title == "3.Total Discount by Category":
    fig = px.bar(data, x='category', y='total_discount', title='Total Discount by Category')
    st.plotly_chart(fig)

#4.Average Sale Price per Product Category(Bar chart)

if selected_title == "4.Average Sale Price per Product Category":
    fig = px.box(data, x='category', y='average_sale_price', title='Average Sale Price per Product Category')
    st.plotly_chart(fig)

#5.Region with the Highest Average Sale Price

if selected_title == "5.Region with the Highest Average Sale Price": 
    st.header(data['region'].max())

#6.Total Profit per Category

if selected_title == "6.Total Profit per Category":
    fig = px.bar(data, x='category', y='total_profit', title='Total Profit per Category')
    st.plotly_chart(fig)

#7.Top 3 Segments with Highest Quantity of Orders
if selected_title == "7.Top 3 Segments with Highest Quantity of Orders":
    fig = px.bar(data, x='segment', y='total_quantity', title='Top 3 Segments with Highest Quantity of Orders')
    st.plotly_chart(fig)

#8.Average Discount Percentage per Region
if selected_title == "8.Average Discount Percentage per Region":
    fig = px.bar(data, x='region', y='avg_discount', title='Average Discount Percentage per Region')
    st.plotly_chart(fig)

#9.Product Category with Highest Total Profit
if selected_title == "9.Product Category with Highest Total Profit":
    fig = px.bar(data, x='category', y='total_profit', title='Product Category with Highest Total Profit')
    st.plotly_chart(fig)

#"10.Total Revenue per Year",

if selected_title == "10.Total Revenue per Year": 
    fig = px.line(data, x='year', y='total_revenue', title='Total Revenue per Year')
    st.plotly_chart(fig)

#"11.Top-Selling Products by Revenue",

if selected_title == "11.Top-Selling Products by Revenue": 
    fig = px.bar(data, x='product_id', y='total_revenue', title='Top-Selling Products by Revenue')
    st.plotly_chart(fig)

#"12.Year-Over-Year Monthly Sales Comparison"

if selected_title == "12.Year-Over-Year Monthly Sales Comparison": 
    fig = px.line(data, x=['year','month'], y='total_sales', color='year', title='Year-Over-Year Monthly Sales Comparison')
    st.plotly_chart(fig)

#"13.Best Performing Products by Revenue",
if selected_title == "13.Best Performing Products by Revenue": 
    fig = px.bar(data, x='product_id', y='total_revenue', title='Best Performing Products by Revenue')
    st.plotly_chart(fig)

#"14.Region-Wise Performance",
if selected_title == "14.Region-Wise Performance": 
    fig = px.bar(data, x='region', y='total_revenue',color='region', title='Region-Wise Performance')
    st.plotly_chart(fig)

#"15.Impact of Discounts on Sales",
if selected_title == "15.Impact of Discounts on Sales": 
    fig = px.scatter(data, x='discount_percent', y='total_sales', title='Impact of Discounts on Sales')
    st.plotly_chart(fig)

#"16.Category Performance Metrics",
if selected_title == "16.Category Performance Metrics": 
    fig = px.bar(data, x='category', y='avg_profit',color='category', title='Category Performance Metrics')
    st.plotly_chart(fig)

#"17.Monthly Regional Sales Analysis",
if selected_title == "17.Monthly Regional Sales Analysis": 
    fig = px.line(data, x='month', y='total_sales', color='region', title='Monthly Regional Sales Analysis')
    st.plotly_chart(fig)

#"18.Revenue from Discounted Sales",
if selected_title == "18.Revenue from Discounted Sales": 
    st.plotly_chart(go.Figure(go.Indicator(mode="number", value=data['total_revenue'].sum(), title={"text": "Revenue from Discounted Sales"})))


#"19.Show Products with Sales more than 50,000 Revenue Along with Regions",
if selected_title == "19.Top 10 cities by sales": 
    fig = px.bar(data, x='city', y='total_sales',color= 'city', title='Top 10 cities by sales')
    st.plotly_chart(fig)

if selected_title == "19.Top 10 cities by sales":
    fig = px.scatter_geo(data,
                         locations='city',
                         locationmode='USA-states',  # Specify U.S. state location mode
                         size='total_sales',  # Metric to determine bubble size
                         scope='usa',
                         title='Profit by State (Bubble Map)'
                        )
    st.plotly_chart(fig)


#"20.Segment-Wise Average Discount",
if selected_title == "20.Top 10 state by profit": 
    fig = px.bar(data, x='state', y='total_profit', title='Top 10 state by profit')
    st.plotly_chart(fig)


  
