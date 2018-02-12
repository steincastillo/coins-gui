
# coins-gui
Coin collection manager with a GUI interface

This documentation is still work in progress... check back soon for an updated version.
in the meanwhile...

## What does it do?
This repository contains a very simple coin collection manager that will help you to keep track of the coins in your collection.
It is designed to be a learning excercise to create a **G**raphical **U**ser **I**nterface (GUI) while also exploring the database and file management capabilities of python.

The application is intended to run on a raspberry pi but it should be portable to other python platforms as it relies solely on standard python libraries:
* Tkinter
* Sqlite
* Pandas

## How to use it?
The application is ready to go! Just clone this repository, launch the python IDLE, open the file ```coins_gui.py``` and execute it. That's it.
A sample database (```coins.db```) and the list of countries (```countries.csv```) with all the infomation you need has been provided.

## What are the interesting highlights?
The application uses **tkinter** to create the GUI, this includes graphical widgets such as:
* Frames
* Buttons
* Scrollbars
* Combobox
* Label frames
* Labels
* Input fields
* Menus
* Messageboxes

The application uses **SQLITE** to handle the coins database. The information stored in database is:
* Code: Automatically handled
* Country: Where the coin is from
* Value: Coin value
* Year: When the coin was minted
* Age: (Calculated) How old is the coin

The application uses **PANDAS** to create a dataframe from a CSV file with the countries list (used in a combobox)

## Any extras?
Glad you ask! yes! there is an extra program: ```coins.py``` which is a text-based version of the coin manager. it has an interesting extra feature: **COIN MAP** that will create an interactive map with markers on the countries where you have coins from.
There is a little catch: for this feature to work you will need to install ```folium``` it is a very simple process and you can find the installation process in the www.raspberrypi.org page.
