import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_name():
    name = input("What is your name?\n")
    return name

def get_filters(name):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello {}! Let\'s explore some US bikeshare data!'.format(name))

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Hi, would you like to see data for Chicago, New York City or Washington?\n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter one of the cities given\n")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        decision = input("\nWould you like to filter the data by month, day, both or none?\n").lower()
        if decision in ('month', 'day', 'both', 'none'):
            if decision == "month" or decision == "both":
                while True:
                    month = input("\nWhich month? January, February, March, April, May or June?\n").lower()
                    if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                        print("Please enter one of the months given.")
                    else:
                        break #End of month
            if decision == "day" or decision == "both":
                while True:
                    try:
                        day = int(input("\nWhich day? Please enter your selection as an integer (e.g. Monday = 1)\n"))#Adding plus one due to an index of 0
                        if day > 7 or day < 1:
                            print("Please enter a number between 1 - 7")
                        else:
                            break #End of day
                    except ValueError:
                        print("Please enter an integer value")
            if decision == "month": day = "all"
            if decision == "day": month = "all"
            if decision == "none":
                month = "all"
                day = "all"
            break #end of filters
        else:
            print("Please enter one of the options given.")
            continue

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

    raw_df = pd.read_csv(CITY_DATA[city])
    df = raw_df.copy()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month # Jan = 1 Dec = 12
    df['week_day'] = df['Start Time'].dt.weekday # Mon = 0 Sun = 6

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_day'] == (day - 1)] #negative 1 as weekday index starts at 0
    return raw_df, df


def time_stats(df, city):
    """

    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """

    print('\nCalculating The Most Frequent Times of Travel in {}...\n'.format(city.title()))
    start_time = time.time()

    #setting up hour column to be used
    df['Hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = (df['month'] == popular_month).sum()
    print("Most popular month: {}\t Count: {}".format(MONTHS[popular_month - 1].title(), popular_month_count))

    # display the most common day of week
    popular_day = df['week_day'].mode()[0]
    popular_day_count = (df['week_day'] == popular_day).sum()
    print("Most popular week day: {}({})\t Count: {}".format(WEEKDAYS[popular_day], popular_day + 1, popular_day_count))

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    popular_hour_count = (df['Hour'] == popular_hour).sum()
    print("Most popular hour: {}\t Count: {}\n".format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """

    print('\nCalculating The Most Popular Stations and Trip in {}...\n'.format(city.title()))
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = (df['Start Station'] == popular_start_station).sum()
    print("Most popular Start Station: {}\t Count: {}".format(popular_start_station, popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = (df['End Station'] == popular_end_station).sum()
    print("Most popular End Station: {}\t Count: {}".format(popular_end_station, popular_end_station_count))

    # display most frequent combination of start station and end station trip
    trips = df['Start Station'] + ' -> ' + df['End Station']
    popular_trip = trips.mode()[0]
    popular_trip_count = (trips == popular_trip).sum()
    print("Most popular trip: {}\t Count: {}".format(popular_trip, popular_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """

    print('\nCalculating Trip Duration in {}...\n'.format(city.title()))
    start_time = time.time()

    df['End Time'] = pd.to_datetime(df['End Time']) #converting to datetime for calculations

    travel_time = df['End Time'] - df['Start Time']
    # display total travel time
    sum_travel_time = travel_time.sum()
    print("Total Travel Time: {}".format(sum_travel_time))
    # display mean travel time
    mean_travel_time = travel_time.mean()
    print("Average Travel Time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats in {}...\n'.format(city.title()))
    start_time = time.time()

    # Display counts of user types
    print("What is the breakdown of user types?")
    user_type_count = df.groupby(['User Type'])['User Type'].count()
    user_type_count_des = user_type_count.sort_values(ascending=False) #Putting the highest type first
    print("{}\n".format(user_type_count_des))

    # Display counts of gender
    print("What is the breakdown of gender?")
    try:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        gender_count_des = gender_count.sort_values(ascending=False) #Putting the highest gender first
        print("{}\n".format(gender_count_des))
    except KeyError:
        print("{} DATASET DOES NOT RECORD GENDER\n".format(city.upper()))
    # Display earliest, most recent, and most common year of birth
    print("What is the earliest, most recent and most common year of birth?")
    try:
        earliest_year = int(df['Birth Year'].min())
        print("Earliest year of birth: {}".format(earliest_year))
        recent_year = int(df['Birth Year'].max())
        print("Most recent year of birth: {}".format(recent_year))
        common_year = int(df['Birth Year'].mode()[0])
        print("Common year of birth: {}".format(common_year))
    except KeyError:
        print("{} DATASET DOES NOT RECORD BIRTHYEARS\n".format(city.upper()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(raw_df, city):
    """Displays the raw data from the choosen bikeshare csv file every 5 rows
    until the user quits. Also checks to see if the remaining rows are under
    5, if so it prints what is left.

    Args:
        (DataFrame) raw_df - Pandas DataFrame containing the original city data
        (str) city - name of the city to analyze
    """

    cur_row_number = 0 #index
    number_of_rows = len(raw_df.index)
    rows_to_print = 5
    while True:
        data_prompt = input("\nWould you like to see individual trip data for {}?\n".format(city.title())).lower()
        if data_prompt != 'yes' or cur_row_number >= number_of_rows:
            break
        elif ((number_of_rows - cur_row_number) < 5): #calculate the number of remaining rows to print
            rows_to_print = number_of_rows - cur_row_number
        for i, row in raw_df.iloc[cur_row_number: cur_row_number + rows_to_print].iterrows():
            print("\nIndex: {}\n{}".format(i, row))
        cur_row_number += 5

def data_pause():
    """Pauses the program and allows the user read information"""

    input("\nPlease press enter to load more data...")
    print('-'*40)

def main():
    while True:
        name = get_name()
        city, month, day = get_filters(name)
        raw_df, df = load_data(city, month, day)

        time_stats(df, city)
        data_pause()
        station_stats(df, city)
        data_pause()
        trip_duration_stats(df, city)
        data_pause()
        user_stats(df, city)
        data_pause()
        view_raw_data(raw_df, city)

        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for your time, I hope you found out something intresting")
            break
        print("\n")

if __name__ == "__main__":
	main()
