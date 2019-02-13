import sqlite3
import re


class Supervisor():
	global connection, cursor
	
	#initialize the class, also connect it to the database.
	def __init__(self, path, connection, cursor):
		connection=sqlite3.connect(path)
		cursor = connection.cursor()
		cursor.execute('PRAGMA foreign_keys=ON;')
		connection.commit()
		self.connection=connection
		self.cursor=cursor


	def supervisor_interface(self, user_info):
		#main method that will be able to run the interface. It will
		#direct the flow of the program to different places depending
		#on user inputs.
		
		#saves all the account managers under the supervisor into an array
		self.cursor.execute('''
			SELECT c.pid, a.name
			FROM personnel a, account_managers c
			WHERE c.pid = a.pid
			AND a.supervisor_pid = ?''', (user_info[0],))
		rows = self.cursor.fetchall()
		man_pids = []
		for row in rows:
			man_pids.append(str(row[0]))

		while True:
			print("\n------------------------------------")
			print(user_info[2]+" (Supervisor)")
			print("\n1 - Create new account")
			print("2 - Customer summary report")
			print("3 - Account manager summary report")
			print("q - Logout")
			option = input("==>")

			if option == '1':
				temp = 's'
				while temp != 'q':
					temp = self.create_acc(user_info, man_pids)
			elif option == '2':
				temp = 's'
				while temp != 'q':
					temp = self.cust_sum(user_info, man_pids)


			elif option == '3':
				self.man_sum(user_info)

			elif option == 'q':
				return
			else:
				print("Invalid option!")

	def create_acc(self, user_info, man_pids):
		#create a customer account for a specific manager
		#under the supervisor.
		
		self.cursor.execute('''
					SELECT account_no
					FROM accounts''')
		rows = self.cursor.fetchall()

		temp = []
		#save all the accounts in a temporary file, that way we know
		#there won't be any duplicates.
		for row in rows:
			temp.append(row[0])
		#infinite loop error checking duplicate account numbers
		while True:
			acc_no = input("Account number (q = quit): \n==>")
			if acc_no == 'q':
				return 'q'
			if acc_no not in temp:
				break
			print("Invalid account number. Duplicate found!")

		#display all the available manager ids
		print("All manager IDs: ")
		if man_pids == []:
			print("No managers found")
		for man_id in man_pids:
			print(man_id)
			
		#error check if the account manager is under the supervisor
		while True:
			man_pid = input("Account manager(q = quit): \n==>")
			if man_pid == 'q':
				return 'q'
			if man_pid in man_pids:
				break
			print("Invalid account manager!")

		cust_name = input("Customer name(q = quit): \n==>")
		if cust_name == 'q': return 'q'
		contact_info = input("Contact info(q = quit): \n==>")
		if contact_info == 'q': return 'q'
		cust_type = input("Customer type(q = quit): \n==>")
		if contact_info == 'q': return 'q'

		#error checks date format
		pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
		while True:
			start = input("Starting date in format 'YYYY-MM-DD'(q = quit): \n==>")
			if start == 'q': return
			if re.match(pattern,start):
				break
			else:
				print("***Invalid date format.***")

		while True:
			end = input("Ending date in format 'YYYY-MM-DD'(q = quit): \n==>")
			if end == 'q': return 'q'
			if re.match(pattern,end):
				break
			else:
				print("***Invalid date format.***")

				
		self.cursor.execute('''
		INSERT INTO accounts VALUES(?,?,?,?,?,?,?,0);''', (acc_no, man_pid, cust_name, contact_info, cust_type, start, end))
		print("\nAccount created!")


	def cust_sum(self, user_info, man_pids):
		#Make up a customer summary which contains the number of
		#number of service agreements, the sum of prices, sum of
		#internal prices, and the account manager name
		
		#query all the customers that the supervisor has access to
		self.cursor.execute('''
		SELECT c.account_no
		FROM accounts c, personnel p
		WHERE p.pid = c.account_mgr
		AND p.supervisor_pid = ?''', (user_info[0],))
		rows = self.cursor.fetchall()
		temp = []
		for row in rows:
			temp.append(row[0])
		print("\nAll available customer account numbers: ")
		if temp == []:
			print("No customers found!")
		for num in temp:
			print(num)
		while True:
			cust = input("Enter customer account number (q = quit): \n==>")
			if cust == 'q':
				return 'q'
			if cust in temp:
				break
			print("Customer not found in any account managers accounts!")
		
		#query a customer report
		self.cursor.execute('''
		SELECT COUNT(d.service_no), SUM(d.price),  SUM(d.internal_cost), p.name
		FROM service_agreements d, accounts c, personnel p
		WHERE c.account_no = ?
		AND c.account_no = d.master_account
		AND p.pid = c.account_mgr;''', (cust,))
		rows = self.cursor.fetchall()
		for row in rows:
			print("summary report")
			print("--------------")
			print("Total number of service agreements:\t", row[0])
			print("Sum of prices:			  \t$%.2f" %row[1])
			print("Sum of internal cost:		  \t$%.2f" %row[2])
			print("Manager name:                      \t", row[3])


	def man_sum(self, user_info):
		#display all the account managers who are under the supervisors
		#summary reports. These reports contain the account managers name,
		#the number of master accounts, number of service accounts, sum of
		#the prices, and sum of internal costs.
		
		print("Manager summary report:")
		#sql query for the manager summary reports:
		self.cursor.execute('''
		SELECT p.name, COUNT(d.master_account), COUNT(d.service_no), SUM(d.price), SUM(d.internal_cost)
		FROM personnel p, accounts a, service_agreements d
		WHERE p.pid = a.account_mgr
		AND a.account_no = d.master_account
		AND p.supervisor_pid = ?
		GROUP BY p.name
		ORDER BY (SUM(d.price) - SUM(d.internal_cost));''', (user_info[0],))
		
		rows = self.cursor.fetchall()
		print("Manager\t\tMaster agreements\tService agreements\tSum of prices\tSum of internal")
		print("-------\t\t-----------------\t------------------\t-------------\t---------------")
		for row in rows:
			print(str(row[0]) + "\t" + str(row[1]) + "\t\t\t" + str(row[2]) + "\t\t\t$%.2f"%row[3] + "\t\t$%.2f"%row[4])
		