# This module implements the interface for account managers, the only function
# should be called is accountmanager_interface(user_id)
import sqlite3
import re


class AccountManager():
	global connection, cursor

	def __init__(self, path, connection, cursor):
		# connect to database
		connection = sqlite3.connect(path)
		cursor = connection.cursor()
		cursor.execute('PRAGMA foreign_keys=ON;')
		connection.commit()
		self.connection=connection
		self.cursor=cursor
		return


	def accountmanager_interface(self, user_id):
	# INPUT: user_id of a VERIFIED account manager (the user is actually an
	# account manager).
	# This is the interface all account managers will be interacting with,
	# Information of an account is only displayed if the account manager logged
	# in is indeed the manager of the said account.
	# This interface includes 4 functionalities for an account manager as seen below

		# connect to databath at path

		while True:
			# get option
			option = input("""Enter the number of option to be selected:
			1 - list all information of an account
			2 - create a new account
			3 - add a new service agreeement to an account
			4 - Show summary report of an account
			q - go back to previous menu\n==>""").strip()

			if option == "1":
				self._list_info(user_id)
			elif option == "2":
				self._create_account(user_id)
			elif option == "3":
				self._add_service(user_id)
			elif option == "4":
				self._report_summary(user_id)
			elif option.lower() == "q":
				break
			else:
				print("Invalid option, enter a number between 1-5")
				continue

		return


	# Select a customer (master account), and then list all the information
	# associated with this customer, followed by the list of all the individual
	# service agreements under for this customer, ordered by service_no. An account
	# manager should only be able to access the accounts that he or she manages.
	def _list_info(self,user_id):

		while True:
			# prompt user
			account_no = input("Enter account_no or l to list all accounts " \
				+ "or q to go back to previous menu:\n==>").lower().strip()
			if account_no.lower() == 'q':
				break

			# run query for this account_mgr
			query = "SELECT account_no, customer_name FROM accounts WHERE account_mgr=?;"
			self.cursor.execute(query,(user_id,))
			rows = self.cursor.fetchall()
			permitted_accounts = []		# accounts this manager is permitted to see
			for row in rows:
				permitted_accounts.append(row[0])


			# list all accounts under this manager
			if account_no == 'l':
				print()
				print("account_no\tcustomer_name")
				print("----------\t-------------")
				for row in rows:
					print(str(row[0]) + "\t" + str(row[1]))
				continue

			# cast account_no & check existence\permission for entered account_no
			if account_no not in permitted_accounts:
				print("***account_no entered does not exist, or you do not have "\
					+ "permission to view this account.***")
				continue

			# show account info
			query = "SELECT * FROM accounts WHERE account_mgr=? AND account_no=?"
			self.cursor.execute(query,(user_id,account_no))
			row = self.cursor.fetchone()
			print()
			print("account_no: \t",		row[0])		# account_no        TEXT,
			print("account_mgr: \t", 	row[1])		# account_mgr       TEXT,
			print("customer_name: \t", 	row[2])		# customer_name     TEXT,
			print("contact_info: \t", 	row[3])		# contact_info      TEXT,
			print("customer_type: \t", 	row[4])		# customer_type     TEXT,
			print("start_date: \t", 	row[5])		# start_date        DATE,
			print("end_date: \t", 		row[6])		# end_date          DATE,
			print("total_amount: \t", 	row[7])		# total_amount      REAL,
			print()

			# list service agreements
			query = "SELECT * FROM service_agreements WHERE master_account=? ORDER BY\
			service_no"
			self.cursor.execute(query,(account_no,))
			rows = self.cursor.fetchall()
			if len(rows) == 0:
				print("***There is currently no service_agreements for this account.***")
			else:
				print("service_agreements")
				print("------------------")
				for row in rows:
					print("service_no:	\t",		row[0])	# service_no        TEXT,
					print("master_account:	\t",	row[1])	# master_account    TEXT,
					print("location:	\t",		row[2])	# location          TEXT,
					print("waste_type:	\t",		row[3])	# waste_type        TEXT,
					print("pick_up_schedule:\t",	row[4])	# pick_up_schedule  TEXT,
					print("local_contact:	\t",	row[5])	# local_contact     TEXT,
					print("internal_cost:	\t",	row[6])	# internal_cost     REAL,
					print("price:		\t",		row[7])	# price             REAL,
					print()
		return


	def _create_account(self,user_id):
		# Create a new master account with all the required information. The manager of
		# the account should be automatically set to the id of the account manager who
		# is creating the account.


		while True:
			print("\nFill in the required information for the account to be added as prompted.")
			# get account_no
			account_no = input("Enter account_no or q to go back to previous menu:\
				\n==>").strip()
			if account_no.lower() == 'q':
				break

			# check if account_no exists
			self.cursor.execute("SELECT account_no FROM accounts;")
			existing_accounts = []
			exist = False
			for row in self.cursor.fetchall():
				if account_no == row[0]:
					exist = True
					break
			if exist:
				print("***account_no already exists.***")
				continue
			else:

				account_mgr = user_id
				customer_name = input("Enter customer_name:\n==>").strip()
				contact_info = input("Enter contact_info:\n==>").strip()

				while True:
					# "municipal", "commercial", "industrial", or "residential"
					customer_type = input("""Select one of the following customer types:
			1 - municipal
			2 - commercial
			3 - industrial
			4 - residential\n==>""").strip()
					if customer_type == "1":
						customer_type = "municipal"
						break
					elif customer_type == "2":
						customer_type = "commercial"
						break
					elif customer_type == "3":
						customer_type = "industrial"
						break
					elif customer_type == "4":
						customer_type = "residential"
						break
					else:
						print("***Invalid option, enter the number of option to be selected.***")
						continue

				# date format: ISO8601 "YYYY-MM-DD HH:MM:SS.SSS"
				pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
				while True:
					start_date = input("Enter start_date(YYYY-MM-DD):\n==>").strip()
					if re.match(pattern,start_date):
						break
					else:
						print("***Invalid date format.***")
				while True:
					end_date = input("Enter end_date(YYYY-MM-DD):\n==>").strip()
					if re.match(pattern, end_date):
						break
					else:
						print("***Invalid date format.***")

				start_date = start_date + " 00:00:00.000"
				end_date = end_date + " 00:00:00.000"
				total_amount = 0 	# new account total inititlized to 0

				# insert value
				values = (account_no,
					account_mgr,
					customer_name,
					contact_info,
					customer_type,
					start_date,
					end_date,
					total_amount)
				cmd = "INSERT INTO accounts VALUES(?,?,?,?,?,?,?,?);"
				self.cursor.execute(cmd,values)
				self.connection.commit()
				print("Account successfully added",end="\n\n")

		return


	def _add_service(self,user_id):
		# For a given customer, add a new service agreement with all the required
		# information -except for the master account number, and the service_no, which
		# should be automatically filled in by the system; master_account is the number
		# of the selected customer, and the service_no is a running numbers, so the
		# next available number should be filled in. If a new service agreement is
		# added, the total amount for the customer should be updated as well. For
		# simplicity, you can add the price for the added service agreement to the total
		# amount in the accounts table.

		print("Fill in the information for the service to be added as prompted.")

		while True:
			# ask for account_no (master account)
			account_no = input("Enter account_no or q to go back to previous menu:\
				\n==>").strip()
			if account_no.lower() == 'q':
				break

			# check account existence/permission
			query = "SELECT account_no FROM accounts WHERE account_mgr=?;"
			self.cursor.execute(query,(user_id,))
			permitted_accounts = []		# accounts this manager is permitted to see
			for row in self.cursor.fetchall():
				permitted_accounts.append(row[0])
			if account_no not in permitted_accounts:
				print("***account_no entered does not exist, or you do not have "\
					+ "permission to view this account.***")
				continue

			# master_account = account_no
			master_account = account_no

			# location
			location = input("Enter location:\n==>").strip()

			# waste_type
			# "hazardous waste", "plastic", "metal", "paper",
			# "compost", "construction waste", and "mixed waste".
			while True:
				waste_type = input("""Select one of the following waste types:
			1 - hazardous waste
			2 - plastic
			3 - metal
			4 - paper
			5 - compost
			6 - construction waste
			7 - mixed waste\n==>""").strip()
				if waste_type == "1":
					waste_type = "hazardous waste"
					break
				elif waste_type == "2":
					waste_type = "plastic"
					break
				elif waste_type == "3":
					waste_type = "metal"
					break
				elif waste_type == "4":
					waste_type = "paper"
					break
				elif waste_type == "5":
					waste_type = "compost"
					break
				elif waste_type == "6":
					waste_type = "construction waste"
					break
				elif waste_type == "7":
					waste_type = "mixed waste"
					break
				else:
					print("***Invalid option, enter the number of option to be selected.***")
					continue

			# pick_up_schedule
			pick_up_schedule = input("Enter pick_up_schedule:\n==>").strip()

			# local_contact
			local_contact = input("Enter local_contact:\n==>").strip()

			# internal_cost
			while True:
				internal_cost = input("Enter internal_cost:\n==>").strip()
				try:
					internal_cost = float(internal_cost)
					break
				except ValueError:
					print("***Internal_cost must be a number***")
					continue

			# price
			while True:
				price = input("Enter price:\n==>").strip()
				try:
					price = float(price)
					break
				except ValueError:
					print("***Price must be a number.***")
					continue

			# generate service_no
			cmd = "SELECT service_no FROM service_agreements WHERE master_account=?;"
			self.cursor.execute(cmd,(account_no,))
			existing_nums = []
			for row in self.cursor.fetchall():
				existing_nums.append(int(row[0]))
			service_no = 1
			while service_no in existing_nums:
				service_no += 1
			service_no = str(service_no)

			# insert new entry
			cmd = "INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?);"
			values = (service_no, master_account, location, waste_type, \
				pick_up_schedule, local_contact, internal_cost, price)
			self.cursor.execute(cmd, values)

			# update total amount
			cmd = "SELECT total_amount FROM accounts WHERE account_no=?;"
			self.cursor.execute(cmd,(master_account,))
			total_amount = self.cursor.fetchone()[0]
			total_amount += price
			cmd = "UPDATE accounts SET total_amount=? WHERE account_no=?;"
			self.cursor.execute(cmd,(total_amount, master_account))
			self.connection.commit()
			print("service successfully added",end="\n\n")

		return


	def _report_summary(self,user_id):
		# Create a summary report for a single customer, listing the total number of
		# service agreements, the sum of the prices and the sum of the internal cost
		# of the service agreements, as well as the number of different waste types
		# that occur in the service agreements.

		while True:
			# ask for account_no
			account_no = input("Enter account_no or q to go back to previous menu:\
				\n==>").strip()
			if account_no.lower() == 'q':
				break

			# check for permission for this manager
			query = "SELECT account_no FROM accounts WHERE account_mgr=?;"
			self.cursor.execute(query,(user_id,))
			rows = self.cursor.fetchall()
			permitted_accounts = []		# accounts this manager is permitted to see
			for row in rows:
				permitted_accounts.append(row[0])

			# check existence\permission for entered account_no
			if account_no not in permitted_accounts:
				print("***account_no entered does not exist, or you do not have "\
					+ "permission to view this account.***")
				continue


			# total number of service agreements
			cmd = """	SELECT COUNT()
						FROM service_agreements
						WHERE master_account=?;"""
			self.cursor.execute(cmd,(account_no,))
			num_services = self.cursor.fetchone()[0]

			# the sum of the prices
			cmd = """	SELECT sum(price)
						FROM service_agreements
						WHERE master_account=?;"""
			self.cursor.execute(cmd,(account_no,))
			sum_price = self.cursor.fetchone()[0]

			# sum of internal cost
			cmd = """	SELECT sum(internal_cost)
						FROM service_agreements
						WHERE master_account=?;"""
			self.cursor.execute(cmd,(account_no,))
			sum_cost = self.cursor.fetchone()[0]

			# the number of different waste types in agreements
			cmd = """	SELECT count(DISTINCT waste_type)
						FROM service_agreements
						WHERE master_account=?;"""
			self.cursor.execute(cmd,(account_no,))
			num_waste_types = self.cursor.fetchone()[0]



			# Create a summary report for a single customer, listing the total number of
			# service agreements, the sum of the prices and the sum of the internal cost of
			# the service agreements, as well as the number of different waste types that
			# occur in the service agreements.
			print("summary report")
			print("--------------")
			print("Total number of service agreements:\t", num_services)
			print("Sum of prices:			\t%.2f" % sum_price)
			print("Sum of internal cost:		\t%.2f" % sum_cost)
			print("Number of different waste types:\t",num_waste_types, end="\n\n")

		return

