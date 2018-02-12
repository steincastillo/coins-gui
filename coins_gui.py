#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import sqlite3
import pandas as pd
import numpy as np
import os.path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.font as tkFont

# Define classes
class App(object):
    """ Use a ttk.Treeview to display the content of the database """

    def __init__(self, master):
        self.root = master
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        """ Create the main windows and the tree """

        # Define windows menu
        self.menubar = Menu(self.root)
        self.menubar.add_command(label='Info',
                                 underline=0,
                                 command=self._info)
        self.menubar.add_command(label='Close',
                                 underline=0,
                                 command=self._close)

        # Define the widgets
        content = ttk.Frame(self.root, padding=(3,3,12,12))

        container = ttk.Frame(content, borderwidth=5,
                              relief='sunken')

        self.tree = ttk.Treeview(container, columns=db_header,
                                 selectmode='browse', show='headings')

        self.vsb = ttk.Scrollbar(container, orient=VERTICAL,
                            command=self.tree.yview)

        self.hsb = ttk.Scrollbar(container, orient=HORIZONTAL,
                            command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.vsb.set,
                            xscrollcommand=self.hsb.set)

        self.close = ttk.Button(content, text='Close',
                                command=self._close)

        self.lf1 =ttk.Labelframe(content, text='Details',
                                 width=300, height=200)

        # Define label frame elements (lf1)
        self.l1 = ttk.Label(self.lf1, text='Code')
        self.l2 = ttk.Label(self.lf1, text='Country')
        self.l3 = ttk.Label(self.lf1, text='Value')
        self.l4 = ttk.Label(self.lf1, text='Year')
        self.l5 = ttk.Label(self.lf1, text='Age')
        self.l6 = ttk.Label(self.lf1, text='Currency')

        # Define variables for label frame (lf1)
        self.d1 = StringVar() # Code
        self.d2 = StringVar() # Country
        self.d3 = StringVar() # Value
        self.d4 = StringVar() # Year
        self.d5 = StringVar() # Age
        self.d6 = StringVar() # Currency

        # Define entry fields for label frame (lf1)
        self.e1 = ttk.Entry(self.lf1, textvariable=self.d1) # Code
        self.e2 = ttk.Entry(self.lf1, textvariable=self.d2) # Country
        self.e3 = ttk.Entry(self.lf1, textvariable=self.d3) # Value
        self.e4 = ttk.Entry(self.lf1, textvariable=self.d4) # Year
        self.e5 = ttk.Entry(self.lf1, textvariable=self.d5) # Age
        self.e6 = ttk.Entry(self.lf1, textvariable=self.d6) # Currency

        # Define label frame buttons (lf1)
        self.lfb1 = ttk.Button(self.lf1, text='Add',
                               command=self.newcoin)
        self.lfb2 = ttk.Button(self.lf1, text='Delete',
                               command=self._deleterecord)
        
        # Grid the widgets
        content.grid(column=0, row=0, sticky=(N,S,E,W))
        
        container.grid(column=0, row=0,
                       columnspan=3, rowspan=3,
                       sticky=(N,S,E,W))
        
        self.tree.grid(column=0, row=0,
                       columnspan=3, rowspan=3)
        
        self.vsb.grid(column=3, row=0, sticky='ns', rowspan=3)
        self.hsb.grid(column=0, row=3, sticky='ew', columnspan=3)

        self.lf1.grid(column=4, row=0, padx=5)
        
        self.close.grid(column=4, row=4, sticky='ew', pady=5)

        # Grid label frame elements
        self.l1.grid(column=0, row=0, sticky=(N,W), padx=5)
        self.l2.grid(column=0, row=1, sticky=(N,W), padx=5)
        self.l3.grid(column=0, row=2, sticky=(N,W), padx=5)
        self.l4.grid(column=0, row=3, sticky=(N,W), padx=5)
        self.l5.grid(column=0, row=4, sticky=(N,W), padx=5)
        self.l6.grid(column=0, row=5, sticky=(N,W), padx=5)

        self.e1.grid(column=1, row=0, sticky=(N,E,W), padx=5)
        self.e2.grid(column=1, row=1, sticky=(N,E,W), padx=5)
        self.e3.grid(column=1, row=2, sticky=(N,E,W), padx=5)
        self.e4.grid(column=1, row=3, sticky=(N,E,W), padx=5)
        self.e5.grid(column=1, row=4, sticky=(N,E,W), padx=5)
        self.e6.grid(column=1, row=5, sticky=(N,E,W), padx=5)

        self.lfb1.grid(column=0, row=6, sticky=(N,W), padx=5, pady=5)
        self.lfb2.grid(column=1, row=6, sticky=(N,E), padx=5, pady=5)
        
        # Configure the main elements
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.ws = int(self.ws/4)
        self.hs = int(self.hs/3)
        self.root.geometry('+'+str(self.ws)+'+'+str(self.hs))
        self.root.config(menu=self.menubar)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title('Coin Collection Viewer')

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

    def _build_tree(self):
        """ Set the tree and display the DB contents """
        
        # Add tree headers
        for col in db_header:
            self.tree.heading(col, text=col.title())
        # Define tree bindings
        self.tree.bind('<Double-Button-1>', self._select)
        self.tree.bind('<Return>', self._select)
        # Set ordering options (country, year and currency)
        self.tree.heading('Country',
                          command=lambda: sortby(self.tree, 'Country', 0))
        self.tree.heading('Year',
                          command=lambda: sortby(self.tree, 'Year', 0))
        self.tree.heading('Currency',
                          command=lambda: sortby(self.tree, 'Currency', 0))
        # Set formating options
        self.tree.column('Code', anchor='center', width=50)
        self.tree.column('Country', width=120)
        self.tree.column('Value', anchor='center', width=100)
        self.tree.column('Year', anchor='center', width=100)
        self.tree.column('Age (years)', anchor='center', width=90)
        self.tree.column('Currency', width=120)
        # Add DB data to the tree
        self.refreshtree()

    def _select(self, event):
        iid = self.tree.focus()
        if iid == '': return
        val = self.tree.item(iid)
        self.d1.set(val['values'][0])
        self.d2.set(val['values'][1])
        self.d3.set(val['values'][2])
        self.d4.set(val['values'][3])
        self.d5.set(val['values'][4])
        self.d6.set(val['values'][5])

    def refreshtree(self):
        """ Refresh the contents of the tree view """

        # Delete current content
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Add DB data to the tree
        self.df = pd.read_sql_query('SELECT * FROM v_full;', conn)
        # Convert dataframe to a numpy array
        self.ds = self.df.values
        # Add data to the treeview
        for item in self.ds:
            self.tree.insert('', 'end',
                             values=(item[0], item[1], item[2],
                                     item[3], item[4], item[5]))
        

    def _info(self):
        msg = 'Coin Collection Viewer V1.5'
        dtl = 'Copyright 2018 Stein Castillo'
        messagebox.showinfo(title='Info', message=msg, detail=dtl)
        
    def _close(self):
        """ Close the DB and terminate the application """
        
        dbClose(conn)
        self.root.destroy()

    def _deleterecord(self):
        """ Delete selected record from the DB """
        
        iid = self.tree.focus()
        if iid == '': return
        
        if messagebox.askyesno('Delete', 'Delete coin from collection?'):
            val = self.tree.item(iid)
            self.code = (val['values'][0])
            cursor.execute('''DELETE FROM coins WHERE id=?''', (self.code,))
            conn.commit()
            self.d1.set('')
            self.d2.set('')
            self.d3.set('')
            self.d4.set('')
            self.d5.set('')
            self.d6.set('')
            self.refreshtree()

    def newcoin(self):
        self.newWindow = Toplevel(self.root)
        self.app = Newcoin(self.newWindow)
        

