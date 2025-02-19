# preprocessing the age list
# Input: age_16_list, age_18_list
# Output: age_list
def get_age_list(age_16_list, age_18_list):
    age_list = age_16_list
    for i in range(len(age_16_list)):
        age_list[i] = str(age_16_list[i])+str(age_18_list[i])
        if age_list[i] == "Truenan":
            age_list[i] = "True"
        if age_list[i] == "Falsenan":
            age_list[i] = "False"
        if age_list[i] == "nanTrue":
            age_list[i] = "True"
        if age_list[i] == "nanFalse":
            age_list[i] = "False"
        if age_list[i] == "TrueFalse":
            age_list[i] = "True"
        if age_list[i] == "FalseTrue":
            age_list[i] = "True"
        if age_list[i] == "nannan":
            age_list[i] = "No_Age"
    return age_list


# check age
def check_age(age_16_list, age_18_list):
    age_list = get_age_list(age_16_list, age_18_list)
    age_priority_list = []
    for i in age_list:
        if i == "True":
            age_priority = 1
        elif i == "False":
            age_priority = 0
        elif i == "No_Age":
            age_priority = 0
        else:
            age_priority = 0
        age_priority_list.append(age_priority)
    print("----------------Finished check age-------------------")
    return age_priority_list

