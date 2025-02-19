import csv_read_write
import re
import numpy as np


# check budget
# Input: budget_list, biweekly_budget_list,
#                  high_budget = 50000,
#                  low_budget = 10000,
#                  high_biweekly_budget = 450,
#                  low_biweekly_budget = 150
# Output: result list
def check_budget(budget_list,
                 biweekly_budget_list,
                 high_budget,
                 low_budget,
                 high_biweekly_budget,
                 low_biweekly_budget
                 ):
    check_budget_list = []
    check_biweekly_budget_list = []
    check_list = budget_list
    for row in budget_list:
        if str(row) == "nan":
            check_budget_list.append(0)
        else:
            row = row.replace(",", "")
            text_num = re.findall("\d+", row)
            if int(text_num[0]) <= low_budget:
                check_budget_list.append(-1)
            elif int(text_num[len(text_num) - 1]) >= high_budget:
                check_budget_list.append(1)
            else:
                check_budget_list.append(0)
    for row in biweekly_budget_list:
        if str(row) == "nan":
            check_biweekly_budget_list.append(0)
        else:
            row = row.replace(",", "")
            text_num = re.findall("\d+", row)
            if int(text_num[0]) <= low_biweekly_budget:
                check_biweekly_budget_list.append(-1)
            elif int(text_num[len(text_num) - 1]) >= high_biweekly_budget:
                check_biweekly_budget_list.append(1)
            else:
                check_biweekly_budget_list.append(0)
    #check_list = np.sum([check_budget_list, check_biweekly_budget_list], axis=0)
    for i in range(len(check_budget_list)):
        check_list[i] = check_budget_list[i] + check_biweekly_budget_list[i]
        if check_list[i] == -2:
            check_list[i] = -1
    print("----------------Finished check budget-------------------")
    return check_list


# check cartype
# Input: cartype_list, high_level_cartype_list = ["EV", "SUV"]
# Output: result list
def check_cartype(cartype_list, high_level_cartype):
    check_cartype_list = []
    for row in cartype_list:
        if str(row) == "nan":
            check_flag = 0
        else:
            if str(row) in high_level_cartype:
                check_flag = 1
            else:
                check_flag = 0
        check_cartype_list.append(check_flag)
    print("----------------Finished check cartype-------------------")
    return check_cartype_list


# check if customers want a high level cartype with low budget
# Input: check_budget_list, check_cartype_list
# Output: result list
def check_budget_cartype(check_budget_list, check_cartype_list):
    check_budget_cartype_list = []
    for row in range(len(check_cartype_list)):
        if check_budget_list[row] == -1 & check_cartype_list[row] == 1:
            check_budget_cartype_list.append(-1)
        else:
            check_budget_cartype_list.append(0)
    print("----------------Finished check if customers want a high level cartype with low budget-------------------")
    return check_budget_cartype_list

