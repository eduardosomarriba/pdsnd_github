import time, datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = str()
    month = str()
    day = str()
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    print('-'*40,'\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Type the name of the city you want to analyze (chicago, new york city or washington): ")).lower()
            check = CITY_DATA[city]
            break
        except:
            print('*'*10," Oops, the city name is not typed correctly. ",'*'*10)

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Type the month of the year you would like to analyze (january to june) or type all: ")).lower()
        acceptable_month = ['all','january','february','march','april','may','june']
        if month in acceptable_month:
            break
        else:
            print('*'*10," Oops, the month is not typed correctly. ",'*'*10)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Type the day of the week (i.e. monday) you would like to analyze or type all: ")).lower()
        acceptable_day = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day in acceptable_day:
            break
        else:
            print('*'*10," Oops, the day of the week is not typed correctly. ",'*'*10)

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    df['hour'] = df['Start Time'].dt.hour
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = int(df['month'].mode()[0])
    print("The most common month is: ", month_names[popular_month])


    # TO DO: display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]
    print("The most common day of the week is: ", popular_dayofweek)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most common hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print("The most common start station is: ", popular_startstation)

    # TO DO: display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print("The most common end station is: ", popular_endstation)

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print("The most common trip is: ", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_traveltime = int(df['Trip Duration'].sum())
    print("The total travel time is: ", datetime.timedelta(seconds = total_traveltime))
    # TO DO: display mean travel time
    mean_traveltime = df['Trip Duration'].mean()
    print("The mean travel time is: ", datetime.timedelta(seconds = mean_traveltime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The breakdown of users is:\n", df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Birth Year' in df.columns:
        print("\nThe breakdown of gender is:\n", df['Gender'].value_counts())
    else:
        print('*'*10," We don't have gender data available for this city. ",'*'*10)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nYear of birth stats:")
        print("1) Earliest year of birth: ", df['Birth Year'].min())
        print("2) Most recent year of birth: ", df['Birth Year'].max())
        print("3) Most common year of birth: ", df['Birth Year'].mode()[0])
    else:
        print('*'*10," We don't have year of birth data available for this city. ",'*'*10)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays all the data of each trip at a time."""
    i = 0
    while True:
        try:
            answer = str(input("Would you like display individual trip data? Type 'yes' or 'no'. ")).lower()
            if answer != 'yes':
                break
            else:
                for x in range(i, i + 5):
                    print(df.iloc[x])
            i += 5
        except:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
