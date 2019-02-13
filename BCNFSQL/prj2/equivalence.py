#copy/paste this to the main file, or call it as a module.
#You only need to invoke setup_eq(), and it will do the rest.
#These functions need to be able to access attribute_closure_single
#and the database
import re

def attribute_closure_single(fds, attribute):
	old={}
	closure=attribute
	while old != closure:
		old = closure
		for fd in fds:
			if fd[0] <= closure and fd[1] not in closure:
				closure = closure.union(fd[1])
	return closure

def get_table_attributes(table_name):
	cursor.execute('SELECT I.Attributes FROM InputRelationSchemas I WHERE I.Name = ?',(table_name,))
	row = cursor.fetchone()

	table_attributes=[]
	set_attributes={i for i in row[0].split(',')}
	return set_attributes

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
		closure1 = attribute_closure_single(F1[1], FD[0]) #uses attribute_closure_single
		closure2 = attribute_closure_single(F2[1], FD[0])
		if closure1 > closure2:
			print("F1 and F2 are not equivalent.")
			return

	for FD in F2[1]:
		closure1 = attribute_closure_single(F1[1], FD[0])
		closure2 = attribute_closure_single(F2[1], FD[0])
		if closure1 < closure2:
			print("F1 and F2 are not equivalent.")
			return
	print("F1 and F2 are equivalent.")
	return

def setup_eq(pass_connection, pass_cursor):
	global cursor, connection
	cursor=pass_cursor
	connection=pass_connection
	print("Type 'quit' or 'exit' to quit")
	print("Type 'done' when you're finished entering schemas\n\n")
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
