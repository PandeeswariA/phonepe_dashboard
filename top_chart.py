import mysql.connector
import pandas as pd

def retrieve_top_data(data_type, metric):
    connection = mysql.connector.connect(
        host='127.0.0.1',  # Your host
        user='root',       # Your username
        password='password',  # Your password
        database='phonepe_pulse_project'  # Your database name
    )
    cursor = connection.cursor()

    if data_type == "Transactions":
        if metric == "count":
            # Query to retrieve top 10 states by transaction count
            query_top_states = """
            SELECT State, SUM(Transaction_count) as Total_Transactions, AVG(Transaction_count) as Avg_Transactions
            FROM (
                SELECT State, Transaction_count FROM agg_trans
                UNION ALL
                SELECT State, Map_Transaction_count as Transaction_count FROM map_trans
                UNION ALL
                SELECT State, Transaction_Count as Transaction_count FROM top_trans
            ) as CombinedTransactions
            GROUP BY State
            ORDER BY Total_Transactions DESC
            LIMIT 10
            """
            # Query to retrieve top 10 districts by transaction count
            query_top_districts = """
            SELECT Districts as District, SUM(Map_Transaction_count) as Total_Transactions, AVG(Map_Transaction_count) as Avg_Transactions
            FROM map_trans
            GROUP BY District
            ORDER BY Total_Transactions DESC
            LIMIT 10
            """
            # Query to retrieve top 10 pincodes by transaction count
            query_top_pincodes = """
            SELECT Pincodes, SUM(Transaction_Count) as Total_Transactions, AVG(Transaction_Count) as Avg_Transactions
            FROM top_trans
            GROUP BY Pincodes
            ORDER BY Total_Transactions DESC
            LIMIT 10
            """
        elif metric == "amount":
            # Query to retrieve top 10 states by transaction amount
            query_top_states = """
            SELECT State, SUM(Transaction_amount) as Total_Transaction_Amount, AVG(Transaction_amount) as Avg_Transaction_Amount
            FROM (
                SELECT State, Transaction_amount FROM agg_trans
                UNION ALL
                SELECT State, Map_Transaction_amount as Transaction_amount FROM map_trans
                UNION ALL
                SELECT State, Transaction_Amount as Transaction_amount FROM top_trans
            ) as CombinedTransactions
            GROUP BY State
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10
            """
            # Query to retrieve top 10 districts by transaction amount
            query_top_districts = """
            SELECT Districts as District, SUM(Map_Transaction_amount) as Total_Transaction_Amount, AVG(Map_Transaction_amount) as Avg_Transaction_Amount
            FROM map_trans
            GROUP BY District
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10
            """
            # Query to retrieve top 10 pincodes by transaction amount
            query_top_pincodes = """
            SELECT Pincodes, SUM(Transaction_Amount) as Total_Transaction_Amount, AVG(Transaction_Amount) as Avg_Transaction_Amount
            FROM top_trans
            GROUP BY Pincodes
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10
            """
    elif data_type == "Users":
        if metric == "count":
            # Query to retrieve top 10 states by user count
            query_top_states = """
            SELECT State, SUM(Agg_User_count) as Total_Users, AVG(Agg_User_count) as Avg_Users
            FROM (
                SELECT State, Agg_User_count FROM agg_user
                UNION ALL
                SELECT State, Registered_Users as Agg_User_count FROM map_user
                UNION ALL
                SELECT State, Registered_User as Agg_User_count FROM top_user
            ) as CombinedUsers
            GROUP BY State
            ORDER BY Total_Users DESC
            LIMIT 10
            """
            # Query to retrieve top 10 districts by user count
            query_top_districts = """
            SELECT Districts as District, SUM(Registered_Users) as Total_Users, AVG(Registered_Users) as Avg_Users
            FROM map_user
            GROUP BY District
            ORDER BY Total_Users DESC
            LIMIT 10
            """
            # Query to retrieve top 10 pincodes by user count
            query_top_pincodes = """
            SELECT Pincodes, SUM(Registered_User) as Total_Users, AVG(Registered_User) as Avg_Users
            FROM top_user
            GROUP BY Pincodes
            ORDER BY Total_Users DESC
            LIMIT 10
            """
    # Execute the queries and fetch the results
    cursor.execute(query_top_states)
    top_states = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total', 'Average'])

    cursor.execute(query_top_districts)
    top_districts = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total', 'Average'])

    cursor.execute(query_top_pincodes)
    top_pincodes = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Total', 'Average'])

    # Close connection
    cursor.close()
    connection.close()

    return top_states, top_districts, top_pincodes








