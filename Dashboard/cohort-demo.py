import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib as mpl 
from datetime import date, datetime
import streamlit as st  

st.set_page_config(
    page_title="Cohorts Dashboard",
    page_icon="📈",
    layout="wide",
)

@st.experimental_memo
def purchase_rate(customer_id):
    purchase_rate = [1]
    counter = 1
    for i in range(1,len(customer_id)):
        if customer_id[i] != customer_id[i-1]:
            purchase_rate.append(1)
            counter = 1
        else:
            counter += 1
            purchase_rate.append(counter)
    return purchase_rate
@st.experimental_memo
def join_date(date, purchase_rate):
    join_date = list(range(len(date)))
    for i in range(len(purchase_rate)):
        if purchase_rate[i] == 1:
            join_date[i] = date[i]
        else:
            join_date[i] = join_date[i-1]
    return join_date

# I do not define all the functions here because it would lengthen the article. 
# I will provide the full code at the end of the article.

st.title("Cohort Interactive Dashboard Demo")
st.markdown("""
This webapp performs cohort analysis of my_company data!
* **Python libraries used:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Shopify](https://company_name.myshopify.com/admin)
* You need to select the data file first to proceed.
""")
uploaded_file = st.file_uploader("Choose a file") # to upload file

#Code template:

if uploaded_file is not None: # this is important because without this, 
                              # when there is no file uploaded, there will be
                              # an error as df is not defined....
    df = pd.read_csv(uploaded_file) # read the file
    df_processed = process_df(df)   # clean the data
    
    # Dashboard title
    st.header("Live Dashboard")
    # Filters
    first_filter = st.selectbox('Select first filter',['Option 1', 'Option 2', 'Option 3'])

    second_filter = st.multiselect('Select second filter', ['Option 1','Option 2','Option 3','Option 4'])

    output = display_function(data_input,first_filter,second_filter)
    st.dataframe(output)
    st.download_button(label='Download csv', data=output.to_csv(), mime='text/csv') # to download the file
   
# Cohort analysis:

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df_processed = process_df(df)
    df_cohorts = cohort_numbers(df_processed)
    cohorts = cohort_percent(df_cohorts)
    
    # Dynamic title by using f-strings
    st.header(f"Live {cohorts.index[0]} to {cohorts.index[-1]} Cohort Dashboard")
    
    # Filters
    first_filter= st.selectbox('Select type of cohort',['By unique customers', 'By percentage', 'By AOV'])

    second_filter = st.multiselect('Select cohort', list(cohorts.index))

    output = select_which_table_to_draw(df_processed,first_filter,second_filter)
    st.dataframe(output)
    st.download_button(label='Download csv', data=output.to_csv(), mime='text/csv')

kpi1, kpi2, kpi3 = st.columns(3) # create 3 placeholders
if uploaded_file is not None:
    
    aov = np.mean(df['total_sales'])
    aov_goal = 95.00
    kpi1.metric(
        # label the metric
        label="AOV", 
        # calculate the metric value
        value=f"$ {round(aov,2)}",
        # calculate the change compared with the goal (arrow up/down)
        delta=f"-${round(aov_goal-aov,2)}" if aov_goal>aov else f"${round(aov-aov_goal,2)}",
    )

    nc = np.mean(df.loc[df['customer_type']=='First-time'].groupby(['day']).count()['customer_id'])
    nc_goal = 30
    kpi2.metric(
        label="New customers/day",
        value=int(nc),
        delta=f"-{round((nc_goal-nc)/nc_goal*100,2)}%" if nc_goal>nc else f"{round((nc - nc_goal)/nc_goal*100,0)}%",
    )

    rc = np.mean(df.loc[df['customer_type']=='Returning'].groupby(['day']).count()['customer_id'])
    rc_goal = 250
    kpi3.metric(
        label="Returning customers/day",
        value= int(rc),
        delta=f"-{round((rc_goal - rc)/rc_goal*100,2)}%" if rc_goal>rc else f"{round((rc-rc_goal)/rc_goal*100,2)}%"
    )