# Main module which should be called directly
# Creates objects from the drivers, supervisor, dispatcher, and account_managers class files, and
# executes the corresponding code in these classes depending on the input provided by the user

import sqlite3
import os.path
import pprint
import re
import time
from copy import deepcopy


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


# Interface for adding new user. Called when user enters '2' from home (main) screen
# Prompts user for login, role, password and PID from available list.
# Upon successful completion, a new user is inserted into the 'users' table with the corresponding data
# The user can enter 'q' at any time to go back to the home screen
def add_user():
	# Adds a user to table
	global connection, cursor
	user_login=input("Enter user login (q = quit): \n==>")
	if user_login == 'q':
		return
	user_role=input("Enter role (q = quit): \n==>")
	if user_role == 'q':
		return
	user_password=input("Enter password (q = quit): \n==>")
	if user_password == 'q':
		return

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
	print("Enter PID (q = quit): ")
	user_id = ""
	while True:
		user_id = input("==>")
		if user_id == 'q':
			return
		elif user_id not in available_pids:
			print("Please select a valid PID")
		else:
			break

	insert_enroll = "INSERT INTO users(user_id, role, login, password) VALUES (:user_id, :user_role, :user_login, :user_password);"
	cursor.execute(insert_enroll, {"user_id": user_id, "user_role": user_role, "user_login": user_login, "user_password" :hash_password(user_password)})
	connection.commit()


def PrettyPrint(table, justify = "R", columnWidth = 0):
    # Not enforced but
    # if provided columnWidth must be greater than max column width in table!
    if columnWidth == 0:
        # find max column width
        for row in table:
            for col in row:
                width = len(str(col))
                if width > columnWidth:
                    columnWidth = width

    outputStr = ""
    for row in table:
        rowList = []
        for col in row:
            if justify == "R": # justify right
                rowList.append(str(col).rjust(columnWidth))
            elif justify == "L": # justify left
                rowList.append(str(col).ljust(columnWidth))
            elif justify == "C": # justify center
                rowList.append(str(col).center(columnWidth))
        outputStr += ' '.join(rowList) + "\n"
    return outputStr

# Testing functions
def get_schemas():
	global connection, cursor
	cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
	for tables in cursor.fetchall():
		for row in tables:
			print(row)
def get_inputrelations():
	global connection, cursor
	cursor.execute("SELECT * FROM InputRelationSchemas")
	table=[]
	table.append(["Name","Attributes","FDs", "hasInstance"])
	print("Name | Attributes | FDs | hasInstance")
	for row in cursor.fetchall():
		table.append(row)
		print(' | '.join([str(i) for i in row]))
	#table.append(["asdf","qwer","asdfkjhasdf","qwerqwer"])
	#print(PrettyPrint(table,"R",50))

def get_outputrelations():
	global connection, cursor
	tbl = []
	print('Name | Attributes | FDs | hasInstance')
	cursor.execute("SELECT * FROM OutputRelationSchemas")
	for row in cursor.fetchall():
		#tbl.append(row)
		print(' | '.join([str(i) for i in row]))

	print(PrettyPrint(tbl,"R",5))
def get_r1():
	global connection, cursor
	tbl = []
	tbl.append(['A','B','C','D','E','F','G','H','K'])
	tbl.append(['--','--','--','--','--','--','--','--','--'])
	cursor.execute("SELECT * FROM R1")
	for row in cursor.fetchall():
		tbl.append(row)
	print(PrettyPrint(tbl))

def get_person():
	global connection, cursor
	tbl = []
	tbl.append(['SSN','Name','Address','Hobby'])
	tbl.append(['----','-----','--------','-----'])

	cursor.execute("SELECT * FROM Person")
	for row in cursor.fetchall():
		tbl.append(row)
	print(PrettyPrint(tbl,"R",15))

def attribute_closure_single(fds, attribute):
	old={}
	closure=attribute
	while old != closure:
		old = closure
		for fd in fds:
			if fd[0] <= closure and fd[1] not in closure:
				closure = closure.union(fd[1])
	return closure

def attribute_closure(fd):
	attribute_closure=[]
	for element in fd:
		attribute_closure.append([element[0], attribute_closure_single(fd,element[0])])


	old = {}

	for i in fd:
		closure_set = i[0]
	return attribute_closure

def get_table_attributes(table_name):
	cursor.execute('SELECT I.Attributes FROM InputRelationSchemas I WHERE I.Name = ?',(table_name,))
	row = cursor.fetchone()

	table_attributes=[]
	set_attributes={i for i in row[0].split(',')}
	return set_attributes




def format_fds(table_name):
	cursor.execute('SELECT I.FDs FROM InputRelationSchemas I WHERE I.Name = ?',(table_name,))
	row = cursor.fetchone()
	dictionary={}
	x={1,2,3}
	formated_arr=[]

	for element in row[0].split(';'):

		fd = re.sub('[{} ]','',element).split('=>')
		setx_arr=[]
		setx_set={i for i in fd[0].split(',')}
		sety_set={i for i in fd[1].split(',')}
		formated_arr.append((setx_set,sety_set))


	return formated_arr

