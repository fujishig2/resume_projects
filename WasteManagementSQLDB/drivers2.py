import sqlite3
import re


class Driver():
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


	def driver_interface(self, user_info):

		#error checks date format
		while True:
			pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
			while True:
				start = input("\nEnter a start date in the form 'YYYY-MM-DD' (q = quit): \n==>")
				if start == 'q': return
				if re.match(pattern,start):
					break
				else:
					print("***Invalid date format.***")
			while True:
				end = input("Enter an end date in the form 'YYYY-MM-DD' (q = quit): \n==>")
				if end == 'q': return
				if re.match(pattern,end):
					break
				else:
					print("***Invalid date format.***")

			print("\n\nTours between " + start + " and " + end + ":\n")

			print("Date and time\t\tLocation\tContact Info\tWaste Type\tDrop Off ID\tPick Up ID")
			print("-------------\t\t--------\t------------\t----------\t-----------\t----------")

			#query all the information needed in 1 statement and order by date.
			self.cursor.execute('''
				SELECT s.date_time, c.location, a.contact_info, e.waste_type, s.cid_drop_off, s.cid_pick_up
				FROM service_fulfillments s, service_agreements c, accounts a, container_waste_types e
				WHERE s.date_time < ? AND s.date_time > ?
				AND s.master_account = c.master_account
				AND e.container_id = s.cid_drop_off
				AND c.master_account = a.account_no
				AND s.driver_id = ?
				GROUP BY s.date_time
				ORDER BY s.date_time;''', (end, start, user_info[0]))

			rows = self.cursor.fetchall()
			for row in rows:
				print(row[0] + "\t" + row[1] + "\t"  + row[2] +  "\t" + row[3] + "\t" + row[4] + "\t\t" + row[5])
			print("\n")
