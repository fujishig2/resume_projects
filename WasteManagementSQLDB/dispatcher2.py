import sqlite3


class Dispatcher():
	global connection, cursor

	def __init__(self, path, connection, cursor):
		# Connects the waste_management.db
		connection=sqlite3.connect(path)
		connection.row_factory = sqlite3.Row
		cursor=connection.cursor()
		cursor.execute('PRAGMA foreign_keys=ON; ')
		connection.commit()
		self.connection=connection
		self.cursor=cursor
		return


	def dispatcher_interface(self, user_info):
		global cursor, connection


		print("\n------------------------------------")
		print(user_info[2]+" (Dispatcher)\n")

		while True:
			go_back=False
			print("Select an option from the list:")
			print("\t1 - Add a new service fulfillment")
			print("\tq - Go back to previous menu")
			while True:
				user_input=input("==>")
				if user_input=='1':
					break
				elif user_input=='q':
					return
			print("\nSelect a service agreement number from the following list:")

			rows=[]
			selected_agreement=[]
			# List service agreements that aren't yet part of service_fulfillments
			self.cursor.execute('''
				SELECT service_no
				FROM service_agreements
				EXCEPT
				SELECT service_no
				FROM service_fulfillments''')
			service_agreements = self.cursor.fetchall()
			for row in service_agreements:
				print(" "+row[0])
			while True:
				service_agreement = input("Enter service agreement number (q = quit): \n==>")
				if service_agreement=='q':
					go_back=True
					break
				valid_service_agreement=False
				for i in service_agreements:
					for j in i:
						if str(service_agreement) == str(j):
							valid_service_agreement = True
				if valid_service_agreement:
					self.cursor.execute('''
						SELECT * FROM service_agreements
						WHERE service_no=?;
					''', (service_agreement, ))
					selected_agreement=[i for i in self.cursor.fetchone()]
					break
				else:
					print("Please enter a valid service agreement")

			if not go_back:
				# List the drivers
				print("\nSelect a driver pid from the following list: \ndriver_pid\n------------")
				self.cursor.execute('''
				SELECT *
				FROM drivers''')
				rows = self.cursor.fetchall()
				for row in rows:
					print(" "+row[0])

				driver_pid=""
				truck_id=""
				while True:
					driver_pid = input("Enter driver PID (q = quit): \n==>")
					if driver_pid == 'q':
						go_back=True
						break
					self.cursor.execute('''
						SELECT *
						FROM drivers
						WHERE pid=?;''', (driver_pid, ))
					row = self.cursor.fetchone()
					if row == None:
						print("Invalid PID, try again")
					else:
						if row[2] == None:
							print("\nThe selected driver doesn't own a truck. \nSelect a truck_id from the list of company trucks: ")
							company_trucks=self.getcompanytrucks()
							while True:
								assigned_truck=input("Enter company truck id (q = quit): \n==>")
								if assigned_truck == 'q':
									go_back=True
									break
								valid_assigned_truck_input=False
								for i in company_trucks:
									for j in i:
										if assigned_truck == j:
											valid_assigned_truck_input=True
								if not valid_assigned_truck_input:
									print("Please enter a valid truck id")
								else:
									truck_id=assigned_truck
									break

						else:
							truck_id=row[2]
						break
				if not go_back:
					test=driver_pid
					####
					pick_up_cid = self.get_pickup_container(selected_agreement[2])
					if pick_up_cid == None:
						pick_up_cid="0000"
					available_containers=self.get_dropoff_containers(selected_agreement)
					if available_containers != None:
						available_container=""
						print("Enter an available container (q = quit): ")
						while True:
							available_container=input("==>")
							if available_container == 'q':
								go_back = True
								break
							if available_container not in available_containers:
								print("Please select a valid container")
							else:
								break
						if not go_back:
							service_date=""
							print("Enter service fulfillment date in the form YYYY-MM-DD (q = quit):")
							service_date=input("==>")
							if service_date == 'q':
								go_back=True
							if not go_back:
								master_account=selected_agreement[1]
								self.insert_service_fulfillment(selected_agreement, driver_pid, truck_id, pick_up_cid, available_container, service_date)


	def insert_service_fulfillment(self, service_agreement, driver_pid, truck_id, pick_up_cid, drop_off_cid, service_date):
		global cursor, connection
		service_no=service_agreement[0]
		master_account=service_agreement[1]
		insert_enroll = '''INSERT INTO service_fulfillments(date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up)
							VALUES (:service_date, :master_account, :service_no, :truck_id, :driver_pid, :drop_off_cid, :pick_up_cid);'''
		self.cursor.execute(insert_enroll, {"service_date": service_date, "master_account": master_account, "service_no": service_no, "truck_id": truck_id,"driver_pid": driver_pid,"drop_off_cid": drop_off_cid,"pick_up_cid": pick_up_cid})
		self.connection.commit()
		print("Service fulfillment table has been update\n")


	def getcompanytrucks(self):
		global connection, cursor
		self.cursor.execute('''
		SELECT truck_id FROM trucks
		EXCEPT
		SELECT owned_truck_id FROM drivers WHERE owned_truck_id IS NOT NULL
		''')

		row=self.cursor.fetchall()
		if row != None:
			for element in row:
				for value in element:
					print(" "+value)
		return row


	def get_dropoff_containers(self, service_agreement):
		global cursor, connection
		self.cursor.execute('''
			SELECT c.container_id
			FROM containers c, container_waste_types c2
			WHERE c2.waste_type=?
			AND c.container_id = c2.container_id
			EXCEPT
			SELECT cid_drop_off
			FROM service_fulfillments
			WHERE julianday('now') - julianday(date_time) < 0
			INTERSECT
			SELECT container_id FROM (SELECT distinct containers.container_id
			FROM containers
			EXCEPT
			SELECT containers.container_id
			FROM containers, service_fulfillments
			WHERE containers.container_id = service_fulfillments.cid_drop_off -- Containers that have never been dropped off

			UNION

			SELECT distinct s.cid_pick_up
			FROM service_fulfillments s
			INNER JOIN service_fulfillments s2 ON s.cid_pick_up = s2.cid_drop_off
			WHERE julianday(s.date_time) > julianday(s2.date_time)
			AND julianday(s2.date_time) =
			(SELECT MAX(julianday(s3.date_time))
			FROM service_fulfillments s3
			WHERE s2.cid_drop_off = s3.cid_drop_off))
			;

		''', (service_agreement[3],))
		row = self.cursor.fetchall()

		available_containers=[]
		if row != []:
			print("\nSelect an available container of waste type "+service_agreement[3]+": ")
			for element in row:
				for value in element:
					print(' '+value)
					available_containers.append(value)
		else:
			print("\nThere are no available containers for waste type "+service_agreement[3]+"\n")
			return None
		return available_containers


	def get_pickup_container(self, location):
		# Takes as input an address (location), and returns the container
		# id that is still there, i.e. hasn't been picked up since it was
		# dropped off at this location

		# Used by the dispatcher
		#
		global connection, cursor
		self.cursor.execute('''
			SELECT julianday('now')-julianday(s_f.date_time), s_f.cid_drop_off, s_a.service_no
			FROM service_fulfillments s_f, service_agreements s_a
			WHERE s_f.service_no = s_a.service_no
			AND s_a.location=?
			AND (julianday('now')-julianday(s_f.date_time)) > 0
			ORDER BY julianday('now')-julianday(s_f.date_time);
			''', (location,))
		row = self.cursor.fetchone()
		#row = cursor.fetchall()
		if row == None:
			return None
		else:
			return row[1]
