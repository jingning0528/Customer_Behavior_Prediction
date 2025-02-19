import spacy
import en_core_web_sm
import csv_read_write
import nltk


nlp = en_core_web_sm.load()
NER = spacy.load("en_core_web_sm")


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
    return output


# check if it is a common name
# Input: name list
# Output: result list
def check_name_entity(check_list):
    output_list = []
    for row in check_list:
        if not row:
            output = "0"
        else:
            output = nltk_test(str(row).capitalize())
        output_list.append(output)
    print("----------------Finished check name-------------------")
    return output_list


