import numpy as np

def women_v_men(df):

    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year')
    final.rename(columns={
        'Name_x' : 'Men',
        'Name_y' : 'Women'
    }, inplace=True)
    final.fillna(0, inplace=True)
    return final


def weight_v_height(df, sport):
    ath_df = df.drop_duplicates(subset=['Name','region'])
    ath_df = ath_df[ath_df['Medal'].notna()]
    sport_medalist = ath_df[ath_df['Sport']== sport]

    sport_medalist = sport_medalist.dropna(subset=['Height', 'Weight'])

    return sport_medalist


def most_successful_countrywise_athlete(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
    
    top_athlete = temp_df['Name'].value_counts().reset_index().head(10)
    merged = top_athlete.merge(temp_df, on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')

    merged.rename(columns={
        'count':'Medals',
        'region':'Region'
    }, inplace=True)

    merged = merged.reset_index(drop=True)
    merged.index = merged.index + 1

    return merged

def country_event_heatmap(df, country):
    df.dropna(subset=['Medal'], inplace=True)
    df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City', 'Sport', 'Event','Medal'], inplace = True)
    new_df = df[df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def yearwise_medal(df, country):
    df.dropna(subset=['Medal'], inplace=True)
    df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City', 'Sport', 'Event','Medal'], inplace = True)
    new_df = df[df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def most_successful(df, sport):
    temp_df = df.dropna(subset='Medal')

    if sport!='OverAll':
        temp_df = temp_df[temp_df['Sport']==sport]

    top_athlete = temp_df['Name'].value_counts().reset_index().head(15)
    merged = top_athlete.merge(temp_df, on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    merged.rename(columns={
        'count':'Medals',
        'region':'Region'
    }, inplace=True)
    merged = merged.reset_index(drop=True)
    merged.index = merged.index + 1
    return merged

def data_overtime(df, col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns={'Year':'Edition', 'count': col}, inplace=True)
    return nation_over_time

def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team','NOC', 'Games', 'Year', 'Season', 'City',	'Sport', 'Event', 'Medal'])
    
    flag=0
    if year=='OverAll' and country=='OverAll':
        temp_df = medal_df
        
    if year=='OverAll' and country!='OverAll':
        flag=1
        temp_df = medal_df[medal_df['region']==country]

    if year!='OverAll' and country=='OverAll':
        temp_df = medal_df[medal_df['Year']==int(year)]

    if year!='OverAll' and country!='OverAll':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    # if len(temp_df) == 0:
    #     return 
    # print(len(temp_df))
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year')
    else:
        x =  temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False)
    
    # print(len(x))
    x['total'] = x['Gold']+x['Silver']+x['Bronze']
    x = x.reset_index()
    x.index = x.index+1
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC', 'Games', 'Year', 'Season', 'City',	'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False)

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'OverAll')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'OverAll')

    return years, country



