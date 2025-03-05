import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide',page_title = 'StartUp Analysis')

df = pd.read_csv('/Users/ajayrajak/Downloads/node js/PythonProject1/startUp_clean.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month']=df['date'].dt.month

# GENERAL ANALYSIS
def load_over_all_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total  = df['amount'].sum()

    # maximum amount infused in a company
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # Avg Amount infused
    mean_funding = df.groupby('startup')['amount'].sum().mean()

    #total funded startups
    funded_startups = df['startup'].nunique()

    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.metric('Total Amount Invested', str(total) + 'Cr')
    with col2:
        st.metric('Maximum Amount Infused in a company', str(max_funding) + 'Cr')
    with col3:
        st.metric('Mean Amount Infused in a companies', str(round(mean_funding)) + 'Cr')
    with col4:
        st.metric('Total Number Of Funded Startups', str(funded_startups))

    st.header('Month On Month Analysis')
    st.subheader('Investment Stage')
    selected_option = st.selectbox('Select Type', ['Total', 'count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig5)



# INVESTOR

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2, = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    col3, col4, = st.columns(2)
    with col3:
        stage_series = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
        st.subheader('Investment Stage')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series, labels=stage_series.index, autopct="%0.1f%%")

        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('Investment Stage')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.1f%%")

        st.pyplot(fig3)
    # year on year investmen
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)

    st.pyplot(fig2)

# side title bar


st.sidebar.title('Start Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Start Up','Investor'])
if option == 'Overall Analysis':
    load_over_all_analysis()

elif option == 'Start Up':
    st.sidebar.selectbox('Select Start Up',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Start Up Details')
    st.title('Start Analysis')

elif option == 'Investor':
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
