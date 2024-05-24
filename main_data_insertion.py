
import os
import json
import pandas as pd

file_path_dict = {
    "aggregated_transaction": "aggregated/transaction",
    "aggregated_user" : "aggregated/user",
    "map_transaction":  "map/transaction/hover",
    "map_user" :  "map/user/hover",
    "top_transaction" : "top/transaction",
    "top_user": "top/user"
}

aggregated_transaction = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}
aggregated_user = {'State': [], 'Year': [], 'Quarter': [], 'Agg_User_device': [], 'Agg_User_count': [], 'Agg_Device_Percentage': []}
map_transaction ={'State':[], 'Year':[], 'Quarter':[], 'Districts':[], 'Map_Transaction_count':[] ,'Map_Transaction_amount':[]}
map_user={'State':[], 'Year':[], 'Quarter':[], "Districts":[], 'Registered_Users':[] ,'App_Opens':[] }
top_transaction = {'State': [], 'Year': [], 'Quarter': [],  'Pincodes': [], 'Transaction_Count': [], 'Transaction_Amount': []}
top_user = {'State': [], 'Year': [], 'Quarter': [],  'Pincodes': [], 'Registered_User': []}


def retrieve_and_insert_data():
    for key, value in file_path_dict.items():
        file_path = "C:/Users/Anand Kumar/Desktop/phonepe/pulse/data/{0}/country/india/state/".format(file_path_dict[key])
        print(file_path)

        path_list = os.listdir(file_path)

        for state in path_list:
            p_state = os.path.join(file_path, state)  # Use os.path.join to construct paths
            state=state.replace('andaman-&-nicobar-islands', "Andaman & Nicobar")
            state = state.replace("-", " ")
            state=state.title()
            state=state.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar and Haveli and Daman and Diu")
            agg_year = os.listdir(p_state)

            for year in agg_year:
                p_year = os.path.join(p_state, year)  # Use os.path.join to construct paths
                agg_year_list = os.listdir(p_year)

                for qr in agg_year_list:
                    file1 = os.path.join(p_year, qr)  # Use os.path.join to construct paths
                    with open(file1, "r") as Data:
                        d1 = json.load(Data)

                        if key == "aggregated_transaction":
                            for z in d1["data"]["transactionData"]:
                                name = z['name']
                                count = z['paymentInstruments'][0]['count']
                                amount = z['paymentInstruments'][0]["amount"]
                                aggregated_transaction['Transaction_type'].append(name)
                                aggregated_transaction['Transaction_count'].append(count)
                                aggregated_transaction['Transaction_amount'].append(amount)
                                aggregated_transaction["State"].append(state)
                                aggregated_transaction["Year"].append(int(year))
                                aggregated_transaction["Quarter"].append(int(qr.split('.')[0]))  # Use split to remove '.json' and convert to int
                        elif key == 'aggregated_user':
                            try:
                                for h in d1['data']["usersByDevice"]:
                                    user_device = h["brand"]
                                    user_count = h['count']
                                    device_per = h['percentage']
                                    aggregated_user['Agg_User_device'].append(user_device)
                                    aggregated_user['Agg_User_count'].append(user_count)
                                    aggregated_user['Agg_Device_Percentage'].append(device_per)
                                    aggregated_user["State"].append(state)
                                    aggregated_user["Year"].append(year)
                                    aggregated_user["Quarter"].append(int(qr.strip(".json")))
                            except TypeError:
                                print("Data not found")
                        elif key == "map_transaction":
                            for m1 in d1["data"]["hoverDataList"]:
                                name=m1['name']
                                count=m1['metric'][0]['count']
                                amount=m1['metric'][0]["amount"]

                                map_transaction['Districts'].append(name)
                                map_transaction['Map_Transaction_count'].append(count)
                                map_transaction['Map_Transaction_amount'].append(amount)
                                map_transaction["State"].append(state)
                                map_transaction["Year"].append(year)
                                map_transaction["Quarter"].append(int(qr.strip('.json')))
                                for i in range(len(map_transaction['Districts'])):
                                    map_transaction['Districts'][i] = map_transaction['Districts'][i].replace('district', '')
                        
                        elif key == "map_user":
                            for z in d1["data"]["hoverData"].items():
                                district=z[0]
                                reg_user=z[1]["registeredUsers"]
                                app_open=z[1]["appOpens"]
                                map_user["Districts"].append(district)
                                map_user['Registered_Users'].append(reg_user)
                                map_user['App_Opens'].append(app_open)
                                map_user['State'].append(state)
                                map_user['Year'].append(year)
                                map_user['Quarter'].append(int(qr.strip('.json')))
                        elif key == "top_transaction":
                            for t in d1['data']['pincodes']:
                                entity_name = t["entityName"]
                                trans_count = t["metric"]["count"]
                                trans_amount = t["metric"]["amount"]

                                top_transaction['State'].append(state)
                                top_transaction['Year'].append(year)
                                top_transaction['Quarter'].append(qr.strip('.json'))
                                top_transaction['Pincodes'].append(entity_name)
                                top_transaction['Transaction_Count'].append(trans_count)
                                top_transaction['Transaction_Amount'].append(trans_amount)
                        elif key == "top_user":
                            for t in d1['data']['pincodes']:
                                name = t["name"]
                                reg_us = t["registeredUsers"]

                                top_user['State'].append(state)
                                top_user['Year'].append(year)
                                top_user['Quarter'].append(qr.strip('.json'))
                                top_user['Pincodes'].append(name)
                                top_user['Registered_User'].append(reg_us)
                            
        from dataframe_with_sql import insert_dataframe_to_sql
        from data_cleaning import clean_data
        if key == 'aggregated_transaction':
            aggregated_transaction_df = pd.DataFrame(aggregated_transaction)
            aggregated_transaction_df.to_csv('aggregated_transaction.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1} ".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
        elif key == "aggregated_user":
            aggregated_user_df=pd.DataFrame(aggregated_user)  
            insert_dataframe_to_sql(key, aggregated_user_df)              
            aggregated_user_df.to_csv('aggregated_user.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1} ".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
            
        elif key == "map_transaction":
            map_transaction_df=pd.DataFrame(map_transaction)
            insert_dataframe_to_sql(key, map_transaction_df)
            map_transaction_df.to_csv('map_transaction.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1} ".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
        elif key == "map_user":
            map_user_df=pd.DataFrame(map_user)
            insert_dataframe_to_sql(key, map_user_df)
            map_user_df.to_csv('map_user.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1} ".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
            
        elif key == "top_transaction":
            top_transaction_df=pd.DataFrame(top_transaction)
            insert_dataframe_to_sql(key, top_transaction_df)
            top_transaction_df.to_csv('top_transaction.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1} ".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
        elif key == "top_user":
            top_user_df = pd.DataFrame(top_user)
            insert_dataframe_to_sql(key, top_user_df)
            top_user_df.to_csv('top_user.csv'.format(), index=False)
            df = pd.read_csv(key + ".csv")
            cleaned_df = clean_data(df.copy())
            print("Number of Initial rows for {0}: is {1} ".format(key, len(df)))
            print("Number of rows after cleanup for {0}: is {1}".format(key, len(df)))
            insert_dataframe_to_sql(key, cleaned_df)
            

if __name__ == "__main__":
    retrieve_and_insert_data()

