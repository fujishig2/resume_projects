import sqlite3
from hashlib import pbkdf2_hmac
import time
import binascii
import account_managers2
import drivers2
import supervisor2
import dispatcher2

connection = None
cursor = None


def connect(path):
	# Connects the waste_management.db
	global connection, cursor
	connection=sqlite3.connect(path)
	connection.row_factory = sqlite3.Row
	cursor=connection.cursor()
	cursor.execute('PRAGMA foreign_keys=ON; ')
	return



def hash_password(password):
	# Returns a hashed password
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000
	dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
	return dk



def login():
	# Main login screen. Asks for username and password, and if user enters valid account in 'users', signs into the correct role page
	attempt=0
	print("\n-------------------")
	print("Login Page")
	while attempt<=2:
		user_login = input("Enter username (q = quit): \n==>")
		if user_login == 'q': return
		user_password = input("Enter password (q = quit): \n==>")
		if user_password == 'q': return
		login_command = '''SELECT * FROM users WHERE password=? AND login=?'''

		cursor.execute(login_command, (bytes(hash_password(user_password)), user_login))
		results = cursor.fetchone()

		if results == None:
			if attempt == 2:
				print("\nNo more attempts remaining, returning to home page\n")
			else:
				print("\nUsername and/or password are incorrect, " + str(2 - attempt) + " attempts remaining\n")

		else:
			if results[1] == "driver":
				DriverClass=drivers2.Driver("./waste_management.db", connection, cursor)
				DriverClass.driver_interface(results)
			elif results[1] == "supervisor":
				SupervisorClass=supervisor2.Supervisor("./waste_management.db", connection, cursor)
				SupervisorClass.supervisor_interface(results)
			elif results[1] == "account manager":
				AccountManager=account_managers2.AccountManager("./waste_management.db", connection, cursor)
				AccountManager.accountmanager_interface(results[0])
			elif results[1] == "dispatcher":
				DispatcherClass=dispatcher2.Dispatcher("./waste_management.db", connection, cursor)
				DispatcherClass.dispatcher_interface(results)

			break
		attempt+=1

def add_user():
	# Adds a user to table
	global connection, cursor
	user_login=input("Enter user login: ")
	user_role=input("Enter role: ")
	user_password=input("Enter password: ")

	cursor.execute('''
			SELECT pid FROM personnel
			EXCEPT
			SELECT user_id FROM users
		''')
	row = cursor.fetchall()
	print("Select one of the available PIDs below")
	available_pids = []
	if row != None:
		for element in row:
			for value in element:
				available_pids.append(value)
				print(" " + value)
	print("Enter PID: ")
	user_id = ""
	while True:
		user_id = input("==>")
		if user_id not in available_pids:
			print("Please select a valid PID")
		else:
			break

	insert_enroll = "INSERT INTO users(user_id, role, login, password) VALUES (:user_id, :user_role, :user_login, :user_password);"
	cursor.execute(insert_enroll, {"user_id": user_id, "user_role": user_role, "user_login": user_login, "user_password" :hash_password(user_password)})
	connection.commit()

def getusertable():
	# For testing purposes, gets the users table
	global connection, cursor
	cursor.execute("SELECT * FROM users")
	row = cursor.fetchall()

	if row != None:
		for element in row:
			for value in element:
				print(value, end=', ')
			print('')



def main():
	global connection, cursor
	path = "./waste_management.db"
	connect(path)

	while True:
		print("--------------------------------------")
		print("Welcome to waste management database! ")
		print("Options: ")
		print(" 1 - Login")
		print(" 2 - Create new user")
		print(" 3 - get user table (for testing)")
		print(" q - Exit program")

		user_input = input("==>")
		if user_input == '1':
			login()
		elif user_input == '2':
			add_user()
		elif user_input == '3':
			getusertable()
		elif user_input == 'q':
			print("Goodbye!")
			return
		else:
			print("Invalid option!")

if __name__ == "__main__":
	main()