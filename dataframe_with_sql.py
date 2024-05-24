
import pandas as pd
import mysql.connector


def insert_dataframe_to_sql(data_type, dataframe):
    connection = mysql.connector.connect(
                                host='127.0.0.1',  # Your host
                                user='root',       # Your username
                                password='password',  # Your password
                                database='phonepe_pulse_project'  # Your database name
                                )
    cursor = connection.cursor()

    #Insert data into MySQL table using parameterized queries
    try:
        rows_inserted = 0  # Initialize counter

        with connection.cursor() as cursor:
            # Define the INSERT INTO statement with placeholders
            if data_type == "aggregated_transaction":
                sql = """INSERT INTO agg_trans (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"""
                
                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
            elif data_type == "aggregated_user":
                sql = """INSERT INTO agg_user(State, Year, Quarter, Agg_User_device, Agg_User_count, Agg_Device_Percentage)        
                                                                VALUES (%s, %s, %s, %s, %s, %s)"""
        
                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row['Agg_User_device'], row['Agg_User_count'], row['Agg_Device_Percentage'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
            elif data_type == "map_transaction":
                sql = """INSERT INTO map_trans(State, Year, Quarter, Districts,
                                                    Map_Transaction_count,
                                                Map_Transaction_amount) 
                                                VALUES (%s, %s, %s, %s, %s, %s)"""

                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row['Districts'], row['Map_Transaction_count'], row['Map_Transaction_amount'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
            elif data_type == "map_user":
                sql = """INSERT INTO map_user(State, Year, Quarter, Districts,
                                                  Registered_Users,
                                                    App_Opens) 
                                                                 
                                                    VALUES (%s, %s, %s, %s, %s, %s)"""
        
                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row["Districts"], 
                                            row['Registered_Users'], 
                                                row['App_Opens'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
            elif data_type == "top_transaction":
                sql = """INSERT INTO top_trans(State, Year, Quarter, Pincodes, 
                                                    Transaction_Count,
			                                          Transaction_Amount)
                                                                 
                                                    VALUES (%s, %s, %s, %s, %s, %s)"""
        
                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row['Pincodes'], 
                                            row['Transaction_Count'], 
                                                row['Transaction_Amount'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
            elif data_type == "top_user":
                sql = """INSERT INTO top_user(State, Year, Quarter, 
                                            Pincodes, 
                                             Registered_User) 
                                                                   
                                             VALUES (%s, %s, %s, %s, %s)"""
        
                # Iterate over each row in the DataFrame and execute the query
                for index, row in dataframe.iterrows():
                    # Extract values from the row
                    values = (row['State'], row['Year'], row['Quarter'], row['Pincodes'], 
                                            row['Registered_User'])
                    # Execute the query with the values
                    cursor.execute(sql, values)
                    rows_inserted += 1  # Increment counter
    
            # Commit changes
            connection.commit()
            print(f"Data inserted successfully! Number of rows inserted: {rows_inserted}")

    except Exception as e:
        print(f"Error inserting data: {e}")

    if rows_inserted:
        return True
    return False


def retrieve_dataframe(table_name="agg_trans"):
    connection = mysql.connector.connect(
                                host='127.0.0.1',  # Your host
                                user='root',       # Your username
                                password='password',  # Your password
                                database='phonepe_pulse_project'  # Your database name
                                )
    cursor = connection.cursor()

    # agg_trans table
    cursor.execute("select *from " + table_name)
    cursor_data =cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()


    dataframe = None
    if table_name =='agg_trans':
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
    elif table_name == 'agg_user':
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Agg_User_device", "Agg_User_count","Agg_Device_Percentage"))
    elif table_name == 'map_trans':
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Districts", "Map_Transaction_count","Map_Transaction_amount"))
    elif table_name == "map_user":
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Districts", "Registered_Users","App_Opens"))
    elif table_name == "top_trans":
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Pincodes", "Transaction_Count","Transaction_Amount"))
    elif table_name == "top_user":
        dataframe = pd.DataFrame(cursor_data, columns=("State", "Year", "Quarter", "Pincodes", "Registered_User"))
    return dataframe