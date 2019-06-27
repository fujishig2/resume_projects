#--------------------------------------------
# Name:      Kyle Fujishige
# Program:   Lab4_KF.py
#--------------------------------------------

#Description:   Read in a file and divide the file into a number output files.
#Syntax:        file_split(input_file, num_of_output_files)
#Parameters:    input_file          – the file to be split
#               num_of_output_files – the number of output files to create
#Returns:       nothing

def file_split(input_file, num_of_output_files):
    try:
        orig_file = open(input_file)
        temp_list = orig_file.readlines()
        orig_file.close()
    
        
        for i in range(num_of_output_files):
            #**************WILL NEED TO USE A DIFFERENT FILE PATH FOR A NEW FILE**************
            new_file = open(r"C:\Users\User\Downloads\CMPT 103\data"+str(i+1)+".txt", "x")
            new_file_contents = ""            
            
        
            #start value is equal to the (total # of lines/# of output files)*i + (total # of lines % # of output files/output files) to make the remainder split evenly amongst the files
            start = int((len(temp_list)/num_of_output_files)*i+len(temp_list)%num_of_output_files/num_of_output_files)
            
            
            #end value is equal to the (total # of lines/# of output files)*(i+1) + (total # of lines % # of output files/output files) to make the remainder split evenly amongst the files.
            end = int((len(temp_list)/num_of_output_files) *(i+1)+len(temp_list)%num_of_output_files/num_of_output_files)


            for j in range(start, end):
                new_file_contents += temp_list[j]
            new_file.write(new_file_contents)
            new_file.close()
            
            
    #There is an input failure if it jumps to the exception.    
    except IOError:
        print("Error! Invalid file path inputted")
    except TypeError:
        print("Error! Invalid data type inputted in num_of_output_files")
        
        
        
#Description:   Read in a file of tags and sequences, and put the tag/sequence pairs into a list of lists.
#Syntax:        data_list = input_sequences(filename)
#Parameters:    filename     - the input file of tags and sequences
#Returns:       keys_and_seq - a list of lists made up of keys and sequence pairs

def input_sequences(filename):
    orig_file = open(filename)
    temp_list = orig_file.readlines()
    orig_file.close()
    
    keys = []
    seq = []
    keys_and_seq = []
    i = -1 
    
    for elem in temp_list:
        if ">" in elem:
            #appends the key to keys, and strips all uncessary characters/spaces
            keys.append(elem.strip(">").strip())
            i += 1
            #seq now gets appended witha blank string, so it can be added upon
            seq.append("")
            
        else: 
            #since seq[i] was a blank string, you can keep adding strings (sequences) to seq[i]
            seq[i] += elem.strip()

    for i in range(len(keys)):
        keys_and_seq.append([keys[i], seq[i]])
    
    return keys_and_seq