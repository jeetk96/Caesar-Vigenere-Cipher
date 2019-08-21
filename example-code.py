#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sqlite3
import sys

from sqlite3 import OperationalError

con = None

try:
    con = sqlite3.connect('fake_umbc.db')
    cur = con.cursor()

    # Open and read the file as a single buffer
    file_descriptor = open('fake_umbc.sql', 'r')
    sql_file = file_descriptor.read()
    file_descriptor.close()

    # Execute the commands in the file to create the database
    sql_commands = sql_file.split(';')

    print "there are " + str(len(sql_commands)) + " commands"

    for command in sql_commands:
        try:
            print "executing: " + command
            cur.execute(command)
        except OperationalError, msg:
            print "Command skipped: ", msg

    print "Done!"

    # Execute an SQL query and get all the results
    result = cur.execute("SELECT first_name, last_name FROM fake_umbc;")
    rows = result.fetchall()

    # Print header information from the result description
    for desc in result.description:
        print desc[0].ljust(20, ' '),

    # Print actual data demonstrating that we've added it to the database
    print ""
    for row in rows:
        for value in row:
            print str(value).ljust(20, ' '),
        print ""

    cur.close()
    con.close()

except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if con:
        con.close()
