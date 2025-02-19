import csv
import re
import csv_read_write


# Check fake phone numbers, e.g. +1 777-777-7777
# Input: phone_list, fake_phone_repeat_threshold: 6
# Output: fake check result
def fake_phone_check(phone_list, fake_phone_repeat_threshold):
    output_list = []
    for row in phone_list:
        flag = 1
        if str(row) == "nan":
            flag = 0
        else:
            row = str(row)
            row = row.replace("-", "")
            row = row.replace("+", "")
            if fake_phone_repeat_threshold < max(row.count("0"), row.count("1"), row.count("2"), row.count("3"),
                                                 row.count("4"),
                                                 row.count("5"), row.count("6"), row.count("7"), row.count("8"),
                                                 row.count("9")):
                flag = -1
        output_list.append(flag)
    print("----------------Finished check fake phone number-------------------")
    return output_list


# description: get area code from phone number, e.g. 204 from +1 204-384-8909
# Input: phone_list: list of original phone number, fake_phone_repeat_threshold: number of repeat str of phone number
# Output: area code list from phone number
def get_area_code_from_phone(phone_list):
    area_code_list = []
    for row in phone_list:
        row = str(row)
        if len(row) > 5:
            if row[1] == '1':
                area_code = row[3] + row[4] + row[5]
            else:
                area_code = '0'
        else:
            area_code = '0'
        area_code_list.append(area_code)
    return area_code_list


# check if the area code from phone number is real area code
# If it is a canadian area code return area code, else return 0
# Input: area_code_str from phone number, path_area_code
# Output: get canadian province or 0
def get_province_from_areacode(area_code_str, path_area_code):
    areacode_reader = csv.reader(open(path_area_code))
    for row in areacode_reader:
        output = "0"
        result = re.search(area_code_str, row[1])
        if result:
            output = row[0]
            break
    return output


# get province from phone number, which used for match with city province
# Input: phone_list
# Output: province list
def get_province_from_phone(phone_list, path_area_code):
    area_code_list = get_area_code_from_phone(phone_list)
    province_list = []
    for row in area_code_list:
        if str(row) == "nan":
            province = "0"
        else:
            row = str(row)
            if row == "0":
                province = "0"
            else:
                phone_area = row
                province = get_province_from_areacode(phone_area, path_area_code)
        province_list.append(province)
    return province_list


# check if the phone number have a real canadian area code
# Input: phone_list
# Output: check result list
def check_phone_area_code(phone_list, path_area_code):
    area_code_list = get_area_code_from_phone(phone_list)
    check_area_code_list = []
    for row in area_code_list:
        row = str(row)
        if row == "0":
            flag = 0
        else:
            phone_area = row
            province = get_province_from_areacode(phone_area, path_area_code)
            if province == "0":
                flag = 0
            else:
                flag = 1
        check_area_code_list.append(flag)
    print("----------------Finished check phone area code-------------------")
    return check_area_code_list


# check repeat submitted profile phone number
# Input: phone_list, threshold_spamming = 4, threshold_serious = 2
# Output: result list
def check_repeat_phone(phone_list, threshold_spamming, threshold_serious):
    repeat_phone_list = []
    for i in phone_list:
        if i == "NONUMBER":
            index = 0
        else:
            if phone_list.count(i) >= threshold_spamming:
                index = -1
            elif threshold_spamming > phone_list.count(i) >= threshold_serious:
                index = 1
            elif phone_list.count(i) == 1:
                index = 0
        repeat_phone_list.append(index)
    print("----------------Finished check repeat submitted phone number-------------------")
    return repeat_phone_list

