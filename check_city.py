import time
import csv
from fuzzywuzzy import process


# Get the standard cities list
# Input: path of canadian cities as reference
# Output: standard cities list
def get_standard_cities(path_canadian_cities):
    cities_list = []
    csv_reader = csv.reader(open(path_canadian_cities))
    for row in csv_reader:
        if row:
            row[1] = row[1].replace("'", "")
            cities_list.append(row[1])
    return cities_list


# Get the standard cities list
# Input: path of canadian cities as reference
# Output: standard cities list
def get_standard_province(path_canadian_cities):
    province_list = []
    csv_reader = csv.reader(open(path_canadian_cities))
    for row in csv_reader:
        if row:
            row[0] = row[0].replace("'", "")
            province_list.append(row[0])
    return province_list


# Get the fuzzy result of a city compared with standard canadian cities
# Input: original_city_list, path_canadian_cities
# Output: (City, Score)
def get_fuzzy_score(original_city_list, path_canadian_cities):
    start = time.time()
    print("----------------Start get fuzzy list-------------------")
    cities = get_standard_cities(path_canadian_cities)
    output_list = []
    score_list = []
    for row in original_city_list:
        if not row:
            output = ("0", 0)
        else:
            text = str(row)
            text = text.split(" ")[0]
            output = process.extractOne(text.lower(), cities)
        output_list.append(output)
        score_list.append(output[1])
    end = time.time()
    print("----------------Get fuzzy list-------------------Run time:", end-start)

    return output_list
    #return score_list


# Get the new list of cities province
# Input: city_fuzzy_list = get_fuzzy_score(original_city_list, path_canadian_cities),
#           original_city_list, path_canadian_cities
# Output: province for following processing
def get_city_province(city_fuzzy_list, path_canadian_cities):
    standard_province_list = get_standard_province(path_canadian_cities)
    standard_cities_list = get_standard_cities(path_canadian_cities)
    new_city_list = []
    for row in city_fuzzy_list:
        new_city_flag = -1
        for col in standard_cities_list:
            new_city_flag += 1
            new_city = "0"
            if str(row[0]) == col:
                new_city = standard_province_list[new_city_flag]
                break
        new_city_list.append(new_city)
    return new_city_list


# Check the if it is a real city name
# Input: city_fuzzy_list = get_fuzzy_score(original_city_list, path_canadian_cities)
#       original_city_list, path_canadian_cities, threshold_high = 80, threshold_low = 40
# Output: result of check city
def check_city_score(city_fuzzy_list, threshold_high):
    city_flag_list = []
    for row in city_fuzzy_list:
        if str(row[1]) == "nan":
            city_flag = 0
        else:
            row = int(row[1])
            if row >= threshold_high:
                city_flag = 1
            else:
                city_flag = 0
            city_flag_list.append(city_flag)
    print("----------------Finished check city score-------------------")
    return city_flag_list


# Get the province match result between city and phone number
# Input: original_city_list, path_canadian_cities, phone_province_list
# Output: match result
def check_match_province(city_fuzzy_list, path_canadian_cities, phone_province_list):
    city_province_list = get_city_province(city_fuzzy_list, path_canadian_cities)
    match_list = []
    for row in range(len(city_province_list)):
        if city_province_list[row] == "0":
            match_flag = 0
        elif phone_province_list[row] == "0":
            match_flag = 0
        elif city_province_list[row] == phone_province_list[row]:
            match_flag = 1
        else:
            match_flag = 0
        match_list.append(match_flag)
    print("----------------Finished check match province-------------------")
    return match_list




