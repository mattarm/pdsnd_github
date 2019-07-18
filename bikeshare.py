#!/usr/bin/env python
# coding: utf-8

# In[57]:


import time
import pandas as pd
import numpy as np

folder = '../bikeshare-2/'

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

##function to get user input for filters of the dataset
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!\n\n')
    
    #get city from input
    valid_cities = ['chicago','new york city','washington']
    city = input('City of interest: Chicago, New York City or Washington\n').lower()
    #check for valid city input
    while city not in valid_cities:
        print('Please provide a valid response.')
        city = input('\nCity of interest: Chicago, New York City or Washington\n').lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['january','february','march','april','may','june','all']
    month = input('\nMonth of departure: January-June or ALL\n').lower()
    #check for month valid input
    while month not in valid_months:
        print('Please provide a valid response.')
        month = input('\nMonth of departure: January-June or ALL\n').lower()
        
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['monday','tuesday', 'wednesday','thursday','friday','saturday','sunday','all']
    day = input('\nDay of departure: Monday, Tuesday, .. Sunday or ALL\n').lower()
    #check for valid day input
    while day not in valid_days:
        print('Please provide a valid response.')
        day = input('\nDay of departure: Monday, Tuesday, .. Sunday or ALL\n').lower()

    print('-'*40)
    return city, month, day

##load the data using the inputs from get_filters()
def load_data(city, month, day):

    folder = '../bikeshare-2/'
    
    #Load data for city
    df = pd.read_csv(folder + CITY_DATA[city],index_col=0)
    print('You are viewing ride data from {}'.format(city.upper()))
    
    #convert datetime to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    ##capitalize month so it works with dt.month_name()
    month = month.capitalize()
    ##filter for month, unless month==All
    if month != 'All':
        df = df[df['Start Time'].dt.month_name() == month]
        print('For rides starting in {}'.format(month))
    else:
        print('For rides in every month available')

    ##capitalize day so it works with dt.day_name()
    day = day.capitalize()
    ##filter for input day, unless input == All
    if day != 'All':
        df = df[df['Start Time'].dt.day_name() == day]
        print('For rides starting on {}'.format(day))
    else:
        print('For every day of the week\n.')
    
    #print number of records returned
    print('This includes {} rides'.format(len(df)))
    
    return df

##run analysis for time stats - find most popular month, day & hour
def time_stats(df, month, day):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    #start_time = time.time()

    # display the most common month
    if month == 'all':
        #get month group object
        pop_month = df.groupby(df['Start Time'].dt.month).size()
        #idxmax gives index of most popular month
        max_month = pop_month.idxmax()
        #get number of rides for max_month
        month_rides = pop_month[max_month]
        print('The most popular MONTH was\n{} with {} RIDES\n'.format(max_month, month_rides))


    # display the most common day of week
    #same process as month
    if day == 'all':
        pop_day = df.groupby(df['Start Time'].dt.day).size()
        max_day = pop_day.idxmax()
        day_rides = pop_day[max_day]
        print('The most popular DAY of the week was\n{} with {} RIDES\n'.format(max_day, day_rides))


    # display the most common start hour
    #same process as month
    pop_hour = df.groupby(df['Start Time'].dt.hour).size()
    max_hour = pop_hour.idxmax()
    hour_rides = pop_hour[max_hour]
    print('The most common departing HOUR was\n {} with {} RIDES'.format(max_hour, hour_rides))

    #print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

##funtion to get the most popular item & the number of rides associated with it
def most_pop(df, field):
    #function for finding max of a group
    #make group for df and field
    grouper_obj = df.groupby(df[field]).size()
    #get name of most popular group
    item = grouper_obj.idxmax()
    #get count of most popular group
    count = grouper_obj[item]
    print('Most popular {}: is {} with {} rides'.format(field, item, count))
    
