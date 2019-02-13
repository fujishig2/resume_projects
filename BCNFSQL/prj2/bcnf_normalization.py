# Main module which should be called directly
# Creates objects from the drivers, supervisor, dispatcher, and account_managers class files, and
# executes the corresponding code in these classes depending on the input provided by the user

import sqlite3
import os.path
import pprint
import re
import time
from copy import deepcopy


# Determines if decomposition is dependency preserving
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

# Gets the function closure
# Used to determine dependency preservation
def function_closure(F, functions):
	closure = attribute_closure_single(functions, F[0]) #uses attribute_closure_single
	if (F[1] >= closure):
		return True
	return False

# Gets the single attribute closure of 1 fd and 1 attribute set
def attribute_closure_single(fds, attribute):
	old={}
	closure=attribute
	while old != closure:
		old = closure
		for fd in fds:
			if fd[0] <= closure and fd[1] not in closure:
				closure = closure.union(fd[1])
	return closure

# Gets the etire attribute closure of a schemas
# Calls atrtibute_closure_single on each fd
def attribute_closure(fd):
	attribute_closure=[]
	for element in fd:
		attribute_closure.append([element[0], attribute_closure_single(fd,element[0])])
	old = {}
	for i in fd:
		closure_set = i[0]
	return attribute_closure

# Returns a formatted set of attributes from InputRelationSchemas
# table_name is the 'Name' of the schema in InputRelationSchemas
def get_table_attributes(table_name):
	cursor.execute('SELECT I.Attributes FROM InputRelationSchemas I WHERE I.Name = ?',(table_name,))
	row = cursor.fetchone()

	table_attributes=[]
	set_attributes={i for i in row[0].split(',')}
	return set_attributes

# Returns formatted set of FDs from InputRelationSchemas, where table_name is the 'Name' in InputRelationSchemas
def format_fds(table_name):
	cursor.execute('SELECT I.FDs FROM InputRelationSchemas I WHERE I.Name = ?',(table_name,))
	row = cursor.fetchone()
	formated_arr=[]
	for element in row[0].split(';'):
		fd = re.sub('[{} ]','',element).split('=>')
		setx_set={i for i in fd[0].split(',')}
		sety_set={i for i in fd[1].split(',')}
		formated_arr.append((setx_set,sety_set))
	return formated_arr

# Gets all the candidate keys
# Uses the attribute closure and original attributes of a schema
def get_candidate_keys(attribute_closure, original_attributes):
	candidate_keys=[]
	for closure in attribute_closure:
		if closure[1] == original_attributes:
			candidate_keys.append(closure[0])
	return candidate_keys

# Simple BCNF test
# Return True if a candidate key is a subset of a FD attribute
def checkBCNF(candidate_keys, fd):
	for key in candidate_keys:
		if  key <= fd[0]:
			return True
	return False

# Primary decomposition function
# Needs the set of attributes and FDs from InputRelationSchemas, and the computed candidate keys
def BCNF_decomposition(attributes, fds, candidate_keys):
	decomp=[attributes, fds]
	isBCNF=False
	temp=[]
	while not isBCNF:
		isBCNF=True
		for j in range(0,len(decomp[1])):
			if j>=len(decomp[1]):
				break
			fd = decomp[1][j]
			for fd in decomp[1]:
				if not checkBCNF(candidate_keys, fd) :
					isBCNF=False
					bad_fd = fd
					decomp_new_attribues=decomp[0] - bad_fd[1]
					decomp_new_fds=decomp[1]
					decomp_new_fds.remove(bad_fd)
					temp.append([bad_fd[0]|bad_fd[1],bad_fd])
					decomp_new_fds_save = deepcopy(decomp_new_fds)
					decomp_arr=[]
					index=0
					for fd in decomp_new_fds_save:
						for i in bad_fd[1]:
							if i in fd[0]:
								if fd in decomp_new_fds:
									decomp_new_fds.remove(fd)
								index -= 1
							if i in fd[1]:
								if i in decomp_new_fds[index][1]:
									decomp_new_fds[index][1].remove(i)
								decomp_arr.append(fd)
							else:
								decomp_arr.append(fd)
						index += 1
					for fd in decomp_new_fds:
						if len(fd[0])==0 or len(fd[1]) == 0:
							decomp_new_fds.remove(fd)
					decomp=[decomp_new_attribues, decomp_new_fds]
					break
	if decomp[1] == []:
		temp.append([decomp[0],decomp[1]])
	else:
		temp.append([decomp[0],(decomp[1][0])])
	return temp

# Used to name the generated tables such that they match the attributes
def get_sorted_attributes(attributes, element):
	sorted_element=[]
	for value in attributes:
		if value in element:
			sorted_element.append(value)
	return sorted_element


# Adds elements to OutputRelationSchemas, as well as generates new tables
def addto_OutputRelationSchema(decomp, table_name):
	global connection, cursor
	table_order=[]
	cursor = connection.execute('SELECT * FROM '+table_name)
	column_names = list(map(lambda x: x[0], cursor.description))
	for element in decomp:
		output_table_name=table_name+'_'+'_'.join(get_sorted_attributes(column_names, element[0]))
		attributes=','.join(sorted(element[0]))
		fd1=""
		if element[1] != []:
			fd1='{'+','.join(sorted(element[1][0]))+'}'
		fd2=""
		if element[1] != []:
			fd2='{'+','.join(sorted(element[1][1]))+'}'
		if fd2 == "" and fd1 == "":
			final_fd='{'+attributes+'}=>{'+attributes+'}'
		else:
			final_fd=fd1+"=>"+fd2
		print("Adding into OutputRelationSchemas: "+output_table_name+" | "+attributes+" | "+final_fd)
		cursor.execute('''
		INSERT OR REPLACE INTO OutputRelationSchemas VALUES(?,?,?);''', (output_table_name, attributes, final_fd))
		connection.commit()
		print("Creating table: "+output_table_name)
		cursor.execute("DROP TABLE IF EXISTS "+output_table_name)
		cursor.execute("CREATE TABLE "+output_table_name+" AS SELECT "+attributes+" FROM "+table_name)
		cursor.execute("SELECT DISTINCT "+attributes+" FROM "+table_name)
		rows = cursor.fetchall()
		for line in rows:
			insert_values=[]
			for i in line:
				insert_values.append(i)
			insert_values_str=','.join(['"'+str(i)+'"' for i in insert_values])
			cursor.execute("INSERT INTO "+output_table_name+"("+attributes+")"+" VALUES("+insert_values_str+");")
			connection.commit()


# Primary function of BCNF, which is called from project2.py
def bcnf_main(pass_cursor, pass_connection):
	global cursor, connection
	cursor=pass_cursor
	connection=pass_connection

	cursor.execute('''SELECT Name FROM InputRelationSchemas WHERE hasInstance=1''')
	print("Select one of the table names from InputRelationSchemas: (q = quit)")
	table_names=[row[0] for row in cursor.fetchall()]
	for table_name in table_names:

		print("\t"+table_name)
	while True:
		user_table=input("=>")
		if user_table in table_names:
			candidate_keys = get_candidate_keys(attribute_closure(format_fds(user_table)), get_table_attributes(user_table))
			decomp=BCNF_decomposition(get_table_attributes(user_table), format_fds(user_table), candidate_keys)
			original = (get_table_attributes(user_table), format_fds(user_table))
			depend_preserv(original, decomp)
			addto_OutputRelationSchema(decomp,user_table)
			break
		elif user_table == 'q':
			return
		else:
			print("Please enter a valid table name")
