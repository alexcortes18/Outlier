from bs4 import BeautifulSoup as bs
# import bs4
# import json
# import jsonlines
from tqdm import tqdm

file = open('med.cd.az.xml', 'r', encoding='utf-8')
content = file.readlines()
bs_contents = []
for line in tqdm(content):
    bs_contents.append(bs(line, "html.parser"))

counter = 1
my_dict = {}

error_list = {}
error_counter = 1

for bs_content in tqdm(bs_contents):
    word_dict = {}
    for entry in bs_content.find_all('HOMOGRAPH'.lower()):
        id = entry['id']

        if entry.find('entry0'.lower()) != None:
            record = entry.find('entry0'.lower()).text
        elif entry.find('entry13'.lower()) != None:
            record = entry.find('entry13'.lower()).text

        if entry.find('PART-OF-SPEECH'.lower()) != None:
            pos = entry.find('PART-OF-SPEECH'.lower()).text
        else:
            pos = []

        node1_list = []
        node1_list.append({'ID': id})
        node1_list.append({'POS': pos})

        for child1 in entry.contents:
            node1 = {}
            if child1.next.name is not None:
                node2_list = []
                for child2 in child1.contents:
                    node2 = {}
                    if child2.next.name is not None and child2.name is not None:
                        node3_list = []

                        child2_length = len(child2.contents)
                        for i in range(child2_length):
                            if child2.contents[i].name is not None:
                                child3 = child2.contents[i]
                                node3 = {}

                                if child3.next.name is not None:
                                    node4_list = []
                                    for child4 in child3.contents:
                                        node4 = {}
                                        if child4.next.name is not None and child4.name is not None:
                                            node5_list = []

                                            child4_length = len(child4.contents)
                                            for i in range(child4_length):
                                                if child4.contents[i].name is not None:
                                                    child5 = child4.contents[i]
                                                    if child5 in child4.contents:
                                                        node5 = {}
                                                        if child5.next.name is not None:
                                                            node5[child5.name] = child5.text
                                                            node5_list.append(node5)
                                                        else:
                                                            node5[child5.name] = child5.text
                                                            node5_list.append(node5)
                                                        node4[child4.name] = node5_list
                                                        node4_list.append(node4)
                                        else:
                                            node4[child4.name] = (child4.text)
                                            node4_list.append(node4)
                                    node3[child3.name] = node4_list
                                    node3_list.append(node3)
                                else:
                                    node3[child3.name] = (child3.text)
                                    node3_list.append(node3)
                        node2[child2.name] = node3_list
                        node2_list.append(node2)
                    else:
                        node2[child2.name] = (child2.text)
                        node2_list.append(node2)
                node1[child1.name] = node2_list
                node1_list.append(node1)
            else:
                continue
        my_dict[record] = node1_list
        break

# print(my_dict['record1'])
import json

# Replace 'record1' with the actual record key you want to inspect
record_key = 'record1'

# Ensure the key exists in the dictionary
if record_key in my_dict:
    # Write the content to a file in a readable format
    with open('output_record.txt', 'w', encoding='utf-8') as file:
        json.dump(my_dict[record_key], file, indent=4, ensure_ascii=False)
    print(f"Output written to 'output_record.txt'")
else:
    print(f"Key '{record_key}' not found in my_dict")
