# Main module which should be called directly
# Creates objects from the drivers, supervisor, dispatcher, and account_managers class files, and
# executes the corresponding code in these classes depending on the input provided by the user

import sqlite3
import os.path
import re
import bcnf_normalization
import equivalence
import attributeClosure

connection = None
cursor = None


# Connects to the waste_management.db file
# Initialized global connection and cursor variables
# Called once at the start of 'main' function
def connect(path):
	global connection, cursor
	connection=sqlite3.connect(path)
	connection.row_factory = sqlite3.Row
	cursor=connection.cursor()
	cursor.execute('PRAGMA foreign_keys=ON; ')
	return


def enter_filename():
	print("Enter database filename:")
	while True:
		database_path=input("==>")
		if os.path.isfile(database_path):
			return database_path
		else:
			print("File does not exist, re-enter filename")


def get_sorted_attributes(attributes, element):
	print("> attributes: ",attributes)
	print("> element: ",element)
	sorted_element=[]
	for value in attributes:
		if value in element:
			sorted_element.append(value)
	return sorted_element


# The main function first initializes the connection to the database (connect function)
# It then prompts the user for command line options:
# - '1' takes user to log in screen
# - '2' gives user the option to create a new user
# - 'q' quits the program
# This module is the main module, and so this function is the one that is executed first
def main():
	global connection, cursor
	db_path=enter_filename()
	connect(db_path)

	while True:
		print("--------------------------------------")
		print("Welcome to mini project part 2! ")
		print("Options: ")
		print(" 1 - BCNF normalization")
		print(" 2 - Attribute closures")
		print(" 3 - Equivalence of 2 sets of FDs")
		print(" q - Exit program")

		user_input = input("==>")
		if user_input == '1':
			bcnf_normalization.bcnf_main(cursor, connection)
		elif user_input == '2':
			# Attribute closure module call here
			attributeClosure.attributeClosureInterface(connection, cursor)
		elif user_input == '3':
			# Equivalence module call here
			equivalence.setup_eq(connection, cursor)
		elif user_input == 'q':
			print("Goodbye!")
			return
		else:
			print("Invalid option!")

if __name__ == "__main__":
	main()
