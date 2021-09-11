import time
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
    print('Hello! Let\'s explore some US bikeshare data!')

    #casefold because more aggressive than lower()
    city = input("Would you like to see Data for Chicago, New York City or Washington?\n").casefold()
    while city not in ("chicago", "new york city", "washington"):
        try:
            city = input("Would you like to see Data for Chicago, New York City or Washington?\n")
            city = city.casefold()
            #to see what is running
            print("Test for while loop city")
        except ValueError:
            print("Choose one of the following expressions: chicago, new york city or washington")

    month = input("Which month do you want to see?\n").casefold()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        try:
            month = input("Which month do you want to see?\n")
            month = month.casefold()
            print("Test for while loop month")
        except ValueError:
            print("Choose one of the following expressions: All, January, February, March, April, May, June")

    day = input("Which day of the week do you want to see?\n").casefold()
    while day not in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
        try:
            day = input("Which day of the week do you want to see?\n")
            day = day.casefold()
            print("Test for while loop day")
        except ValueError:
            print("Choose one of the following expressions: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")


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
    #reading the csv file with the city name input
    df = pd.read_csv(CITY_DATA[city])

    #converting the Start Time to a known time
    df["Start Time"] = pd.to_datetime(df["Start Time"])


    #defining the month column
    df["month"] = df["Start Time"].dt.month

    # defining the day column
    df["day"] = df["Start Time"].dt.day_name()

    #defining the hour column
    df["hour"] = df["Start Time"].dt.hour

    #new df filter
    if month != "all":
      months = ["january", "february", "march", "april", "may", "june"]
      month = months.index(month) + 1
      df = df[df["month"] == month]

     # filter by day
      if day != "all":
        df = df[df["day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("The most common month is ", df["month"].mode()[0])

    print("\nThe most common day of week is ", df["day"].mode()[0])

    print("\nThe most common hour of start is ", df["hour"].mode()[0], " o'clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most common used Start Station is ", df["Start Station"].mode()[0])

    print("\nThe most common used End Station is ", df["End Station"].mode()[0])

    df["most_combination"] = "\nThe most frequent combination is " + df["Start Station"] + " to " + df["End Station"]
    print(df["most_combination"].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total travel time is ", df["Trip Duration"].sum(), " seconds")
    print("This is a total of approximately ", int(df["Trip Duration"].sum()/3600), " hours")

    print("\nThe mean time of travel is ", df["Trip Duration"].mean(), "seconds")
    print("This is a total of approximately ", round(df["Trip Duration"].mean()/3600, 3), "hours")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("The number of different User Types are\n", df["User Type"].value_counts())

    if "Gender" in df:
        print("\nThe number of different Genders are\n", df["Gender"].value_counts())
    else:
        print("\nThere is no Gender Data in this City!")

    if "Birth Year" in df:
        print("\nThe earliest Year of Birth is ", int(df["Birth Year"].min()))
        print("\nThe most recent Year of Birth is ", int(df["Birth Year"].max()))
        print("\nThe most common Year of Birth is ", int(df["Birth Year"].mode()[0]))
    else:
        print("\nThere are no Data for Birth Year in this City!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #give the user a output of 5 rows when entering yes
        #df has to be defined again
        df = pd.read_csv(CITY_DATA[city])

        user_input = input("Would you like to see 5 rows more of raw Data? Enter yes otherwise no!\n").casefold()
        while user_input not in ("yes", "no"):
            try:
                user_input = input("Would you like to see 5 rows more of raw Data? Enter yes otherwise no!\n")
                user_input = user_input.casefold()
            except ValueError:
                print("Choose one of the following expressions: yes, no\n")

        count_raw_data = 0
        while True:
            if user_input == "yes":
                print(df.iloc[count_raw_data : count_raw_data + 5])
                count_raw_data +=5
                user_input = input("Do you want to go on? ").casefold()
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
