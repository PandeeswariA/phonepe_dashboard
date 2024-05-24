import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import plotly.express as px
import pandas as pd
import requests
import json

# Set page layout to wide
st.set_page_config(layout="wide")

st.markdown("<h1 style='color: purple; white-space: nowrap;'>PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION</h1>", unsafe_allow_html=True)

# Page Layout: The st.set_page_config(layout="wide") call sets the Streamlit app layout to use the full width of the browser window.
# HTML Title with white-space: nowrap: The white-space: nowrap; CSS property ensures that the text does not wrap to the next line, keeping the title on a single line.

with st.sidebar:
     select=option_menu("Main Menu",["HOME", "DATA EXPLORATION",  "TOP CHART"])
     
     from final_geo_chart  import final_dataframe


if select == "HOME":
    tab1, tab2 = st.tabs(["Home", "Insights"])

    with tab1:
        st.markdown("<h2 style='color: purple;'>Title: </h2>", unsafe_allow_html=True)
        st.write("Phonepe Pulse Data Visualization And Exploration")
        
        st.markdown("<h2 style='color: purple;'>Domain :  </h2>", unsafe_allow_html=True)
        st.write("Fintech")

        st.markdown("<h2 style='color: purple;'>Technologies Used :  </h2>", unsafe_allow_html=True)

        st.write("Github Cloning, Python, Pandas, MySQL, MySql-Connector-Python, Streamlit, Plotly. ")

        st.markdown("<h2 style='color: purple;'>Imported  Libraries :  </h2>", unsafe_allow_html=True)

        st.write("Streamlit,  Plotly Express,  Pandas,  MySqlConnector,  Requests,  Json")
        
        st.markdown("<h2 style='color: purple;'>Project  Description :  </h2>", unsafe_allow_html=True)

        st.write("The Phonepe Data VisualizationAnd Exploration Project is a Python-based solutions that extracts data from Phonepe Pulse Github repository , then cleaning of data is done and then data is converted to Pandas DataFrame and then stored into a MYSQLDataBase, then the User performs variety of Visualisation about  Transactions and Users of Phonepe app that are achieved through interactive Dashboard using User-Friendly tool Streamlit and Plotly,In this project, The User also perform Geo Visualization to present data geographically and also  visualizes and explores transaction and  User data of  Phonepe app  across various states in India using PhonePe data.")  
        

    with tab2:
        
        st.markdown("<h1 style='color: purple;'>Geo Map for PhonePe Pulse Project</h1>", unsafe_allow_html=True)

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        geo_data_1 = json.loads(response.content)

        fig = px.choropleth(
            final_dataframe,
            geojson=geo_data_1,
            locations='State',
            featureidkey='properties.ST_NM',
            color='Sum_Transaction_Amount',
            color_continuous_scale="rainbow",
            hover_name='State',
            hover_data={
                'Sum_Transaction_Amount': ':.2f',
                'Sum_Transaction_Count': ':.2f',
                'Sum_User_Count': ':.2f'
            },
            title='Map of India with States and Transaction Data'
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig)
    