class Newcoin():
    """ Open a new window to capture new coin data """
    
    def __init__(self, master):
        self.master = master
        self._setupwidgets()

    def _setupwidgets(self):
        """ Setup widgets for the new coin entry window """
        
        self.frame = ttk.Frame(self.master)
        self.f1 = ttk.Frame(self.frame, padding=(3,3,12,12))
        
        self.confirmButton = ttk.Button(self.f1, text='Add',
                                        command=self.get_data)
        self.quitButton = ttk.Button(self.f1, text='Quit',
                                     command=self.close_window)

        # Define frame elements (f1)
        self.l1 = ttk.Label(self.f1, text='Country')
        self.l2 = ttk.Label(self.f1, text='Value')
        self.l3 = ttk.Label(self.f1, text='Year')

        # Define variables for frame (f1)
        self.d1 = StringVar() # Country
        self.d2 = StringVar() # Value
        self.d3 = StringVar() # Year

        # Initialize variables
        self.d2.set('0')    # Value
        self.d3.set('0')    # Year

        # Define entry fields for frame (f1)
        self.e1 = ttk.Combobox(self.f1, textvariable=self.d1,
                               values=clist, state='readonly') # Country
        self.e1.current(0)
        self.e2 = ttk.Entry(self.f1, textvariable=self.d2) # Value
        self.e3 = ttk.Entry(self.f1, textvariable=self.d3) # Year

        # Grid label frame elements
        self.frame.grid(column=0, row=0, sticky=(S,N,E,W))
        self.f1.grid(column=0, row=0, sticky=(S,N,E,W))
        
        self.l1.grid(column=0, row=0, sticky=(N,W), padx=5)
        self.l2.grid(column=0, row=1, sticky=(N,W), padx=5)
        self.l3.grid(column=0, row=2, sticky=(N,W), padx=5)

        self.e1.grid(column=1, row=0, sticky=(N,E,W), padx=5)
        self.e2.grid(column=1, row=1, sticky=(N,E,W), padx=5)
        self.e3.grid(column=1, row=2, sticky=(N,E,W), padx=5)
        
        # Grid the frame buttons
        self.confirmButton.grid(column=0, row=3, sticky=(N,W), padx=5, pady=5)
        self.quitButton.grid(column=1, row=3, sticky=(N,E), padx=5, pady=5)

        # Configure the elements
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.f1.columnconfigure(0, weight=1)
        self.f1.columnconfigure(1, weight=1)


    def close_window(self):
        self.master.destroy()

    def get_data(self):
        """ Collect, validate and add data to the DB """
        
        self.validyear = False
        self.validvalue = False
        self.validcountry = False
        
        # Validate value
        self.value = self.d2.get()
        if self.value.replace('.','').isdigit():
            self.value = float(self.value)
            if self.value > 0:
                self.validvalue = True
            
        # Validate year
        self.year=self.d3.get()
        if self.year.isdigit():
            self.year = int(self.year)
            if self.year > 0:
                self.validyear = True
        
        # Validate country
        self.country= self.d1.get()
        cursor.execute('SELECT * FROM country WHERE nicename=:id',
                       {'id':self.country})
        self.id_exists = cursor.fetchone()
        if self.id_exists:
            self.country = self.id_exists[1]
            self.validcountry = True

        # If data is valid, add to the DB
        if self.validyear and self.validvalue and self.validcountry:
            self.row = (self.country, self.value, self.year)
            self.sql = '''INSERT INTO coins (country, value, year) VALUES (?, ?, ?)'''
            cursor.execute(self.sql, self.row)
            conn.commit()
            messagebox.showinfo('Info', 'Coin added to collection!')
            # Refresh the treeview
            coins.refreshtree()
            # Clear the entry variables
            self.d2.set('0')
            self.d3.set('0')
        else:
            messagebox.showerror('Error', 'Invalid Data... Please verify')
        

# Define functions
def sortby(tree, col, descending):
    """ Sort tree contents when a column heade is clicken on """
    
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
            tree.move(item[1],'', ix)
    # Switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
                                                     int (not descending)))
            
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

if __name__=='__main__':
    # Setup DB access
    conn, cursor = dbConnect('coins.db')

    # Set dynamic table headers
    data = cursor.execute('select * from v_full')
    db_header = list(map(lambda x:x[0], data.description))
    db_header = [x.capitalize() for x in db_header]

    # Create the countries list
    countries = pd.read_sql_query('SELECT * FROM country;', conn)
    clist1 = countries['nicename'].values
    clist = []
    clist = [item for item in clist1]

    # Initiate the GUI
    root = Tk()
    coins = App(root)
        
