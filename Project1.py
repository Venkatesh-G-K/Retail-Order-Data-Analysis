# %%
##  Retail Order Data Analysis
#Getting Data from kaggle
pip install sqlalchemy
# %%
#!kaggle datasets download ankitbansal06/retail-orders -f orders.csv
# %% ----- Importing needed---

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.title('Retail Order Data Analysis')
st.button("Regenerate")


#Unzipping File
from zipfile import ZipFile

with ZipFile("orders.csv.zip", "r") as zip_ref:
    zip_ref.extractall("orders")


# %%
df = pd.read_csv("C:\\Users\\VeNkAT\\Desktop\\Python_Learn\\orders\\orders.csv")

df.head()
df = pd.DataFrame(df)


# %%
#df = pd.DataFrame(df)

# %%
#filling missing values with 0

df.fillna(0, inplace=True)

print(df.head())

# %%
#Renaming Columns
df.rename(columns = lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

print(df.head())

# %%
# Remove extra spaces in text fields:

df = df.apply(lambda x: x.str.strip()
  if x.dtype == "object"
              else x)


# %%
#Adding Calculated Columns:
#sales = unit_price * Quantity
#Profit = sale - Cost
#discount = (discount * sale_price) / 100


# %%
df['sale_price'] = df['cost_price'] * df['quantity']

# %%
df['profit'] = df['sale_price'] - df['cost_price']

# %%
df['discount'] = df['discount_percent'] * df['sale_price'] / 100


# %%
st.subheader("Data Frame")
df
# Define the common column(s)
common_columns = ['order_id']

# Split the data into two tables
table1 = common_columns + ['order_date', 'ship_mode', 'segment', 'country', 'city', 'state', 'postal_code', 'region']
table2 = common_columns + ['category', 'sub_category', 'product_id', 'cost_price', 'list_price', 'quantity', 'discount_percent', 'sale_price', 'profit', 'discount']

shipment = df[table1]
product = df[table2]

# %%
st.subheader("Spliting Tables")
st.write("Shipment Table")
shipment

# %%
st.write("Product Table")
product

# %%
#from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# %%


# Connection details
user = "postgres"
password = "venkat"  # Updated password
host = "localhost"
port = "5432"
database = "mydb"

# Create the connection string
connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


# %%
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Create the engine
try:
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        print("Connection to PostgreSQL was successful!")
except Exception as e:
    print(f"Error occurred: {e}")


# %%
engine

# %%
import pandas as pd

# %%
shipment.to_sql ("shipment",con = engine, if_exists="replace" )
product.to_sql ("product",con = engine, if_exists="replace" )

# %%
#---------------------------------------THE END------------------------------------------------------------------------------------------------#

#----------------------------------STREAMLIT--------------------------------------

# %%
st.subheader("Thank You")
# %%
st.write("THE END")
# %%
# streamlit run Project1.py