##get station_stats for most common start station, end station and combo of the two
def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    #start_time = time.time()

    # display most commonly used start station
    most_pop(df, 'Start Station')

    # display most commonly used end station
    most_pop(df, 'End Station')

    #calc & display most popular trip
    combo_group = df.groupby(['Start Station','End Station']).size()
    pop_combo = combo_group.idxmax()
    combo_rides = combo_group[pop_combo]
    start = pop_combo[0]
    end = pop_combo[1]
    print('Most common ride was made {} times.\nDeparting: {}\nArriving: {}\n'.format(combo_rides, start, end))

    #print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

##stats for travel time, total time, average trip time, max trip time in seconds, minutes, hours, days
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    #start_time = time.time()

    # display total travel time
    tt = sum(df['Trip Duration'])
    print('Total travel time in seconds: {}'.format(tt))
    print('Total travel time in minutes: {}'.format(round(tt/60),2))
    print('Total travel time in hours: {}'.format(round(tt/60/60),2))
    print('Total travel time in days{}\n'.format(round(tt/60/60/24),2))
    
    # display mean travel time
    avg_tt = df['Trip Duration'].mean()
    print('Average travel time in seconds: {}'.format(round(avg_tt,2)))
    print('Average travel time in minutes: {}'.format(round(avg_tt/60,2)))
    print('Average travel time in hours: {}'.format(round(avg_tt/60/60,2)))
    print('Average travel time in days: {}\n'.format(round(avg_tt/60/60/24,2)))
    
    #display max travel time
    max_tt = df['Trip Duration'].max()
    print('Max travel time in seconds: {}'.format(max_tt))
    print('Max travel time in minutes: {}'.format(max_tt/60))
    print('Max travel time in hours: {}'.format((max_tt/60/60)))
    print('Max travel time in days: {}'.format(max_tt/60/60/24))
    
    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
##user tpe analysis, how many rides for each type of rider
def cust_type_stats(df):
    cust_types = df['User Type'].unique()
    type_rides = df.groupby('User Type').size().sort_values(ascending=False)
    for t in cust_types:
        print('{} customers took {} trips'.format(t, type_rides[t]))
    print('\n')
        

##gender analysis, how many rides for each sex
def gender_stats(df):
    genders = df['Gender'].unique()
    rides_by_gender = df.groupby('Gender').size()
    for g in genders:
        print('{} customers took {} trips'.format(g, rides_by_gender[g]))    
    print('\n')    
    
##age analysis, oldest, youngest, average age and number of rides
def age_stats(df):
    #age group object
    age_groups = df.groupby('Birth Year').size()
    
    #get min birth year
    old = int(df['Birth Year'].min())
    #number of rides for customers with birth year = old ^^
    old_rides = age_groups[old]
    
    #repeat old for young
    young = int(df['Birth Year'].max())
    young_rides = age_groups[young]
    
    #repeat for most common
    mode = int(df['Birth Year'].mode())
    mode_rides = age_groups[mode]
    
    print('Oldest riders were born in: {}.  Took {} rides'.format(old, old_rides))
    print('Youngest riders were born in: {}.  Took {} rides'.format(young, young_rides))
    print('Most common birth year was: {}.  Took {} rides\n'.format(mode, mode_rides)) 


##age, gender, cust_type when the data is present    
def user_stats(df, city):

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    
    #calc user types for all
    if city == 'washington':
        cust_type_stats(df)
    #calc gender & age for !washington, drop NaN for nyc & chicago
    else:
        df = df.dropna(subset=['User Type','Gender'])
        cust_type_stats(df)
        gender_stats(df)
        age_stats(df)
    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


##run the program
##get inputs
##check for valid inputs
##load data
##filter data
##run analysis
##option to print data
##restart or terminate
def main():
    while True:
        #get filters, set city, month, day
        city, month, day = get_filters()
        #build df
        df = load_data(city, month, day)
       
        #proceed if df contains records
        if len(df) > 0:
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            
            #to display data
            i=0
            more_data = input('Would you like to see 5 lines of the dataframe?  Enter yes or no.\n').lower()
            while more_data == 'yes':
                print(df[i:i+5])
                i += 5
                more_data = input('Would you like to see 5 lines of the dataframe?  Enter yes or no.\n').lower()
                
        #if there's no data in the df prompt for restart
        else:
            print('There is no ride data for this selection.')
        
        #restart prompt
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()