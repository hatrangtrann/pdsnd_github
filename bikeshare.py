import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'data/chicago.csv', 'Chicago': 'data/chicago.csv',
             'New York City': 'data/new_york_city.csv', 'New york city': 'data/new_york_city.csv',
              'new york city': 'data/new_york_city.csv', 'washington': 'data/washington.csv',
             'Washington': 'data/washington.csv' }

def get_filters():
    """
    Request user to input data of a city, month, and day to analyze.

    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    city = input('\nWhich city data you want to see? : Chicago, New York, or Washington: ').lower()
    while city not in CITY_DATA.keys():
         print('That\'s not a valid entry!')
         city = input('\nWhich city data to see? : Chicago, New York, or Washington: ').lower()

    print(f"\nYou have chosen {city.title()} as your city.")
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, for which you're seeking the data:")
        print("\nAccepted input:\nFull month name; not case sensitive (e.g. january or JANUARY).\nFull month name in title case (e.g. April).")
        print("\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        print("\nAccepted input:\nDay name; not case sensitive (e.g. monday or MONDAY).\nDay name in title case (e.g. Monday).")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")

    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """
	Shows statistics on the most frequent times of travel based on given data.

    Args:
        param1 (df): The data frame you want to analyze.

    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def station_stats(df):
    """
	Shows statistics on the most popular stations and trip based on the given data.

    Args:
        param1 (df): The data frame you want to analyze.

    Returns:
        Print out the result.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station: {common_end_station}")
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print(f"\nThe most frequent combination of trips are from {combo}.")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def trip_duration_stats(df):
    """
    Analyzes the trip duration based on the provided data.

    Args:
        param1 (df): The data frame you want to analyze.

    Returns:
        Print out the result.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = sum(data['Trip Duration'])
    print('\nTotal travel time is: ', total_travel_time/3600, " hours")
    average_travel_time = data['Trip Duration'].mean()
    print('\nAverage travel time is: ', average_travel_time/3600, " hours")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def user_stats(df):
    """
	Shows statistics on bikeshare users based on the given data and city.

    Args:
        param1 (df): The data frame you want to analyze.
		city (str): The name of the city.
    Returns:
        Print out the user types and, if the city is 'chicago' or 'new york', also prints the user gender,
        earliest year of birth, most recent year of birth, and most common year of birth.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = data['User Type'].value_counts()
    print(user_types)
    if city in ['chicago', 'new york']:
        user_gender = data['Gender'].value_counts()
        print(user_gender)
        earliest = int(data['Birth Year'].min())
        most_recent = int(data['Birth Year'].max())
        most_common = int(data['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is: ", earliest)
        print("\nMost recent year of birth is: ", most_recent)
        print("\nThe most common year of birth is: ", most_common)
   print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def display_data(df):
    """
	Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The data frame you want to analyze.

    Returns:
        Print out the result.
    """
     while True:
        view_data = input('\nDo you wish to view data within 5 rows of a trip? Enter yes or no\n').lower()
        if view_data.lower() == 'yes':
            print('\nPlease stretch the width of your window to accomodate all columns in one horizontal row\n')
            break
        elif view_data.lower() == 'no':
            return
        else:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")

    position = 0
    while view_data == 'yes' and position <= (len(data.index)-5):
        try:
            print(data.iloc[position : position + 5])
            position += 5
            view_data = input("\nDo you want to view more data?: ").lower()
        except:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if name == "main":
	main()