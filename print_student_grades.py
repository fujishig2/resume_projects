def print_student_grades(filename):
    file = open(filename)
    lst = []
    while lst != [""]:
        lst = file.readline().strip().split(",")
        total = 0
        for i in lst[1:]:
            total+= int(i)
        if total != 0:
            avg = total/(len(lst)-1)
            print(lst[0], "- final grade:", avg)    
        