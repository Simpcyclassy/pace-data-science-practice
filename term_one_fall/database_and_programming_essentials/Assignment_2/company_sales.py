#!/usr/bin/env python
# coding: utf-8

# In[50]:


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

# 1a. Read data from the sales.csv file into pandas dataframes.
sales_df = pd.read_csv('sales.csv')

# 1a. Read data from the sales_team.csv file into pandas dataframes.
sales_team_df = pd.read_csv('sales_teams.csv')

# Combine the two dataframes based on Sales Agent column
combined_df = pd.merge(sales_df, sales_team_df, on='Sales Agent', how='left')
combined_df['Product Name'].unique()


# In[51]:


combined_df['Regional Office'].unique()


# In[52]:


# 2a. Rename the columns in both datasets, making all lowercase and replacing space with an underscore.
combined_df.columns = combined_df.columns.str.lower().str.replace(' ', '_')
combined_df.head(10)


# In[53]:


# 2b. Identify the missing values with ‘Not Available’ and ‘Unknown’, and then replace them with NaN values.
combined_df.replace(['Not Available', 'Unknown'], np.nan, inplace=True)
combined_df.head(10)


# In[54]:


# 3a. Add a new column, to determine the ‘Total Sales Value’ using the deal closing values and quantities.
combined_df['close_value_per_unit'] = pd.to_numeric(combined_df['close_value_per_unit'], errors='coerce')
combined_df['closing_quantity'] = pd.to_numeric(combined_df['closing_quantity'], errors='coerce')

combined_df['total_sales_value'] = combined_df['close_value_per_unit'] * combined_df['closing_quantity']
combined_df.head(10)


# In[55]:


# 3b. Add a new column, to list the ‘Sales Region’ based on sales agent’s regional office information available in the sales team dataset.
combined_df.rename(columns={'regional_office': 'sales_region'}, inplace=True)
combined_df.head(10)


# In[56]:


# 4. Convert 'deal_engage_date' and 'deal_close_date' from object data type to datetime
combined_df['deal_engage_date'] = pd.to_datetime(combined_df['deal_engage_date'], format="%Y-%m-%d", errors='coerce')
combined_df['deal_close_date'] = pd.to_datetime(combined_df['deal_close_date'], format="%Y-%m-%d", errors='coerce')

combined_df.head(10)


# In[57]:


# 5. Drop 'close_value_per_unit' and 'closing_quantity' columns, and other redundant columns
columns_to_drop = ['close_value_per_unit', 'closing_quantity']
combined_df.drop(columns=columns_to_drop, inplace=True)
combined_df.head(10)


# In[59]:


# 6. Create a new database named ‘CRM’ and write the dataset into a table named ‘sales’
os.environ['MYSQL_PASSWORD'] = "12345678"
password = os.getenv('MYSQL_PASSWORD')

# Create engine and handle connection errors
engine = create_engine(f'mysql+mysqlconnector://root:{password}@localhost/CRM',
            connect_args={'auth_plugin': 'caching_sha2_password'})
print(f"Mysql is connected successfully with create_engine: {engine}")

combined_df.to_sql('sales', con=engine, if_exists='replace', index=False)


# In[60]:


# 7a.Find top 5 sales agents along with their sales revenue.
query_a = """
    SELECT sales_agent, SUM(total_sales_value) AS sales_revenue
    FROM sales
    GROUP BY sales_agent
    ORDER BY sales_revenue DESC
    LIMIT 5;
"""

top_sales_agents = pd.read_sql(query_a, engine)
top_sales_agents.head(10)


# In[61]:


# 7b. Find the total value of sales closed by different regions.
query_b = """
    SELECT sales_region, SUM(total_sales_value) AS total_sales_value
    FROM sales
    GROUP BY sales_region
    ORDER BY total_sales_value DESC;
"""

total_sales_by_region = pd.read_sql(query_b, engine)
total_sales_by_region.head(10)


# In[70]:


# Find the list of returning customers in descending order of their respective ‘repeat customer rate’
# (i.e., the percentage of closed deals from returning customers).
# Please note that the 'account' column in the 'sales' contains the information about their business clients which you may refer to as the 'customers'

query_c = """
    WITH closed_deals AS (
        SELECT 
            account, 
            COUNT(*) AS total_deals,
            SUM(CASE WHEN TRIM(LOWER(deal_stage)) = 'won' THEN 1 ELSE 0 END) AS closed_deals
        FROM sales
        GROUP BY account
        HAVING COUNT(*) > 1
    )
    SELECT 
        account,
        closed_deals,
        (closed_deals * 100.0 / total_deals) AS repeat_customer_rate
    FROM closed_deals
    ORDER BY repeat_customer_rate DESC;

"""

returning_customers = pd.read_sql(query_c, engine)
returning_customers.head(10)


# In[68]:


combined_df['deal_stage'].unique()


# In[ ]:




