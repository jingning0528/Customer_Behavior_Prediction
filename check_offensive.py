import csv
import csv_read_write


# get the reference offensive file
def get_offensive_list(path_offensive):
    offensive_list = []
    csv_reader = csv.reader(open(path_offensive))
    for row in csv_reader:
        if row:
            offensive_list.append(row[0])
    return offensive_list


# Check if the input list contain offensive word
# Input: detect_list, path_offensive
# Output: check result
def offensive_detect(detect_list, path_offensive):
    column1 = detect_list
    column2 = get_offensive_list(path_offensive)
    output_list = []
    for i in column1:
        if str(i) == "nan":
            index = "0"
        else:
            i = str(i)
            for j in column2:
                j = str(j)
                flag = i.lower().find(j)
                if flag != -1:
                    index = "-1"
                    break
                else:
                    index = "0"
        output_list.append(index)
    print("----------------Finished check offensive word-------------------")
    return output_list