def get_candidate_keys(attribute_closure, original_attributes):
	candidate_keys=[]
	for closure in attribute_closure:
		print("Attribute closure, ",closure)
		if closure[1] == original_attributes:
			candidate_keys.append(closure[0])
	#return [{'H','B'}]
	print(candidate_keys)
	#return [{'B','C','D'}]
	#return [{'A','B','H'}, {'B','H'}]
	return candidate_keys



def checkBCNF(candidate_keys, fd):
	for key in candidate_keys:
		if  key <= fd[0]:
			print("TRUE",key, fd)
			return True
	print("FALSE", fd)
	return False

def BCNF_decomposition(attributes, fds, candidate_keys):
	decomp=[attributes, fds]
	print("Original decomp: ",end='')
	print(decomp)
	isBCNF=False
	temp=[]
	while not isBCNF:
		isBCNF=True
		for j in range(0,len(decomp[1])):
		##for fd in decomp:
			print("j: "+str(j))
			if j>=len(decomp[1]):
				break
			fd = decomp[1][j]

			for fd in decomp[1]:
				print("DECOMP: ",decomp)
				print("TEMP ",temp)
				if not checkBCNF(candidate_keys, fd) :

					isBCNF=False
					bad_fd = fd
					print("\nbad_fd: ",end='')
					print(bad_fd)
					decomp_new_attribues=decomp[0] - bad_fd[1]
					print("new attributes: ",end='')
					print(decomp_new_attribues)
					decomp_new_fds=decomp[1]
					decomp_new_fds.remove(bad_fd)
					temp.append([bad_fd[0]|bad_fd[1],bad_fd])
					#decomp_new_fds[1].remove(fd)
					decomp_new_fds_save = deepcopy(decomp_new_fds)

					decomp_arr=[]
					index=0
					for fd in decomp_new_fds_save:
						print(" > checking ",fd)
						print(decomp_new_fds)

						for i in bad_fd[1]:
							if i in fd[0]:
								#fd[0].remove(i)
								print(" > removing ",fd)
								if fd in decomp_new_fds:
									decomp_new_fds.remove(fd)
								index -= 1
								#break
							if i in fd[1]:
								print(" > removing "+i+" from ",fd)
								print(" - ",decomp_new_fds, index)
								if i in decomp_new_fds[index][1]:
									decomp_new_fds[index][1].remove(i)

								print(" 	> new fd ",fd)
								print("		> new decomp ",decomp_new_fds)
								decomp_arr.append(fd)
								#break

							else:		
								#fd = (fd[0], fd[0])
								decomp_arr.append(fd)
						index += 1

					print('\n')
					for i in decomp_new_fds:
						print(i)
					print('\n')
					for fd in decomp_new_fds:
						if len(fd[0])==0 or len(fd[1]) == 0:
							decomp_new_fds.remove(fd)
					print("new fds: ",end='')
					print(decomp_new_fds)

					decomp=[decomp_new_attribues, decomp_new_fds]
					print('new decomp: ',end='')
					print(decomp)
					break
					#decomp.append([bad_fd[0]|bad_fd[1],bad_fd])
					#break
					#time.sleep(5000)
	print("APPENDING: ",decomp)
	if decomp[1] == []:

		temp.append([decomp[0],decomp[1]])
	else:
		temp.append([decomp[0],(decomp[1][0])])

	return temp





def addto_OutputRelationSchema(decomp, table_name):
	global connection, cursor
	print("\n\n\n")
	print(table_name)
	for element in decomp:
		print(element)
		output_table_name=table_name+'_'+'_'.join(sorted(list(element[0])))
		attributes=','.join(sorted(list(element[0])))
		fd1=""
		if element[1] != []:
			print(element[1])
			fd1='{'+','.join(sorted(list(element[1][0])))+'}'
		fd2=""
		if element[1] != []:
			fd2='{'+','.join(sorted(list(element[1][1])))+'}'

		if fd2 == "" and fd1 == "":
			final_fd='{'+attributes+'}=>{'+attributes+'}'
		else:
			final_fd=fd1+"=>"+fd2
		print("Table name: ",output_table_name)
		print("attributes: ",attributes)
		print("fds",final_fd)
		cursor.execute('''
		INSERT OR REPLACE INTO OutputRelationSchemas VALUES(?,?,?);''', (output_table_name, attributes, final_fd))

		connection.commit()

		cursor.execute("DROP TABLE IF EXISTS "+output_table_name)
		cursor.execute("CREATE TABLE "+output_table_name+" AS SELECT "+attributes+" FROM "+table_name)

		cursor.execute("SELECT DISTINCT "+attributes+" FROM "+table_name)
		rows = cursor.fetchall()
		for line in rows:
			insert_values=[]
			for i in line:
				insert_values.append(i)

				#print(i, end=' ')
			print('\n')
			print(insert_values)
			insert_values_str=','.join(['"'+str(i)+'"' for i in insert_values])
			print("INSERT INTO "+output_table_name+"("+attributes+")"+" VALUES("+','.join([str(i) for i in insert_values])+");")
			cursor.execute("INSERT INTO "+output_table_name+"("+attributes+")"+" VALUES("+insert_values_str+");")
			#connection.commit()




