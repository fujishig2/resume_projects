def weather_change(filename):
    try:
        file = open(filename)
        lst = file.read().split()
        for i in range(len(lst)-1):
            print(lst[i+1], "to", lst[i] + ", change =", float(lst[i+1]) - float(lst[i]))
    except:
        print("Error")