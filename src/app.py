import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.figure_factory import create_distplot


df = pd.read_csv('/Users/harshpratapsingh/Documents/ML-Projects/learning_ml/notebook/data/all_about_olypics/athlete_events.csv')
region_df = pd.read_csv('/Users/harshpratapsingh/Documents/ML-Projects/learning_ml/notebook/data/all_about_olypics/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')

st.sidebar.image('notebook/data/all_about_olypics/olympics_img.png')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'OverAll Analysis','Country-Wise Analysis', 'Athlete-Wise Analysis')
)
if user_menu=='Medal Tally':

    st.sidebar.header('Medal Tally')

    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)

    selected_country = st.sidebar.selectbox('Select country', country)
    
    medal_tally =  helper.fetch_medal_tally(df, selected_year, selected_country)
    if len(medal_tally) == 0:
        st.title('Sorry! No Awards this year for '+ selected_country+'.')
    else:
        if  selected_year=='OverAll' and selected_country == 'OverAll':
            st.title('Over-all Tally.')
        elif selected_year!='OverAll' and selected_country == 'OverAll':
            st.title('Medal Tally of ' + str(selected_year) + '-Olympics.')
        elif selected_year=='OverAll' and selected_country != 'OverAll':
            st.title('Over All Medal Tally Of ' + selected_country + ' in Olympics.')
        else:
            st.title(selected_country+"'s Medal Tally for " + str(selected_year) + '-Olympics.')
        st.table(medal_tally)


elif user_menu=='OverAll Analysis':

    st.title('Key Olympics Statistics')

    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('City')
        st.title(cities)
    with col3:
        st.header('Sport')
        st.title(sports)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Event')
        st.title(events)
    with col2:
        st.header('Athlete')
        st.title(athletes)
    with col3:
        st.header('Country')
        st.title(nations)

    nations_overtime = helper.data_overtime(df, 'region')
    nations_overtime.rename(columns={'region': 'Region'}, inplace=True)
    fig = px.line(nations_overtime, x='Edition', y='Region')
    st.title('Participating Nations in Olympics(1896-2016)')
    st.plotly_chart(fig)

    events_overtime = helper.data_overtime(df, 'Event')
    events_overtime.rename(columns={'Event': 'Events'}, inplace=True)
    fig = px.line(events_overtime, x='Edition', y='Events')
    st.title('Events in Olympics(1896-2016)')
    st.plotly_chart(fig)

    athletes_overtime = helper.data_overtime(df, 'Name')
    athletes_overtime.rename(columns={'Name': 'Athletes'}, inplace=True)
    fig = px.line(athletes_overtime,  x='Edition', y='Athletes')
    st.title('Participants in Olympics(1896-2016)')
    st.plotly_chart(fig)

    st.title('Men vs Women Participation')
    final_df = helper.women_v_men(df)
    fig = px.line(final_df, x='Year', y=['Men', 'Women'])
    st.plotly_chart(fig)

    st.title('Events in Olympics(1896-2016)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'OverAll')
    selected_sport = st.selectbox('Select the Sport Category', sport_list)

    st.title('Most Successful Athletes')
    x = helper.most_successful(df, selected_sport)
    st.table(x)

elif user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select the country', country_list )
    country_df = helper.yearwise_medal(df, selected_country)
    if len(country_df) == 0:
        st.title('Sorry! No Medals found since 1896.')
    else:
        fig = px.line(country_df, x='Year', y='Medal')
        st.title('Overall medal tally for ' + selected_country)
        st.plotly_chart(fig)
    
        st.title(selected_country + ' excels in the following sports')
        pt = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

        st.title('Top 10 Athlete from '+ selected_country)
        top10_df = helper.most_successful_countrywise_athlete(df, selected_country)
        st.table(top10_df)

elif user_menu == 'Athlete-Wise Analysis':

    df_athlete = df.drop_duplicates(subset=['Name', 'region'])

    x1 = df_athlete['Age'].dropna()
    x2 = df_athlete[df_athlete['Medal'] == 'Gold']['Age'].dropna()
    x3 = df_athlete[df_athlete['Medal'] == 'Silver']['Age'].dropna()
    x4 = df_athlete[df_athlete['Medal'] == 'Bronze']['Age'].dropna()

    fig = create_distplot([x1,x2,x3,x4],['Overall Age','Gold','Silver','Bronze'], show_hist=False, show_rug=False)

    fig.update_layout(autosize=False,width=1000, height=600)
    st.title('Medal vs Age Distribution')
    st.plotly_chart(fig)


    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water Polo', 'Hockey', 'Rowing', 'Fencing',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
        'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
        'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]


    st.title('Medal vs Age Distribution by Sport')
    selected_medal = st.selectbox("Select a Medal Category", ['Select here','Gold', 'Silver', 'Bronze'])
    selected_sports = st.multiselect('Select Sport to View Age Trend', famous_sports)

    if selected_medal != 'Select here' and selected_sports:
        x_data=[]
        name = []

        for sport in selected_sports:
            ath_df = df_athlete[(df_athlete['Sport'] == sport)]
            ages = ath_df[ath_df['Medal']==selected_medal]['Age'].dropna()
            
            if len(ages) >= 2:
                x_data.append(ages)
                name.append(sport)

        if x_data:
            fig = create_distplot(x_data, name, show_hist=False, show_rug=False)
            fig.update_layout(autosize=False, width=1000, height=600)
            st.title(f'{selected_medal} Medalist Age Distribution by Sport')
            st.plotly_chart(fig)
        else:
            st.warning(f"No valid {selected_medal} medal age data available for selected sports.")
    else:
        st.info("Please select a medal and at least one sport to view the chart.")



    st.title('Height vs Weight Relation for Winning')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Select here')
    selected_sport = st.selectbox('Select the sport here', sport_list)
    
    if selected_sport!= 'Select here':
        df_sport_w_h = helper.weight_v_height(df, selected_sport)
        # print(type(df_sport_w_h))
        # st.table(df_sport_w_h)
        # print(df_sport_w_h.shape[0])
        if df_sport_w_h.empty:
            st.warning(f"No data found for {selected_sport}")
        else:
            fig, ax = plt.subplots(figsize=(10,8))

            medal_palette = {
                'Gold': '#FFD700',     
                'Silver': '#C0C0C0',   
                'Bronze': '#CD7F32',
            }
            ax = sns.scatterplot(
                data=df_sport_w_h,
                x='Weight',
                y='Height',
                hue='Medal',
                style='Sex',
                palette=medal_palette,
                s=100,
                edgecolor='black'
            )

            ax.set_title(f'Height vs Weight of Medalists in {selected_sport}', fontsize=14)
            ax.set_xlabel("Weight (kg)")
            ax.set_ylabel("Height (cm)")
            ax.grid(True)
            plt.tight_layout()
            
            st.pyplot(fig)
    else:
        st.info("Please select a sport to view the Scatter Plot.")
            