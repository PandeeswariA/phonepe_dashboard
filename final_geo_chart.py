import pandas as pd
import mysql.connector
import requests
import json
import plotly.express as px

from dataframe_with_sql import retrieve_dataframe

# Define the SQL connection and retrieve the data
def retrieve_dataframe(table_name):
    connection = mysql.connector.connect(
        host='127.0.0.1',  # Your host
        user='root',       # Your username
        password='password',  # Your password
        database='phonepe_pulse_project'  # Your database name
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table_name)
    cursor_data = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    if table_name == 'agg_trans':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"])
    elif table_name == 'agg_user':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Agg_User_device", "Agg_User_count", "Agg_Device_Percentage"])
    elif table_name == 'map_trans':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Districts", "Map_Transaction_count", "Map_Transaction_amount"])
    elif table_name == 'map_user':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Districts", "Registered_Users", "App_Opens"])
    elif table_name == 'top_trans':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Pincodes", "Transaction_Count", "Transaction_Amount"])
    elif table_name == 'top_user':
        return pd.DataFrame(cursor_data, columns=["State", "Year", "Quarter", "Pincodes", "Registered_User"])

# Retrieve DataFrames from SQL
agg_trans_df = retrieve_dataframe('agg_trans')
agg_user_df = retrieve_dataframe('agg_user')
map_trans_df = retrieve_dataframe('map_trans')
map_user_df = retrieve_dataframe('map_user')
top_trans_df = retrieve_dataframe('top_trans')
top_user_df = retrieve_dataframe('top_user')

combined_df = pd.concat([agg_trans_df, agg_user_df, map_trans_df, map_user_df, top_trans_df, top_user_df], ignore_index=True)




# Aggregate the data by state
aggregated_df = combined_df.groupby("State").agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum",
    "Transaction_Count":"sum",
    "Transaction_Amount":"sum",
    "Agg_User_count":"sum",
    "Map_Transaction_amount":"sum",
    "Map_Transaction_count":"sum",
    "Registered_Users": "sum",
    "Registered_User": "sum"
}).reset_index()

sum_transaction_amount_df=aggregated_df["Transaction_amount"]+aggregated_df["Transaction_Amount"]+aggregated_df["Map_Transaction_amount"]
sum_transaction_count_df=aggregated_df["Transaction_count"]+aggregated_df["Transaction_Count"]+aggregated_df["Map_Transaction_count"]
sum_user_count_df=aggregated_df["Agg_User_count"]+aggregated_df["Registered_Users"]+aggregated_df["Registered_User"]

final_dataframe = pd.DataFrame({
    "State":aggregated_df["State"],
    'Sum_Transaction_Amount': sum_transaction_amount_df,
    'Sum_Transaction_Count': sum_transaction_count_df,
    'Sum_User_Count': sum_user_count_df
})