elif select=="DATA EXPLORATION":
        
        tab1, tab2, tab3 = st.tabs(["Aggregate Analysis", "Map Analysis", "Top Analysis"])

        with tab1:
                Method1 = st.selectbox("Select an option", ["Aggregated Transaction Analysis", "Aggregated User Analysis"])

                if Method1 == "Aggregated Transaction Analysis":

                    from dataframe_with_sql import retrieve_dataframe

                    dataframe = retrieve_dataframe("agg_trans")

                    col1, col2 = st.columns(2)

                    dataframe = retrieve_dataframe("agg_trans")

                    with col1:
                            
                            st.subheader("Year Analysis")
                            selected_year_slr = st.slider("Year", min_value=2018, max_value=2023)

                            # Filter the data for the selected year
                            filtered_data_year = dataframe[dataframe["Year"] == selected_year_slr]

                            # Group by year and sum the transaction amount and count
                            grouped_data_state_year = filtered_data_year.groupby("State").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                            # Plot chart for transaction amount over years
                            fig_year_amount = px.bar(grouped_data_state_year, x="State", y="Transaction_amount", color="State", title=f"Total Transaction Amount by State for {selected_year_slr}",
                                labels={"Transaction_amount": "Total Transaction Amount"})
                            st.plotly_chart(fig_year_amount)

                            fig_year_count = px.line(grouped_data_state_year, x="State", y="Transaction_count", height=500, title=f"Total Transaction Count by State for {selected_year_slr}",
                            labels={"Transaction_count": "Total Transaction Count"})
                            st.plotly_chart(fig_year_count)

                            grouped_data_state_year_type = filtered_data_year.groupby("Transaction_type").agg({"Transaction_amount": "sum"}).reset_index()


                            fig_year_histogram_trans_amt_ct = px.histogram(grouped_data_state_year_type, x="Transaction_type", y="Transaction_amount", color="Transaction_type",
                                title=f"Transaction Amount and Transaction Type for  {selected_year_slr}",
                                labels={"Transaction_amount": "Total Transaction Amount", "State": "State"})
                            st.plotly_chart(fig_year_histogram_trans_amt_ct)

                            grouped_data_trans_year = filtered_data_year.groupby("Transaction_type").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                            fig_3d_scatter = px.scatter_3d(grouped_data_trans_year, 
                                x='Transaction_type', 
                                y='Transaction_count', 
                                z='Transaction_amount',
                                color='Transaction_type',
                                title= f'Transaction Type vs Transaction Count vs Transaction Amount for {selected_year_slr}',
                                labels={'Transaction_count': 'Total Transaction Count', 
                                        'Transaction_amount': 'Total Transaction Amount',
                                        'Transaction_type': 'Transaction Type'})

                            # Update axis labels and tick font size
                            fig_3d_scatter.update_layout(scene=dict(xaxis_title='Transaction Type',
                                                        yaxis_title='Total Transaction Count',
                                                        zaxis_title='Total Transaction Amount'))

                            # Show the plot
                            st.plotly_chart(fig_3d_scatter)


                    with col2:
                            st.subheader("Quarter Analysis")
                            quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                            quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                            selected_quarter = quarter_map[quarter]

                            # Filter the data for the selected quarter and year
                            filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                            # Group by quarter and sum the transaction amount and count
                            grouped_data_state_quarter = filtered_data_quarter.groupby("State").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                            # Plot chart for transaction amount for the selected quarter
                            fig_quarter_amount = px.bar(grouped_data_state_quarter, x="State", y="Transaction_amount", color="State",
                                    title=f"Total Transaction Amount by State for {quarter} {selected_year_slr}",
                                    labels={"Transaction_amount": "Total Transaction Amount"})
                            st.plotly_chart(fig_quarter_amount)


                            fig_quarter_count = px.line(grouped_data_state_quarter, x="State", y="Transaction_count", height=500,
                            title=f"Total Transaction Count by State for {quarter} {selected_year_slr}",
                            labels={"Transaction_count": "Total Transaction Count"})
                            st.plotly_chart(fig_quarter_count)

                            grouped_data_trans_quarter = filtered_data_year.groupby("Transaction_type").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()


                            fig_quarter_trans_amt_ct = px.histogram(grouped_data_trans_quarter, x="Transaction_type", y="Transaction_amount", 
                                title=f"Transaction Amount vs Transaction Type({quarter} {selected_year_slr})", color="Transaction_type",
                                labels={"Transaction_amount": "Total Transaction Amount", "Transaction_count": "Total Transaction Count"})
                            st.plotly_chart(fig_quarter_trans_amt_ct)

                            grouped_data_trans_quarter = filtered_data_year.groupby("Transaction_type").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                            fig_3d_scatter = px.scatter_3d(grouped_data_trans_quarter, 
                                x='Transaction_type', 
                                y='Transaction_count', 
                                z='Transaction_amount',
                                color='Transaction_type',
                            title=f'Transaction Type vs Transaction Count vs Transaction Amount({quarter} {selected_year_slr})',
                            labels={'Transaction_count': 'Total Transaction Count', 
                                    'Transaction_amount': 'Total Transaction Amount',
                                    'Transaction_type': 'Transaction Type'})

                        # Update axis labels and tick font size
                            fig_3d_scatter.update_layout(scene=dict(xaxis_title='Transaction Type',
                                                        yaxis_title='Total Transaction Count',
                                                        zaxis_title='Total Transaction Amount'))

                            # Show the plot
                            st.plotly_chart(fig_3d_scatter)

                    if Method1 == "Aggregated Transaction Analysis":

                        from dataframe_with_sql import retrieve_dataframe

                        dataframe = retrieve_dataframe("agg_trans")

                        st.header("Aggregte Transaction Amount And Count By Year")

                        grouped_data_yearwise_agg_trans =dataframe.groupby("Year").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                        st.subheader('Transaction Amount by Year')
                        agg_trans_yr_amt = px.bar(grouped_data_yearwise_agg_trans, x='Year', y='Transaction_amount', color='Year', title='Transaction Amount by Year')
                        st.plotly_chart(agg_trans_yr_amt)

            
                        st.subheader('Transaction count by Year')

                        # Create the line chart with Plotly Express
                        agg_trans_yr_ct = px.line(
                        grouped_data_yearwise_agg_trans, 
                        x='Year', 
                        y='Transaction_count', 
                        title='Transaction count by Year',
                        labels={'Transaction_count': 'Transaction Count', 'Year': 'Year'},
                        markers=True
                        )

                        # Update traces to show both lines and markers, and set marker properties
                        agg_trans_yr_ct.update_traces(
                        mode='markers+lines', 
                        marker=dict(color='red', size=8), 
                        line=dict(color='royalblue')
                        )

                        # Display the line chart in Streamlit
                        st.plotly_chart(agg_trans_yr_ct)


                        st.subheader('Transaction Type and Amount')

                        grouped_data_trans_type = dataframe.groupby("Transaction_type").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                        # Plotting histogram for transaction amount
                        agg_trans_type_amount = px.pie(grouped_data_trans_type, names='Transaction_type',  values='Transaction_amount', 
                                        color='Transaction_type', title='Transaction Amount by Transaction Type')
                        st.plotly_chart(agg_trans_type_amount)

                        st.subheader("Transaction Type and Count")

                        agg_trans_type_ct = px.bar(grouped_data_trans_type, x='Transaction_type', y='Transaction_count', title='Transaction Count by Transaction Type', color="Transaction_type")

                        # Update marker color to red


                        st.plotly_chart(agg_trans_type_ct)

                        grouped_data_state_agg_trans = dataframe.groupby("State").agg({"Transaction_amount": "sum", "Transaction_count": "sum"}).reset_index()

                        st.subheader("Transaction Amount By State")

                        fig=fig = px.bar(grouped_data_state_agg_trans, x='State', y='Transaction_amount', title='Transaction Amount  by State',color_discrete_sequence=["orange"], height=600, width=650)
                        
                        
                        st.plotly_chart(fig)

                elif Method1 == "Aggregated User Analysis":
                        from dataframe_with_sql import retrieve_dataframe
                                    
                        dataframe = retrieve_dataframe("agg_user")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Year Analysis")
                            selected_year_slr = st.slider("Year", min_value=2018, max_value=2023)

                            # Filter the data for the selected year
                            filtered_data_year = dataframe[dataframe["Year"] == selected_year_slr]

                            # Group by year and sum the transaction amount and count
                            grouped_data_user_dev_year = filtered_data_year.groupby(["State", "Agg_User_device"]).agg({"Agg_User_count": "sum", "Agg_Device_Percentage" :"sum"}).reset_index()

                            # Plot chart for transaction amount over years
                            fig_year_state_user_ct = px.bar(grouped_data_user_dev_year, x="State", y="Agg_User_count", color_discrete_sequence=["green"], height=500, width=800, title=f"Agg User by State for {selected_year_slr}",
                                            labels={"Agg_User_count": "User"})
                            st.plotly_chart(fig_year_state_user_ct)

                            df_agg_us_yr_sorted = grouped_data_user_dev_year.sort_values(by='Agg_User_count', ascending=False)

                            fig_year_user_count_device = px.histogram(df_agg_us_yr_sorted, x="Agg_User_device", y="Agg_User_count",  title=f"Aggregate user count by device for {selected_year_slr}",
                                labels={"Transaction_count": "Total Aggregate User Count"})
                            st.plotly_chart(fig_year_user_count_device)

                        with col2:
                            st.subheader("Quarter Analysis")
                            quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                            quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                            selected_quarter = quarter_map[quarter]

                            # Filter the data for the selected quarter and year
                            filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                            # Group by year and sum the transaction amount and count
                            grouped_data_user_dev_quarter = filtered_data_year.groupby(["State", "Agg_User_device"]).agg({"Agg_User_count": "sum"}).reset_index()

                            # Plot chart for transaction amount over years
                            fig_quarter_user_count_state = px.bar(grouped_data_user_dev_quarter, x="State", y="Agg_User_count", color_discrete_sequence= ["green"], height=500, width=800, title=f"Agg User by State for {(selected_year_slr, quarter)}",
                                            labels={"Agg_User_count": "User"})
                            st.plotly_chart(fig_quarter_user_count_state)

                            
                            grouped_data_user_quarter = filtered_data_year.groupby("Agg_User_device").agg({
                                                                            "Agg_User_count": "sum", "Agg_Device_Percentage": "sum"
                                                                        }).reset_index()
                            
                            df_agg_us_qr_sorted = grouped_data_user_quarter.sort_values(by='Agg_User_count', ascending=False)
                            
                            fig_qr_user_count_dev = px.bar(df_agg_us_qr_sorted, 
                                            x="Agg_User_device", 
                                            y="Agg_User_count",
                                            hover_name="Agg_User_device",
                                            title=f"Agg User count by device for {(selected_year_slr, quarter)}",
                                            labels={"Agg_User_count": "User Count", 
                                                    "Agg_User_device": "User Device"})

                            st.plotly_chart(fig_qr_user_count_dev)
                        

                        grouped_data_yearwise_agg_user =dataframe.groupby("Year").agg({"Agg_User_count": "sum", "Agg_Device_Percentage": "sum"}).reset_index()

                        st.subheader('Aggregate User Count by by Year')
                        agg_user_yr_ct = px.bar(grouped_data_yearwise_agg_user, x='Year', y='Agg_User_count', color='Year', title='Aggregate User Count by Year')
                        st.plotly_chart(agg_user_yr_ct)

                        grouped_data_state_agg_user =dataframe.groupby("State").agg({"Agg_User_count": "sum", "Agg_Device_Percentage": "sum"}).reset_index()
                        df_agg_us_sorted = grouped_data_state_agg_user.sort_values(by='Agg_User_count', ascending=True)

                        st.subheader('Aggregate User Count by State')
                        agg_user_st_ct = px.histogram(df_agg_us_sorted, x='State', y='Agg_User_count', color="State", height=500, width=800, title='Aggregate User Count by state')
                        st.plotly_chart(agg_user_st_ct)

                        grouped_data_device_agg_user =dataframe.groupby("Agg_User_device").agg({"Agg_User_count": "sum", "Agg_Device_Percentage": "sum"}).reset_index()

                        st.subheader('Aggregate User Count by device')
                        agg_user_device_count = px.bar(grouped_data_device_agg_user, x='Agg_User_device', y='Agg_User_count', color_discrete_sequence=['red'], hover_name="Agg_User_device", title='Aggregate User Count by device')
                        st.plotly_chart(agg_user_device_count)
                    
        with tab2:

            Method2 = st.selectbox("select a option", ["Map Transaction Analysis", "Map User Analysis"])

            if Method2=="Map Transaction Analysis":
                from dataframe_with_sql import retrieve_dataframe

                dataframe= retrieve_dataframe("map_trans")

                col1, col2 = st.columns(2)

                with col1:

                    from dataframe_with_sql import retrieve_dataframe
                    
                    st.subheader("Year Analysis")

                    selected_map_year_slr = st.slider("Year Map", min_value=2018, max_value=2023)

                    # Filter the data for the selected year
                    filtered_data_map_year = dataframe[dataframe["Year"] == selected_map_year_slr]

                    # Group by year and sum the transaction amount and count
                    grouped_data_map_state_year = filtered_data_map_year.groupby("State").agg({"Map_Transaction_amount": "sum", "Map_Transaction_count": "sum"}).reset_index()

                    # Plot chart for transaction amount over years
                    fig_year_map_trans_amount = px.bar(grouped_data_map_state_year, x="State", y="Map_Transaction_amount", color_discrete_sequence=["yellow"], height=700, width=650, title=f"Total Transaction Amount by State  for {selected_map_year_slr}",
                                    labels={"Transaction_amount": "Total Map Transaction Amount"})
                    st.plotly_chart(fig_year_map_trans_amount)

                    fig_year_count = px.line(grouped_data_map_state_year, x="State", y="Map_Transaction_count", height=600, width=650, title=f"Total Transaction Count by State for  {selected_map_year_slr}",
                            labels={"Map_Transaction_count": "Total Map Transaction Count"}, color_discrete_sequence=["pink"],  markers=True)

                    fig_year_count.update_traces(marker=dict(size=6, symbol='circle', color='blue'))

                    st.plotly_chart(fig_year_count)

 
                with col2:
                    st.subheader("Quarter Analysis")
                    quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quarter = st.selectbox("Map_Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                    selected_quarter = quarter_map[quarter]

                    filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                    grouped_data_state_quarter = filtered_data_quarter.groupby("State").agg({"Map_Transaction_amount": "sum", "Map_Transaction_count": "sum"}).reset_index()

                    fig_quarter_Map_amount = px.bar(grouped_data_state_quarter, x="State", y="Map_Transaction_amount", color_discrete_sequence=["yellow"],height=700, width=650,
                                        title=f"Map Transaction Amount by State for {quarter} {selected_year_slr}",
                                        labels={"Map_Transaction_amount": "Total Map  Transaction Amount"})
                    st.plotly_chart(fig_quarter_Map_amount)

                    fig_quarter_Map_count = px.line(grouped_data_state_quarter, x="State", y="Map_Transaction_count", height=600, width=650,
                                title=f"Map  Transaction Count by State for {quarter} {selected_year_slr}", labels={"Map Transaction_count": "Total Map Transaction Count"}, color_discrete_sequence=["pink"],  markers=True)


                    # Customize marker appearance
                    fig_quarter_Map_count.update_traces(marker=dict(size=6, symbol='circle', color='blue'))
                    st.plotly_chart(fig_quarter_Map_count)



                st.header("Map Transaction Amount And Count By Year")

                grouped_data_yearwise_map_trans =dataframe.groupby("Year").agg({"Map_Transaction_amount": "sum", "Map_Transaction_count": "sum"}).reset_index()

                st.subheader('Map Transaction Amount by Year')
                map_trans_yr_amt = px.bar(grouped_data_yearwise_map_trans, x='Year', y='Map_Transaction_amount', color='Year', title='Map Transaction Amount by Year')
                st.plotly_chart(map_trans_yr_amt)

                st.subheader('Map Transaction count by Year')
                map_trans_yr_ct = px.funnel(grouped_data_yearwise_map_trans, x='Year', y='Map_Transaction_count', color="Year", 
                                            title='Map Transaction count by Year',  orientation='v') 
                                            

                st.plotly_chart(map_trans_yr_ct)

                grouped_data_st_map_trans =dataframe.groupby("State").agg({"Map_Transaction_amount": "sum", "Map_Transaction_count": "sum"}).reset_index()

                

                df_melted = dataframe.melt(id_vars='State', value_vars=['Map_Transaction_amount', 'Map_Transaction_count'], var_name='Metric', value_name='Value')


                fig = px.bar(df_melted, x='State', y='Value', color='Metric', barmode='group', title='Transaction Amount and Count by State')

                st.plotly_chart(fig)

                
            elif Method2=="Map User Analysis":
                from dataframe_with_sql import retrieve_dataframe

                dataframe= retrieve_dataframe("map_user")

                st.title("Map User Analysis")
                

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Year Analysis")
                    selected_year_slr = st.slider("Map_User_Year", min_value=2018, max_value=2023)

                    # Filter the data for the selected year
                    filtered_data_year = dataframe[dataframe["Year"] == selected_year_slr]

                    # Group by year and sum the transaction amount and count
                    grouped_data_map_user_st_year = filtered_data_year.groupby("State").agg({"Registered_Users": "sum", "App_Opens":"sum"}).reset_index()
                    fig_st_rgus=px.bar(grouped_data_map_user_st_year, x="State", y="Registered_Users", color_discrete_sequence=['violet'], height=650, width=600, title=f"Registered Map User by State for {selected_year_slr}",
                            labels={"map_User_count": "count"})
                    st.plotly_chart(fig_st_rgus)


                    grouped_data_map_user_st_year = filtered_data_year.groupby("State").agg({"Registered_Users": "sum", "App_Opens":"sum"}).reset_index()
                    fig_st_appop=px.line(grouped_data_map_user_st_year, x="State", y="App_Opens", color_discrete_sequence=["black"], title=f"App Opens by State for {selected_year_slr}", height=500,
                            labels={"map_User_count": "count"})
                    st.plotly_chart(fig_st_appop)


                with col2:
                    st.subheader("Quarter Analysis")
                    quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quarter = st.selectbox("Map_us_Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                    selected_quarter = quarter_map[quarter]

                    # Filter the data for the selected quarter and year
                    filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                    # Group by year and sum the transaction amount and count

                    grouped_data_map_user_st_qr = filtered_data_quarter.groupby("State").agg({"Registered_Users": "sum", "App_Opens":"sum"}).reset_index()
                    fig_st_qr_rgus=px.bar(grouped_data_map_user_st_qr, x="State", y="Registered_Users", color_discrete_sequence=['violet'], height=650, width=600, title=f"Map User by State for  {(selected_year_slr, quarter)}",
                            labels={"map_User_count": "count"})
                    st.plotly_chart(fig_st_qr_rgus)


                    fig_stqr_appop=px.line(grouped_data_map_user_st_qr, x="State", y="App_Opens", height=500, color_discrete_sequence=["black"], title=f"App opens by State for {(selected_year_slr, quarter)}",
                            labels={"map_User_count": "count"})
                    st.plotly_chart(fig_stqr_appop)



                grouped_data_map_rguser_st = dataframe.groupby("State").agg({"Registered_Users": "sum", "App_Opens": "sum"}).reset_index()

                # Sort the DataFrame by Registered_Users in descending order
                df_sorted = grouped_data_map_rguser_st.sort_values(by='Registered_Users', ascending=False)
                
                fig_year_state_maprg_user_ct = px.bar(df_sorted, x="State", y="Registered_Users", color="State", height=600, width=800, title="Map User by State",
                            labels={"map_User_count": "User"})
                st.plotly_chart(fig_year_state_maprg_user_ct)

                grouped_data_map_rguser_year = dataframe.groupby("Year").agg({"Registered_Users": "sum", "App_Opens" :"sum"}).reset_index()


                fig_year_state_maprg_user_ct = px.bar(grouped_data_map_rguser_year, x="Year", y="Registered_Users", color="Year", height=500, width=800, title="Map User by Year",
                                labels={"map_User_count": "count"})
                st.plotly_chart(fig_year_state_maprg_user_ct)

                fig = px.bar(grouped_data_map_rguser_st, x="State", y="App_Opens", color_discrete_sequence=["skyblue"], height=600, width=800, title="Map App Opens by State",
                    labels={"App_Opens": "count"})
                st.plotly_chart(fig)


                grouped_data_map_rguser_dis = dataframe.groupby("Districts").agg({"Registered_Users": "sum", "App_Opens": "sum"}).reset_index()


                fig_year_state_maprg_user_ct = px.bar(grouped_data_map_rguser_dis, x="Districts", y="Registered_Users",  height=450, width=800, title="Map User by Districts", color_discrete_sequence=["red"],
                                labels={"map_User_count_dis": "User"})
                st.plotly_chart(fig_year_state_maprg_user_ct)

        with tab3:
            Method3 = st.selectbox("select a option", ["Top Transaction Analysis", "Top User Analysis"])

            if Method3=="Top Transaction Analysis":
                
                from dataframe_with_sql import retrieve_dataframe

                dataframe = retrieve_dataframe("top_trans")

                
                col1, col2 = st.columns(2)
                
                dataframe = retrieve_dataframe("top_trans")

                with col1:
                    st.subheader("Year Analysis")
                    selected_year_slr = st.slider("Top_Year", min_value=2018, max_value=2023)

                    # Filter the data for the selected year
                    filtered_data_year = dataframe[dataframe["Year"] == selected_year_slr]

                    # Group by year and sum the transaction amount and count
                    grouped_data_top_state_year = filtered_data_year.groupby("State").agg({"Transaction_Amount": "sum", "Transaction_Count": "sum"}).reset_index()

                    # Plot chart for transaction amount over years
                    fig_year_amount = px.bar(grouped_data_top_state_year, x="State", y="Transaction_Amount", color="State", height=500, width=800,  title=f"Top Total Transaction Amount by State for {selected_year_slr}",
                                    labels=({"Transaction_Amount": "Top Total Transaction Amount"}))
                    st.plotly_chart(fig_year_amount)

                    fig_yearstate_count = px.line(grouped_data_top_state_year, 
                                x="State", 
                                y="Transaction_Count", 
                                height=500,
                                title=f"Top Total Transaction Count by State for {selected_year_slr}",
                                labels={"Transaction_Count": "Total Top Transaction Count"})

                    # Customizing the line and marker colors, and enabling markers
                    fig_yearstate_count.update_traces(line=dict(color='green'), 
                                                    marker=dict(color='purple'), 
                                                    mode='lines+markers')

                    # Display the plot in the Streamlit app
                    st.plotly_chart(fig_yearstate_count)

                with col2:
                    st.subheader("Quarter Analysis")
                    quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quarter = st.selectbox("Top_Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                    selected_quarter = quarter_map[quarter]

                    # Filter the data for the selected quarter and year
                    filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                    # Group by quarter and sum the transaction amount and count
                    grouped_data_state_quarter = filtered_data_quarter.groupby("State").agg({"Transaction_Amount": "sum", "Transaction_Count": "sum"}).reset_index()

                    # Plot chart for transaction amount for the selected quarter
                    fig_quarter_amount = px.bar(grouped_data_state_quarter, x="State", y="Transaction_Amount", color="State", height=500, width=800,
                                        title=f"Top Total Transaction Amount by State for {quarter} {selected_year_slr}",
                                        labels={"Transaction_Amount": "Top Total Transaction Amount"})
                    st.plotly_chart(fig_quarter_amount)

                    fig_quarter_count = px.line(grouped_data_state_quarter, 
                                x="State", 
                                y="Transaction_Count",
                                height=500, 
                                title=f"Top Total Transaction Count by State for {quarter} {selected_year_slr}",
                                labels={"Transaction_Count": "Top Total Transaction Count"})

                    # Customizing the line and marker colors
                    fig_quarter_count.update_traces(line=dict(color='green'), 
                                                    marker=dict(color='purple', size=6), 
                                                    mode='lines+markers')

                    # Display the plot in the Streamlit app
                    st.plotly_chart(fig_quarter_count)


                grouped_data_yearwise_top_trans =dataframe.groupby("Year").agg({"Transaction_Amount": "sum", "Transaction_Count": "sum"}).reset_index()


                st.subheader('Top Transaction Amount by Year')
                top_trans_yr_amt = px.bar(grouped_data_yearwise_top_trans, x='Year', y='Transaction_Amount', color='Year',  labels=({"Transaction_Amount": "Top Total Transaction Amount"}), title='Top Transaction Amount by Year')
                st.plotly_chart(top_trans_yr_amt)
                
                top_yr_df_sorted = grouped_data_yearwise_top_trans.sort_values(by='Year', ascending=True)

                st.subheader('Top Transaction count by Year')
                top_trans_yr_ct = px.bar(top_yr_df_sorted, x='Year', y='Transaction_Count',labels=({"Transaction_Count": "Top Total Transaction Count"}), title='Top Transaction count by Year', color_discrete_sequence=["red"])
                st.plotly_chart(top_trans_yr_ct)

                # # Grouping the data by state
                grouped_data_state_top_trans = dataframe.groupby("State").agg({"Transaction_Amount": "sum", "Transaction_Count": "sum"}).reset_index()

                top_df_sorted = grouped_data_state_top_trans.sort_values(by='Transaction_Amount', ascending=False)

                # # Creating a bar chart
                fig = px.bar(top_df_sorted, x='State', y='Transaction_Amount', 
                             title='Top Transaction Amount by State', color="State", height=500, width=750,
                            labels={'Transaction_Amount': 'Top Total Transaction Amount', 'State': 'State'},
                            )

                st.plotly_chart(fig)
                    
            elif Method3=="Top User Analysis":
                from dataframe_with_sql import retrieve_dataframe
            
                # Retrieve the data
                
                dataframe = retrieve_dataframe("top_user")

                grouped_data_yearwise_top_user =dataframe.groupby("Year").agg({"Registered_User": "sum"}).reset_index()


                st.subheader('Top User Count by Year')
                top_user_yr_ct = px.bar(grouped_data_yearwise_top_user, x='Year', y='Registered_User', color='Year', title='Top User Count by Year')
                st.plotly_chart(top_user_yr_ct)

                grouped_data_state_top_user =dataframe.groupby("State").agg({"Registered_User": "sum"}).reset_index()

                top_us_yr_df_sorted = grouped_data_state_top_user.sort_values(by='State', ascending=True)

                st.subheader('Top User Count by State')
                top_user_st_ct = px.bar(top_us_yr_df_sorted, x='State', y='Registered_User', color_discrete_sequence=["purple"], height=600, width=800, title='Top User Count by state')
                st.plotly_chart(top_user_st_ct)

                # grouped_data_qr_top_user =dataframe.groupby("Quarter").agg({"Registered_User": "sum"}).reset_index()

                grouped_data_statewise =dataframe.groupby("Quarter").agg({"Registered_User": "sum"}).reset_index()

                st.subheader('Top User Count by Quarter')
                top_user_count = px.funnel(grouped_data_statewise, x='Quarter', y='Registered_User', color="Quarter", hover_name="Quarter",
                                            title='Top Registered User Count by Quarter',     orientation='h')
                                              # Set orientation to 'h' for a vertical funnel chart

                st.plotly_chart(top_user_count)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Year Analysis")
                    selected_year_slr = st.slider("Top_User_Year", min_value=2018, max_value=2023)

                    # Filter the data for the selected year
                    filtered_data_year = dataframe[dataframe["Year"] == selected_year_slr]

                    # Group by year and sum the transaction amount and count
                    grouped_data_top_user_st_year = dataframe.groupby("State").agg({"Registered_User": "sum"}).reset_index()

                    top_us_yr_df_sort = grouped_data_top_user_st_year.sort_values(by='State', ascending=True)

                    # Creating the bar chart
                    fig_year_state_top_rguser_ct = px.bar(
                        top_us_yr_df_sort,
                        x="State",
                        y="Registered_User",
                        color="State",
                        height=400,
                        width=800,
                        title=f"Top Registered User by State for {selected_year_slr}",
                        labels={"Registered_User": "Top Total Registered User"}
                    )
                    st.plotly_chart(fig_year_state_top_rguser_ct)

                    grouped_data_pin_yr_top_user =dataframe.groupby("Pincodes").agg({"Registered_User": "sum"}).reset_index()

                    fig_yrw_rguser_count_pin = px.histogram(grouped_data_pin_yr_top_user, 
                                   x="Pincodes", 
                                   y="Registered_User",
                                   color_discrete_sequence=["orange"],
                                   hover_name="Pincodes",
                                   height=500,
                                   width=650,
                                   title=f"Top Registered User count by Pincodes{selected_year_slr}",
                                   labels={"Registered_User": "Top User Count"})
                    st.plotly_chart(fig_yrw_rguser_count_pin)     

                with col2:
                    st.subheader("Quarter Analysis")
                    quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quarter = st.selectbox("Top_us_Quarter", ["Q1", "Q2", "Q3", "Q4"], index=0)

                    selected_quarter = quarter_map[quarter]

                    # Filter the data for the selected quarter and year
                    filtered_data_quarter = dataframe[(dataframe["Year"] == selected_year_slr) & (dataframe["Quarter"] == selected_quarter)]

                    # Group by year and sum the transaction amount and count

                    grouped_data_top_user_st_qr = dataframe.groupby("State").agg({"Registered_User": "sum"}).reset_index()

                    top_us_qr_df_sort = grouped_data_top_user_st_qr.sort_values(by='State', ascending=False)

                    # Creating the bar chart
                    fig_qr_state_top_rguser_ct = px.bar(
                        top_us_qr_df_sort,
                        x="State",
                        y="Registered_User",
                        color="State",
                        height=550,
                        width=800,
                        title=f"Top Registered User by State for {(selected_year_slr, quarter)}",
                        labels={"Registered_User": "Top Total Registered User"}
                    )
                    st.plotly_chart(fig_qr_state_top_rguser_ct)

                    grouped_data_pin_qr_top_user =dataframe.groupby("Pincodes").agg({"Registered_User": "sum"}).reset_index()


                    fig_qr_rguser_count_pin = px.histogram(grouped_data_pin_qr_top_user, 
                                   x="Pincodes", 
                                   y="Registered_User",
                                   color_discrete_sequence=["orange"],
                                   hover_name="Pincodes",
                                   height=500,
                                   width=650,
                                   title=f"Top Registered User count by Pincodes{(selected_year_slr, quarter)}",
                                   labels={"Registered_User": "Top User Count"})
                    st.plotly_chart(fig_qr_rguser_count_pin)
                
elif select=="TOP CHART":
    
        from top_chart import retrieve_top_data  # Ensure this import path is correct

        st.title("Top 10 Charts")

        Top_Chart = st.selectbox("Select a option", ["Transactions", "Users"])

        if Top_Chart == "Transactions":
            metric = st.selectbox("Select metric", ["count", "amount"])
            top_states, top_districts, top_pincodes = retrieve_top_data("Transactions", metric)
            
            # Display for top states
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 States by Total Transaction " + ("Count and Average" if metric == "count" else "Amount and Average"))
                st.dataframe(top_states)
            
            with col2:
                if metric == "count":
                    fig = px.pie(top_states, values='Total', names='State', title="Top 10 States - Total Transaction Count", labels={'State': 'State'}, hole=0.3)
                else:
                    top_df_sorted = top_states.sort_values(by='Total', ascending=False)

                    fig = px.bar(top_df_sorted, x="State", y='Total', title="Top 10 States - Total Transaction Amount", color='Average', hover_name="State")
                    st.plotly_chart(fig)
            
            # Display for top districts
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Districts by Total Transaction " + ("Count and Average" if metric == "count" else "Amount and Average"))
                st.dataframe(top_districts)
            
            with col2:
                if metric == "count":
                    fig = px.histogram(top_districts, x='District', y='Total', title="Top 10 Districts - Total Transaction " + ("Count" if metric == "count" else "Amount"),
                            labels={'District': 'District', 'Total': 'Transaction ' + ("Count" if metric == "count" else "Amount")})
                    st.plotly_chart(fig)
                    # fig = px.pie(top_districts, values='Total', names='District', title="Top 10 Districts - Total Transaction Count", labels={'District': 'District'})
                else:
                    fig = px.funnel(top_districts, x="District", y='Total', title="Top 10 Districts - Total Transaction Amount",
                                     color="Average", orientation='v', width=800)

                    # fig = px.histogram(top_districts, x="District", y='Total', title="Top 10 Districts - Total Transaction Amount", color="Average")
                    st.plotly_chart(fig)
            
            # Display for top pincodes
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Pincodes by Total Transaction " + ("Count and Average" if metric == "count" else "Amount and Average"))
                st.dataframe(top_pincodes)
            
            with col2:
                if metric == "count":
                    fig = px.pie(top_pincodes, values='Pincodes', names='Total', title="Top 10 Pincodes - Total Transaction Count", color='Pincodes')
                else:
                    fig = px.pie(top_pincodes, values='Pincodes', names='Average', title="Top 10 Pincodes - Total Transaction Amount", color='Total')

                st.plotly_chart(fig)


        elif Top_Chart == "Users":
            top_states, top_districts, top_pincodes = retrieve_top_data("Users", "count")
            
            # Display for top states
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 States by Total Users and Average")
                st.dataframe(top_states)
            
            with col2:
                st.subheader("Top 10 States by Total Users - Average")
                fig = px.pie(top_states, names='State', values='Total', title="Top 10 States - Total Users and Average", 
                        hover_data=['Average'], hole=0.3)
                st.plotly_chart(fig)
        
            # Display for top districts
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Districts by Total Users and Average")
                st.dataframe(top_districts)
            
            with col2:
            # Plot the bar chart
                fig = px.bar(top_districts, x='District', y='Total', color='District', title="Top 10 Districts - Total Users By Top 10  Districts")
                st.plotly_chart(fig)
                # st.subheader("Top 10 Districts by Total Users - Average")
                # fig = px.scatter(top_districts, x='District', y='Total', title="Top 10 Districts - Total Users")
                # st.plotly_chart(fig)
            
            # Display for top pincodes
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Pincodes by Total Users and Average")
                st.dataframe(top_pincodes)
            
            with col2:
                st.subheader("Top 10 Pincodes by Total Users")

                fig = px.pie(top_pincodes, values='Total', names='Pincodes',
                        title="Total Users By Top 10 Pincodes")
                st.plotly_chart(fig)
                