import re
import spacy
import en_core_web_sm
import nltk
import csv_read_write
from check_age import get_age_list


nlp = en_core_web_sm.load()
NER = spacy.load("en_core_web_sm")


# check email format
def check_email_format(email_list):
    email_format_list = []
    for row in email_list:
        if str(row) == "nan":
            output = "0"
        else:
            text = str(row)
            if re.match(r'^[a-zA-Z0-9_.-]{3,30}@[a-zA-Z0-9-]{1,13}(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', text):
                output = "1"
            else:
                output = "-1"
        email_format_list.append(output)
    print("----------------Finished check email format-------------------")
    return email_format_list


# NLP processing
# Input: str to analysis
# Output: if it contain name
def nltk_test(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person = []
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON' or t.label() == 'GPE' or t.label() == 'GSP'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
    if len(person) == 0:
        output = "0"
    else:
        output = "1"
    return person


# check if email contain customers name
# Input: email_list, name_list
# Output: result list
def check_email_name(email_list, name_list):
    flag = 0
    output_list = []
    for row in email_list:
        if str(row) == "nan":
            output = "0"
        else:
            output = str(row).split('@')[0].capitalize()
        if str(name_list[flag]).lower() in output:
            result = 1
        else:
            result = 0
        flag += 1
        output_list.append(result)
    print("----------------Finished check if email contain user name-------------------")
    return output_list


# check if email age match user input age
# Input: email_list, age_16_list, age_18_list
# Output: result list
def check_email_age(email_list, age_16_list, age_18_list):
    flag = 0
    age_list = get_age_list(age_16_list, age_18_list)
    match_list = []
    for row in email_list:
        match = 0
        if str(row) == "nan":
            age = "NONE"
        else:
            text = row.split("@")[0]
            text_num = re.findall("\d+",text)
            if not text_num:
                age = "NONE"
            else:
                if 2010 > int(text_num[0]) > 1920:
                    match = -1
                    if int(text_num[0]) < 2005:
                        age = "True"

                    else:
                        age = "False"
                else:
                    age = "NONE"

        if age_list[flag] == 'No_Age':
            match = 0
        else:
            if age == age_list[flag]:
                match = 1
        flag += 1
        match_list.append(match)
    print("----------------Finished check email age match user input age-------------------")
    return match_list


# check email popular domain
# Input: email_list
# Output: result list
def check_email_domain(email_list):
    domain_str = "domain: gmail.com, hotmail.com, outlook.com, yahoo.ca, yahoo.com, icloud.com, mail.com, telus.net, " \
                 "live.ca, live.com,  shaw.ca "
    csv_reader = email_list
    output_list = []
    for row in csv_reader:
        if str(row) == "nan":
            output = "No Email"
        else:
            output = row[0].split("@")[1]
        if output in domain_str:
            output = "1"
        else:
            output = "-1"
        output_list.append(output)
    print("----------------Finished check email popular domain-------------------")
    return output_list

