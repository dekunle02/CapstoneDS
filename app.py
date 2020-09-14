import calendar
import pandas as pd
import numpy as np
import time
import datetime
from colorama import Fore, Style

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'
             }

MONTH_NAMES = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}
DAY_NAMES = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thur': 'Thursday', 'fri': 'Friday',
             'sat': 'Saturday', 'sun': 'Sunday'}

welcome_message = "Hello, let's explore some US BikeShare data!"
city_prompt = "Would you like to see data for (chicago, new york, or washington)?\n-> "
filter_prompt = "Would you like to filter by (month, day, or none)?\n-> "
month_prompt = f"Choose a month {tuple(MONTH_NAMES.keys())}\n-> "
day_prompt = f"Choose a day of the week {tuple(DAY_NAMES.keys())}.\n-> "
error_prompt = "There seems to be an error in your input, please type an option from choices listed above ^\n"
raw_prompt = "Would you like to see 5 lines of raw data?"

now = datetime.datetime.now()


def convert_seconds_to_string(seconds):
    return time.strftime("%H hr(s) %M min %S sec", time.gmtime(seconds))


def get_filter_pref():
    print(welcome_message)
    month = "none"
    day = "none"
    city = input(city_prompt)

    while city not in CITY_DATA.keys():
        city = input(error_prompt)

    filter_param = input(filter_prompt)
    while filter_param not in ("month", "day", "none"):
        filter_param = input(error_prompt)
    if filter_param == "month":
        month = input(month_prompt)
        while month not in MONTH_NAMES.keys():
            month = input(error_prompt)
    elif filter_param == "day":
        day = input(day_prompt)
        while day not in DAY_NAMES.keys():
            day = input(error_prompt)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != "none":
        criteria = df['month'] == MONTH_NAMES[month]
        df = df[criteria]
    if day != "none":
        criteria = df['day_of_week'] == DAY_NAMES[day]
        df = df[criteria]

    return df


def time_stats(df):
    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df.month.mode()[0]
    freq = (df.month == mode_month).sum()
    print(
        f"{Fore.BLUE}{calendar.month_name[mode_month]}{Style.RESET_ALL} is the most common month appearing {freq} times.")

    # display the most common day of week
    mode_day = df.day_of_week.mode()[0]
    freq = (df.day_of_week == mode_day).sum()
    print(
        f"{Fore.BLUE}{mode_day}{Style.RESET_ALL} is the most common day appearing {freq} times.")

    # display the most common start hour
    mode_hour = df.hour.mode()[0]
    freq = (df.hour == mode_hour).sum()
    print(
        f"{Fore.BLUE}{mode_hour}:00{Style.RESET_ALL} is the most popular hour appearing {freq} times.")

    print(f"\n{Fore.YELLOW}This took %s seconds.{Style.RESET_ALL}" % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = df["Start Station"].mode()[0]
    print(f'{Fore.BLUE}{mode_start_station}{Style.RESET_ALL} is the most common Start Station.')

    # display most commonly used end station
    mode_end_station = df["End Station"].mode()[0]
    print(f'{Fore.BLUE}{mode_end_station}{Style.RESET_ALL} is the most popular End Station.')

    # display most frequent combination of start station and end station trip
    mode_station_combo = (df["Start Station"] + " -to- " + df["End Station"]).mode()[0]
    print(f'The most common station combination is {mode_station_combo}')

    print(f"\n{Fore.YELLOW}This took %s seconds.{Style.RESET_ALL}" % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(
        f"Total Travel Time was {Fore.BLUE}{total_travel_time}{Style.RESET_ALL} seconds. That comes to {convert_seconds_to_string(total_travel_time)}.")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(
        f"Each trip took an average of {Fore.BLUE}{average_travel_time}{Style.RESET_ALL} seconds. That comes to {convert_seconds_to_string(average_travel_time)}.")

    print(f"\n{Fore.YELLOW}This took %s seconds.{Style.RESET_ALL}" % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print(f"Subscribers: -> {user_count[0]}")
    print(f"Customers: -> {user_count[1]}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df.Gender.value_counts()
        print(f"Male: {gender_count[0]}")
        print(f"Female: {gender_count[1]}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        print(
            f"The earliest birth year was {Fore.BLUE}{earliest}{Style.RESET_ALL}, about {now.year - earliest} yrs old.")
        youngest = int(df['Birth Year'].max())
        print(
            f"The youngest birth year was {Fore.BLUE}{youngest}{Style.RESET_ALL}, about {now.year - youngest} yrs old.")
        common = int(df['Birth Year'].mode()[0])
        print(
            f"The most common birth year was {Fore.BLUE}{common}{Style.RESET_ALL}, about {now.year - common} yrs old.")

    print(f"\n{Fore.YELLOW}This took %s seconds.{Style.RESET_ALL}" % (time.time() - start_time))
    print('-' * 40)


def receive_yes_no(question_string):
    restart = input(f'\n{question_string} (yes or no)\n-> ')
    while restart not in ('yes', 'no'):
        restart = input(error_prompt)
    return restart


def main():
    while True:
        city, month, day = get_filter_pref()
        df = load_data(city, month, day)
        print()
        print('-' * 40)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_raw = receive_yes_no(raw_prompt)
        starting_index = 0
        ending_index = 4
        while see_raw != "no":
            print()
            while starting_index < ending_index:
                print("-" * 40)
                print(df.iloc[starting_index])
                starting_index += 1
            ending_index += 5
            see_raw = receive_yes_no(raw_prompt)

        restart = receive_yes_no("Would you like to start over?")
        if restart == "no":
            break

        print()


if __name__ == "__main__":
    main()
