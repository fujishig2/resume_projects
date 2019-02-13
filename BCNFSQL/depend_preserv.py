#need to call depend_preserv with the original relation setup using this:
#original = (get_table_attributes(table_name), format_fds(table_name))
#decomp is the DECOMP FINAL.
#These functions need to be able to access attribute_closure_single
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
	closure = attribute_closure_single(functions, F[0]) #uses attribute_closure_single
	if (F[1] >= closure):
		return True
	return False