#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*****************************************
Created on Sat Dec 16 18:38:00 2017
Edited  on Thu Jan 04 14:50:00 2018
@author: Stein Castillo

*****************************************
*         Coin Database Manager         *
*                 V1.8                  *
*****************************************

Description:
    Manages a simple coin collection database
    
Requirements:
    coins.db must be in same directory    
    
Usage:
    python coins.py     
*****************************************
"""

# Import libraries
import sqlite3
import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt
import folium
import html
import webbrowser

# Define functions

def menu(title, options):
    """ Displays the option menu and captures user input

    Parameters
    ----------
        str -> menu title
        list -> menu options
    Returns
    ----------
        User selected option
        option : String
    """
    print ('************************************')
    print (title.rjust(36-(len(title)//2), ' ').upper())
    print ('************************************')
    for line in options:
        print (line)
    print ('************************************')
    option = input('Select option: ')
    return (option.upper())

def search(sql, db):
    rows = pd.read_sql_query(sql, db)
    if rows.count()[0]:
        print (rows)
    else:
        print('[MSG] Not found!')

# Database management functions

def dbConnect(sqlite_file):
    """ Make connection to an SQLite database """

    # Validate  DB is available
    if not(os.path.isfile(sqlite_file)):              
        print ("[Error] File {} does not exist. Please verify\n".format(sqlite_file))
        exit(0)
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def dbClose(conn):
    """ Commit changes and close connection to the database """
    
    conn.commit()
    conn.close()

# Main loop

if __name__ == '__main__':
    # Define menu options
    TITLE = 'Coin Manager Menu'
    OPTIONS = ['1. Display DB contents', 
               '2. Enter new record', 
               '3. Delete record',
               '4. DB stats',
               '5. Search country code',
               '6. Free DB search',
               '7. Plot coin map',
               'X. Exit']
    # Print routine header
    print (__doc__)   
    # Setup DB access
    conn, cursor = dbConnect('coins.db')
    
    loop = True
    
    while loop:
        option = menu(TITLE, OPTIONS)

        if option == '1':
            print ('Display DB contents')
            print ('*******************')
            with pd.option_context('display.max_rows', 100):
                print (pd.read_sql_query('SELECT * FROM v_full;', conn))

        elif option == '2':
            print ('Enter new record')
            print ('*******************')
            # Get country value from the user
            country = input('Country: ')
            country = country.upper()
            # Validate country ID
            cursor.execute('SELECT * FROM country WHERE iso=:id', {'id':country})
            id_exists = cursor.fetchone()
            if id_exists:
                # Get the rest of the values from the user
                value = input('Value: ')
                year = input('Year: ')
                value = float(value)
                year = int(year)
                # Insert row into the DB
                row = (country, value, year)
                sql = '''INSERT INTO coins (country, value, year) VALUES (?, ?, ?)'''
                cursor.execute(sql, row)
                conn.commit()
                print ('[MSG] Record added to the database')
            else:
                print ('[ERROR] Country code is invalid, data was not saved!')

        elif option == '3':
            print ('Delete record')
            print ('*******************')
            record = input ('Record CODE to delete: ')
            record = int(record)
            cursor.execute('''SELECT * FROM coins where id=?''', (record,))
            id_exists = cursor.fetchone()
            # Validate the record ID
            if id_exists:
                confirm = input ('Are you sure you want to proceed [Y/N]').upper()
                if confirm == 'Y':
                    cursor.execute('''DELETE FROM coins WHERE id=?''', (record,))
                    conn.commit()
                    print ('[MSG] Record deleted from the database')
            else:
                print ('[ERROR] Record not found!')

        elif option == '4':
            print ('DB stats')
            print ('*******************')
            print ('\n')

            print ('Stats by YEAR:')
            print ('*******************')
            sql = 'SELECT year, count(*) as count \
                   FROM coins GROUP BY year ORDER BY year;'
            data = pd.read_sql_query(sql, conn)
            print (data)
            print ('\n')

            # Draw graph coin count by year
            X = data['year']
            y = data['count']
            plt.scatter(X, y, color='red')
            plt.axis([X[0]-10, (X[len(X)-1]), 0, (max(y)+1)])
            plt.title('Coin distribution by YEAR')
            plt.xlabel('Year')
            plt.ylabel('Count')
            plt.show()

            print ('Stats by DECADE:')
            print ('****************')
            sql = 'SELECT year, count(*) as count \
                   FROM coins GROUP BY year ORDER BY year;'
            data = pd.read_sql_query(sql, conn)
            # Calculate the decade
            data['year'] = (data['year']//10)*10
            # Group the dataframe by decade
            decade = data.groupby('year', as_index=False).count()
            # Rename the dataframe columns
            decade.columns = ['decade', 'count']
            print(decade)
            print('\n')

            # Draw graph coin distribution by decade
            X = decade['decade']
            y = decade['count']
            plt.pie(y, labels=X, autopct='%1.1f%%', shadow=True)
            plt.title('Coin distribution by DECADE')
            plt.show()

            print ('Stats by COUNTRY:')
            print ('*****************')
            sql = 'SELECT name as country, count(*) as count \
                   FROM coins  \
                   INNER JOIN country on country.iso = coins.country \
                   GROUP BY country \
                   ORDER BY count DESC;'
            data = pd.read_sql_query(sql, conn)
            print (data)
            print ('\n')

            # Draw graph coin count by country
            X = data['country']
            y = data['count']
            X1 = np.arange(len(X))
            plt.barh(X1, y, color='blue')
            plt.yticks(X1, X)
            plt.title('Coin distribtuion by COUNTRY')
            plt.xlabel('Count')
            plt.grid()
            plt.show()

            sql = 'SELECT count(*) FROM coins;'
            cursor.execute('''SELECT count(*) from coins;''')
            print ('Total records: {}'.format(cursor.fetchone()[0]))

        elif option == '5':
            print ('Search country code')
            print ('*******************')
            country = input('Country name: ').upper()
            # Search for country name
            sql = 'SELECT name, iso FROM country WHERE name LIKE ' + '\'%'+country+'%\''+';'
            search(sql, conn)

        elif option == '6':
            print ('Free DB search')
            print ('**************')
            value = input('Enter value to search: ')
            print ('Searching countries...')
            value = value.upper()
            sql = 'SELECT * FROM v_full WHERE country like '+'\'%'+value+'%\''+';'
            search(sql, conn)
            print('Searching values...')
            sql = 'SELECT * FROM v_full WHERE value like '+'\'%'+value+'%\''+';'
            search(sql, conn)
            print('Searching years...')
            sql = 'SELECT * FROM v_full WHERE year like '+'\'%'+value+'%\''+';'
            search(sql, conn)
            print('Searching currency...')
            sql = 'SELECT * FROM v_full WHERE currency like '+'\'%'+value+'%\''+';'
            search(sql, conn)
            
        elif option == '7':
            print ('Plot coin MAP')
            print ('**************')
            # Pre-process countries information
            country_df = pd.read_csv('countries.csv')
            # Drop unnecessary features
            country_df = country_df.drop(['tld', 'cca3', 'cioc', 'ccn3',
                                          'callingCode', 'altSpellings',
                                          'languages', 'translations', 'borders',
                                          'demonym', 'landlocked', 'area'], axis=1)
            # Extract country name
            for obs in range(len(country_df.index)):
                country_df['name'][obs] = country_df['name'][obs].split(',')[0]

            # Query the coins database
            sql = 'SELECT country, count(*) as count \
                   FROM coins \
                   GROUP BY country \
                   ORDER BY count DESC'
            list = pd.read_sql_query(sql, conn)

            # Merge dataframes
            plot = pd.merge(country_df, list, how = 'inner',
                            left_on = 'cca2',
                            right_on = 'country')
            
            # Process coordinates
            # Split latlng into two different columns
            plot['latitude'], plot['longitude'] = zip(*plot['latlng'].apply(lambda x: x.split(',', 1)))
            # Convert values to float
            plot.latitude = plot.latitude.astype(float)
            plot.longitude = plot.longitude.astype(float)

            # Alternative method to process the coordinates.
            # This method iterated throught the dataframe
            # plot['latitude'] = 0.0
            # plot['longitude'] = 0.0
            # for obs in range(len(plot.index)):
            #     latitude = float(plot['latlng'][obs].split(',')[0])
            #     plot['latitude'][obs] = latitude
            #     longitude = float(plot['latlng'][obs].split(',')[1])
            #     plot['longitude'][obs] = longitude

            # Map countries and markers
            world_map = folium.Map(location = [0, 0],
                                   tiles = 'Mapbox Bright',
                                   zoom_start = 2)
            coins_group = folium.FeatureGroup('Coins')
            for obs in range(len(plot.index)):
                coins_group.add_child(folium.Marker(location=[plot['latitude'][obs],
                                                              plot['longitude'][obs]],
                                                    popup=plot['name'][obs]))
            world_map.add_child(coins_group)

            world_map.save('coin_map.html')
            webbrowser.open_new('file://coin_map.html')

        elif option == 'X':
            print ('Exit')
            loop = False
        
    # Close the database
    dbClose(conn)
