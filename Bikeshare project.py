import time
import pandas as pd
import numpy as np
from statistics import mode 

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city= input('enter the letter for the city you want \n     ("ch" for chicago, "ny" for new york city, "w" for washington)\n').lower()
    #check the city
    while city not in ['ch','ny','w']:
        print("\n invalid name")
        city= input('enter the letter for the city you want \n         ("ch" for chicago, "ny" for new york city, "w" for washington)\n').lower()
        
    # get user input for month (all, january, february, ... , june)
    month= input('enter the month you want\n (january,february,march,april,may,june)\n     or wirte "all" to show all months\n').lower()
    #check the month
    months= ['january','february','march','april','may','june','all']
    while month not in months:
            print("\n invalid month")
            month= input('enter the month you want\n (january,february,march,april,may,june)\n             or wirte "all" to show all months\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('enter the day you want\n (saturday,sunday,monday,tuesday,wednesday,thursday,friday)\n     or wirte "all" to show all days\n').lower()
    #check the day
    days=['saturday', 'sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    while day not in days:
        print("\n invalid day")
        day=input('enter the day you want\n (saturday,sunday,monday,tuesday,wednesday,thursday,friday)\n         or wirte "all" to show all days\n').lower()
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data from the file into a dataframe df
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter df if user entered a spesific month (if 'all' then it will return the original df with all months)
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter df if user entered a spesific day (if 'all' then it will return the original df with all days)
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month= df['month'].mode()[0]
    print("The most common month '",common_month, "'")

    # display the most common day of week
    common_week= df['day_of_week'].mode()[0]
    print("The most common day of week '",common_week, "'")

    # display the most common start hour
    common_start_hour= df['hour'].mode()[0]
    print("The most common start hour is '",common_start_hour, "'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Common start station is '", common_start_station, "'")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Common end station is '", common_end_station, "'")

    # display most frequent combination of start station and end station trip
    df["combination station"] = df["Start Station"]+ '  ->  ' + df["End Station"]
    common_combination_station = df["combination station"].mode()[0]
    print("Common combination station is '", common_combination_station, "'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is '", total_travel_time, "'")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean of travel time is '", mean_travel_time, "'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types=df['User Type'].value_counts()
    print("The counts of user types are \n'", counts_of_user_types, "'")
    
    # wachington doesn't have data about (gender, birth year).. so we avoid it
    if city != 'w':
        
        # Display counts of gender
        counts_of_gender=df['Gender'].value_counts()
        print("The counts of gender are \n'", counts_of_gender, "'")
        
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print("\nThe earliest year is '",int(earliest_year), "'")
        
        most_recent_year = df['Birth Year'].max()
        print("\nThe most recent year of birth is '",int(most_recent_year), "'")
        
        most_common_year = mode(df['Birth Year'])
        print("\nThe most common Year is '",int(most_common_year), "'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def  display_raw_data(city) :
    """Displays the raw dataframe 5 lines by 5 lines"""
    
    # ask the user if they want to display raw data, and display it if they say 'yes', otherwise we end
    raw = input ('write "yes" to display the first 5 rows of the raw data,    otherwise press any key to end\n')
    while raw == "yes":
        try:
            for chunk in pd.read_csv(CITY_DATA[city] , chunksize=5):
                print(chunk)

                raw = input('write "yes" to display another 5 rows, otherwise enter any key to end\n')
                if raw != "yes":
                    print('Thank You')
                    break
            break
        except KeyboardInterrupt:
            print('Thank you')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()