def BCNF_decomp2(attributes, fds, candidate_key):
	i=0
	decomp=[attributes, fds]
	for fd in fds[1]:
		s=(fd[0]|fd[1], fd[0])
		BCNF_decomposition(s, attributes, )



def insertInto():
	global connection, cursor
	cursor.execute("INSERT INTO InputRelationSchemas ")
	
def equivalence_interface():
	global connection, cursor
	cursor.execute("SELECT I.Name FROM InputRelationSchemas I")
	rows = cursor.fetchall()
	input_schemas = []
	for row in rows:
		input_schemas.append(row[0])
	user_input = ""
	schemas = []
	i = 1
	while True:
		user_input = input("Please enter schema #" + str(i) + ": ") 
		if user_input.lower() == 'quit' or user_input.lower() =="exit": 
			return False
		elif user_input.lower() == 'done':
			return schemas
		while user_input not in input_schemas:
			print("Error! schema not found in input relations.")
			user_input = input("Please enter schema #" + str(i) + ": ")
			if user_input.lower() == 'quit' or user_input.lower() =="exit": 
				return False
			elif user_input.lower() == 'done':
				return schemas					
		schemas.append(user_input)
		i += 1

def function_union(schemas):
	global connection, cursor
	A = set()
	F = []
	for schema in schemas:
		A1 = get_table_attributes(schema)
		A = A | set(A1)
		F1 = format_fds(schema)
		for FD in F1:
			if FD not in F:
				F.append(FD)
	return (A, F)

def equivalence_set(F1, F2):
	for FD in F1[1]:
		closure1 = attribute_closure_single(F1[1], FD[0])
		closure2 = attribute_closure_single(F2[1], FD[0])
		#print(closure1, closure2)
		if closure1 > closure2:
			print("F1 and F2 are not equivalent.")
			return
	
	for FD in F2[1]:
		closure1 = attribute_closure_single(F1[1], FD[0])
		closure2 = attribute_closure_single(F2[1], FD[0])
		#print(closure1, closure2)
		if closure1 < closure2:
			print("F1 and F2 are not equivalent.")
			return			
	print("F1 and F2 are equivalent.")
	return

def setup_eq():
	print("Type quit or exit to quit")
	print("Type done when you're finished entering schemas\n\n")	
	print("Creating F1:")
	schemas1 = equivalence_interface()
	if schemas1 == False:
		return
	F1 = function_union(schemas1)
	print("\n\nCreating F2:")
	schemas2 = equivalence_interface()
	if schemas2 == False:
		return	
	F2 = function_union(schemas2)
	equivalence_set(F1, F2)	
	return

def depend_preserv(original, decomp):
	functions = []
	for relation in decomp:
		if not relation[1]:
			functions.append((relation[0], relation[0]))
		else:
			functions.append(relation[1])
	for F in original[1]:
		if F not in functions:
			if not function_closure(F, functions):
				print("This decomposition is not dependency preserving.")
				return False
	print("This decomposition is dependency preserving.")
	return True

def function_closure(F, functions):
	print(functions)
	print(F)
	closure = attribute_closure_single(functions, F[0])
	if (F[1] >= closure):
		return True
	return False

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
		print(" 4 - (TESTING) get schema of db")
		print(" 5 - (TESTING) get InputRelationSchemas table")
		print(" 6 - (TESTING) get OutputRelationSchemas table")
		print(" 7 - (TESTING) get R1 table")
		print(" 8 - (TESTING) get Person table")
		print(" 9 - (TESTING) format FD")
		print(" q - Exit program")

		user_input = input("==>")
		if user_input == '1':
			print("BCNF normalization")
		elif user_input == '2':
			print("Attribute closures")
		elif user_input == '3':
			setup_eq()
		elif user_input == 'q':
			print("Goodbye!")
			return
		elif user_input == '4':
			get_schemas()
		elif user_input == '5':
			get_inputrelations()
		elif user_input == '6':
			get_outputrelations()
		elif user_input == '7':
			get_r1()
		elif user_input == '8':
			get_person()
		elif user_input == '9':
			get_table_attributes("ForAttrClosureF1")
			table_name="ForAttrClosureF1"
			print(format_fds(table_name))
			candidate_keys = get_candidate_keys(attribute_closure(format_fds(table_name)), get_table_attributes(table_name))

			print(candidate_keys)
			decomp=BCNF_decomposition(get_table_attributes(table_name), format_fds(table_name), candidate_keys)

			print("\n\nDECOMP FINAL: ",decomp)
			original = get_table_attributes(table_name), format_fds(table_name)
			depend_preserv(original, decomp)
			
			
			#addto_OutputRelationSchema(decomp,table_name)
			
			


		else:
			print("Invalid option!")

if __name__ == "__main__":
	main()
